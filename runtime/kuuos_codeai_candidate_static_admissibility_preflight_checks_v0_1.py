from __future__ import annotations
import ast,re,sys
from pathlib import PurePosixPath
from runtime.kuuos_codeai_typed_structured_edit_ir_v0_1 import OP_CREATE_FILE,OP_DELETE_SYMBOL
from runtime.kuuos_codeai_candidate_static_admissibility_preflight_schema_v0_1 import *
LIMPORT=re.compile(r'^\s*import\s+([A-Za-z0-9_.\'/-]+)'); LDECL=re.compile(r'^\s*(?:private\s+|protected\s+)?(?:noncomputable\s+)?(?:def|theorem|lemma|structure|inductive|abbrev|class|instance)\s+([A-Za-z_][A-Za-z0-9_\'.]*)')
def collision_findings(ops):
 out=[]; by={}
 for o in ops: by.setdefault(o['path'],[]).append(o)
 for p,xs in sorted(by.items()):
  if any(o['operation']==OP_CREATE_FILE for o in xs) and len(xs)>1: out.append(finding('create_path_operation_collision',SEVERITY_REJECT,p)); continue
  def span(o):
   a,b=o['application_start_line'],o['application_end_line']; return (a,a,True) if b<a else (a,b,False)
  for i,a in enumerate(xs):
   sa,ea,ia=span(a)
   for b in xs[i+1:]:
    sb,eb,ib=span(b); hit=(sa==sb if ia and ib else eb>=sa>=sb-1 if ia else ea>=sb>=sa-1 if ib else max(sa,sb)<=min(ea,eb))
    if hit: out.append(finding('operation_range_collision',SEVERITY_REJECT,p,b['operation_id'],a['operation_id']))
 return out
def apply_operations(repo,ops):
 result=dict(repo); source=dict(repo); out=[]
 for o in sorted(ops,key=lambda x:x['application_sequence']):
  p=o['path']; oid=o['operation_id']
  if o['operation']==OP_CREATE_FILE:
   if p in result: out.append(finding('create_path_already_exists',SEVERITY_REJECT,p,oid))
   else: result[p]=o['new_text']
   continue
  if p not in source or p not in result: out.append(finding('existing_target_missing',SEVERITY_REJECT,p,oid)); continue
  if o['file_digest']!=file_digest(source[p]): out.append(finding('source_file_digest_mismatch',SEVERITY_REJECT,p,oid)); continue
  lines=result[p].splitlines(keepends=True); a=o['application_start_line']; b=o['application_end_line']
  if b<a:
   k=a-1
   if not 0<=k<=len(lines): out.append(finding('insertion_line_out_of_range',SEVERITY_REJECT,p,oid)); continue
   lines[k:k]=o['new_text'].splitlines(keepends=True)
  else:
   if a<=0 or b<a or b>len(lines): out.append(finding('replacement_line_out_of_range',SEVERITY_REJECT,p,oid)); continue
   lines[a-1:b]=[] if o['operation']==OP_DELETE_SYMBOL else o['new_text'].splitlines(keepends=True)
  result[p]=''.join(lines)
  if not canonical_text(result[p]): out.append(finding('materialized_text_not_canonical',SEVERITY_REJECT,p,oid))
 return result,out
def _py_candidates(path,module,level):
 parts=list(PurePosixPath(path).parts[:-1]); trim=max(0,level-1)
 if trim>len(parts): return ()
 if trim: parts=parts[:-trim]
 if module: parts+=module.split('.')
 if not parts:return ()
 s='/'.join(parts); return s+'.py',s+'/__init__.py'
def _pycheck(p,repo,pol,inv):
 try: tree=ast.parse(repo[p])
 except SyntaxError as e:return [finding('python_parse_failed',SEVERITY_REPAIRABLE,p,detail=type(e).__name__)]
 roots={PurePosixPath(x).parts[0] for x in repo if x.endswith('.py')}; allowed=set(pol['allowed_external_python_modules'])|set(inv['python_external_modules']); out=[]
 for n in ast.walk(tree):
  vals=[(0,a.name) for a in n.names] if isinstance(n,ast.Import) else [(n.level,n.module or '')] if isinstance(n,ast.ImportFrom) else []
  for level,m in vals:
   root=m.split('.')[0] if m else ''; cand=_py_candidates(p,m,level)
   if level or root in roots:
    if pol['require_internal_python_import_resolution'] and not any(x in repo for x in cand): out.append(finding('internal_python_import_unresolved',SEVERITY_REPAIRABLE,p,detail=m))
   elif root not in sys.stdlib_module_names and root not in allowed: out.append(finding('external_python_dependency_unaccounted',SEVERITY_HOLD,p,detail=m))
 return out
def _leanmap(repo):
 out=set()
 for p in repo:
  if p.endswith('.lean'):
   q=p[:-5]; q=q[7:] if q.startswith('formal/') else q; out.add(q.replace('/','.'))
 return out
def _leancheck(p,repo,pol,inv):
 imports=[]; decl=[]
 for line in repo[p].splitlines():
  m=LIMPORT.match(line); imports+=([m.group(1)] if m else []); m=LDECL.match(line); decl+=([m.group(1)] if m else [])
 scrub=re.sub(r'"(?:\\.|[^"\\])*"','""',repo[p]); scrub='\n'.join(x.split('--',1)[0] for x in scrub.splitlines()); pairs={'(':')','[':']','{':'}'}; stack=[]; bal=True
 for c in scrub:
  if c in pairs:stack.append(pairs[c])
  elif c in pairs.values():
   if not stack or stack.pop()!=c:bal=False;break
 if stack:bal=False
 out=[]
 if pol['require_materialized_parse'] and not bal:out.append(finding('lean_lexical_structure_unbalanced',SEVERITY_REPAIRABLE,p))
 for x in sorted({x for x in decl if decl.count(x)>1}):out.append(finding('lean_duplicate_top_level_declaration',SEVERITY_REPAIRABLE,p,detail=x))
 mods=_leanmap(repo); roots={x.split('.')[0] for x in mods}; allowed=tuple(pol['allowed_external_lean_import_prefixes'])+tuple(inv['lean_external_import_prefixes'])
 for m in imports:
  if m in mods:continue
  if m.split('.')[0] in roots:
   if pol['require_internal_lean_import_resolution']:out.append(finding('internal_lean_import_unresolved',SEVERITY_REPAIRABLE,p,detail=m))
  elif not any(m==q or m.startswith(q+'.') for q in allowed):out.append(finding('external_lean_dependency_unaccounted',SEVERITY_HOLD,p,detail=m))
 return out
def static_findings(source,result,ops,pol,inv):
 out=[]; changed=sorted(p for p in set(source)|set(result) if source.get(p)!=result.get(p)); lang={o['path']:o['language'] for o in ops}
 for o in ops:
  for m in pol['forbidden_new_text_markers']:
   if m and m in o['new_text']:out.append(finding('forbidden_new_text_marker',SEVERITY_REPAIRABLE,o['path'],o['operation_id'],m))
  if source.get(o['path'])==result.get(o['path']):out.append(finding('operation_has_no_material_effect',SEVERITY_REPAIRABLE,o['path'],o['operation_id']))
 for p in changed:
  if lang.get(p)=='python':out+=_pycheck(p,result,pol,inv)
  elif lang.get(p)=='lean':out+=_leancheck(p,result,pol,inv)
 return out
def test_findings(changed,ir,req,cat,required):
 if not required:return []
 plans={p['test_plan_id']:p for p in cat['plans']}; refs=set(req['required_test_plan_ids'])|set(ir['test_plan_ids'])
 for o in ir['operations']:refs.update(o['test_plan_ids'])
 out=[finding('test_plan_missing_from_catalog',SEVERITY_REPAIRABLE,detail=x) for x in sorted(refs) if x not in plans]; avail=[plans[x] for x in sorted(refs) if x in plans]
 for p in changed:
  lang=next((o['language'] for o in ir['operations'] if o['path']==p),'')
  if not any(lang in q['languages'] and any(has_prefix(p,z) for z in q['covered_path_prefixes']) for q in avail):out.append(finding('changed_path_without_test_plan_coverage',SEVERITY_REPAIRABLE,p))
 return out
def disposition(fs):
 ss={x['severity'] for x in fs}; return DISPOSITION_REJECTED if SEVERITY_REJECT in ss else DISPOSITION_HOLD if SEVERITY_HOLD in ss else DISPOSITION_REPAIRABLE if SEVERITY_REPAIRABLE in ss else DISPOSITION_ADMISSIBLE
