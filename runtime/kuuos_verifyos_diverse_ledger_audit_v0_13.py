"""Independent finite frozen-registry audit, plus v0.12 agreement gate.
No import or execution of the inherited integrity/scope gate code in audit().
"""
from __future__ import annotations
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

SCHEMA = 'kuuos.verifyos.diverse-ledger-audit.v0.13'
REPO = 'itakura-hidetoshi/KuuOS'
PINS = {'lean':'v4.30.0-rc2','mathlib':'5450b53e5ddc75d46418fabb605edbf36bd0beb6'}
REGISTRY = 'base/kuuos_continuation_20261128_v15.json'
BASE = ('base/KuuOS_native_GPT_continuity_v15.md','base/initial_checks_20261128_v15.json',REGISTRY,'base/kuuos_inheritance_gate_v15.py')
GATES = ('gates/kuuos_inheritance_gate_v16.py','gates/kuuos_scope_guard_v16_1.py')
BOUNDARY = {'full_gate_equivalence_proved':False,'arbitrary_ledger_supported':False,
            'independent_organization_verified':False,'external_truth_verified':False,
            'proof_authority':False,'action_authority':False,'current_at_delivery_verified':False}
ERRORS = (ValueError,TypeError,KeyError,AttributeError,IndexError,OverflowError,RecursionError,OSError)


def need(ok, reason):
    if not ok: raise ValueError(reason)


def canonical(x):
    return (json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()


def sha(raw): return hashlib.sha256(raw).hexdigest()


def hexd(x,n): return type(x) is str and re.fullmatch('[0-9a-f]{%d}'%n,x) is not None


def decode(raw):
    def pairs(items):
        out={}
        for k,v in items:
            need(k not in out,'DUPLICATE_KEY'); out[k]=v
        return out
    return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))


def evidence(x): return type(x) is list and bool(x) and all(type(y) is str and y.strip() for y in x)


def scope_decision(review,rules):
    if review.get('schema')!='kuuos.native-gpt.scope-review.v16.1': return 'HOLD_SCOPE_SCHEMA'
    identity=review.get('rule_identity')
    if type(identity) is not str or identity not in rules: return 'HOLD_UNKNOWN_RULE'
    rule=rules[identity]
    if rule.get('tier') not in ('A','B'): return 'HOLD_UNCERTIFIED_TIER'
    source=rule['source']; scope=rule['scope']
    expected={'rule_sha256':sha(canonical(rule)),'source_head':source['source_head'],'blob':source['blob'],'scope':scope,'pins':PINS}
    if review.get('binding')!=expected: return 'HOLD_RULE_BINDING_DRIFT'
    obs=review.get('observed')
    if type(obs) is not dict: return 'HOLD_CONTEXT_NO_DATA'
    if any(obs.get(k)!=expected[k] for k in ('pins','source_head','blob')): return 'HOLD_SOURCE_OR_PIN_DRIFT'
    if obs.get('scope')!=scope or obs.get('scope_status')!='MATCH': return 'HOLD_CONTEXT_CHANGED_OR_UNCONFIRMED'
    if not all(evidence(obs.get(k)) for k in ('source_evidence','scope_evidence')): return 'HOLD_CONTEXT_EVIDENCE_MISSING'
    if obs.get('exclusion_status')!='CLEAR' or not evidence(obs.get('exclusion_evidence')): return 'HOLD_EXCLUSION_CHANGED_OR_UNCONFIRMED'
    checks=obs.get('premise_checks')
    if type(checks) is not list or any(type(x) is not dict for x in checks) or [x.get('premise') for x in checks]!=rule['premises']: return 'HOLD_PREMISE_INVENTORY'
    if not all(x.get('status')=='SATISFIED' and evidence(x.get('evidence')) for x in checks): return 'HOLD_PREMISE_CHANGED_OR_UNCONFIRMED'
    return 'CONDITIONAL_REUSE_CANDIDATE_ONLY'


def materialize(root,seq,inventory):
    need(type(seq) is int and 0<=seq<=128,'PROFILE_SEQUENCE_LIMIT')
    need(type(inventory) is dict,'INVENTORY_REQUIRED')
    names=set(BASE+GATES)|{f'ledger/{i:012d}.json' for i in range(seq+1)}
    need(set(inventory)==names and all(hexd(x,64) for x in inventory.values()),'EXACT_INVENTORY_REQUIRED')
    root=Path(root); need(root.is_dir() and not root.is_symlink(),'UNSAFE_ROOT')
    for group in ('base','gates','ledger'):
        d=root/group; need(d.is_dir() and not d.is_symlink(),'UNSAFE_DIRECTORY')
        need({group+'/'+x.name for x in d.iterdir()}=={x for x in names if x.startswith(group+'/')},'FILE_SET_MISMATCH')
    files={}
    for name in sorted(names):
        path=root/name; need(path.is_file() and not path.is_symlink(),'UNSAFE_FILE')
        with path.open('rb') as handle: raw=handle.read(8*1024*1024+1)
        need(len(raw)<=8*1024*1024 and sha(raw)==inventory[name],'INPUT_HASH_OR_SIZE_MISMATCH')
        files[name]=raw
    return files


def audit(root,request,inventory):
    """Reconstruct both outputs for frozen base rules and observational-only events."""
    out={'schema':SCHEMA,'status':'HOLD','reason':None,**BOUNDARY}
    try:
        seq=request['seq']; tip=request['tip']; need(hexd(tip,64),'TIP_REQUIRED')
        files=materialize(root,seq,inventory)
        need(set(request['expected_hashes'])=={REGISTRY,*GATES} and all(inventory[k]==x for k,x in request['expected_hashes'].items()),'REQUEST_PIN_MISMATCH')
        base=decode(files[REGISTRY]); need(base['schema']=='kuuos.native-gpt.continuity.v15' and base['repository']==REPO and base['pins']==PINS,'BASE_SCOPE')
        rules={x['identity']:x for x in base['rules']}; need(len(base['rules'])==len(rules)==10,'BASE_RULE_COUNT')
        need(all(type(x) is str and x for x in rules),'BASE_RULE_IDENTITY')
        ck=base['checkpoints']; marks={k:ck[k] for k in ('main_observed','main_reported_substantive','research_observed_head')}
        need(all(hexd(x,40) for x in marks.values()),'BASE_WATERMARK_SCHEMA')
        certs=set(ck['research_scoped_verified']); need(all(hexd(x,40) for x in certs),'BASE_CERT_SCHEMA')
        parent='0'*64; runs=set(); obstructions=set(); counts={'candidate':0,'held':0,'no_use':0}; decisions=[]
        for i in range(seq+1):
            raw=files[f'ledger/{i:012d}.json']; event=decode(raw)
            need(raw==canonical(event),'NONCANONICAL_EVENT')
            need(event['schema']=='kuuos.native-gpt.ledger.v16' and event['repository']==REPO and event['pins']==PINS and event['base_registry_sha256']==inventory[REGISTRY],'EVENT_SCOPE')
            need(type(event['seq']) is int and event['seq']==i and event['parent_sha256']==parent and event['kind']==('GENESIS' if i==0 else 'DAILY_RUN'),'CHAIN_LINK')
            run=event['run_id']; need(type(run) is str and run and run not in runs,'RUN_ID'); runs.add(run)
            need(datetime.fromisoformat(event['observed_at']).tzinfo is not None,'TIMEZONE')
            need(event['proof_authority'] is False and event['action_authority'] is False and type(event['pb16_executed']) is int and event['pb16_executed']==0,'AUTHORITY_ESCALATION')
            for k in ('new_rules','withdrawals','research_certificates','notification_intents'):
                need(event[k]==[],'OUTSIDE_FROZEN_REGISTRY_PROFILE:'+k)
            need(type(event['observation']) is dict and type(event['backlog_notes']) is list and all(type(x) is str and x.strip() for x in event['backlog_notes']),'EVENT_STRUCTURE')
            need(type(event['obstructions']) is list,'OBSTRUCTION_INVENTORY')
            for item in event['obstructions']:
                oid=item['id']; need(type(oid) is str and oid and oid not in obstructions and item['scope'] and item['reason'] and item['kind'] in ('PROVED_NO_GO','OPERATIONAL_HOLD','RETRACTION'),'OBSTRUCTION_RECORD')
                need(item['kind']!='PROVED_NO_GO' or item.get('proof_reference'),'NO_GO_REFERENCE_REQUIRED'); obstructions.add(oid)
            need(type(event['transitions']) is list and (i>0 or not event['transitions']),'TRANSITION_INVENTORY')
            touched=set()
            for tr in event['transitions']:
                k=tr['key']; need(k in ('main_observed','research_observed_head') and k not in touched,'OUTSIDE_OBSERVATIONAL_TRANSITION_PROFILE'); touched.add(k)
                old,new=marks[k],tr['to']; cmp=tr['compare']
                need(tr['from']==old and hexd(new,40) and cmp['base']==old and cmp['head']==new and cmp['status']=='ahead' and type(cmp['ahead_by']) is int and cmp['ahead_by']>0 and type(cmp['behind_by']) is int and cmp['behind_by']==0 and cmp['repository']==REPO and cmp['source_url'].startswith('https://github.com/'+REPO+'/compare/'),'TRANSITION_BINDING')
                marks[k]=new
            need(type(event['checks']) is list,'CHECK_INVENTORY')
            if i:
                checks=event['checks']; ids=[x['id'] for x in checks]
                need(type(checks) is list and len(ids)==len(set(ids)) and {'T1','T2','T3','T4','T5'}<=set(ids),'CHECK_INVENTORY')
                for x in checks:
                    need(x['status'] in ('PASS','FAIL','NO_DATA') and x['kind'] in ('SELF_CHECK','LOCAL_FIXTURE','NO_DATA') and 'actual' in x and 'expected' in x,'CHECK_SCHEMA')
                    need(x['status']!='PASS' or (x['kind']!='NO_DATA' and canonical(x['actual'])==canonical(x['expected'])),'FALSE_PASS')
                reviews=event['scope_reviews']; need(type(reviews) is list,'REVIEW_INVENTORY')
                if not reviews:
                    need(type(event.get('scope_no_use_reason')) is str and event['scope_no_use_reason'].strip(),'NO_USE_REASON'); counts['no_use']+=1
                seen=set()
                for review in reviews:
                    rid=review['review_id']; need(type(rid) is str and rid.strip() and rid not in seen,'REVIEW_ID'); seen.add(rid)
                    decision=scope_decision(review,rules); candidate=decision=='CONDITIONAL_REUSE_CANDIDATE_ONLY'
                    decisions.append({'seq':i,'review_id':rid,'recorded':review.get('status'),'recomputed':decision})
                    need(review['status']==decision,'SCOPE_DECISION_DISAGREEMENT')
                    need(review['proof_authority'] is False and review['action_authority'] is False and review['disposition']==('CANDIDATE_ONLY' if candidate else 'HOLD'),'REVIEW_AUTHORITY')
                    need(review['evidence_kind'] in ('LOCAL_FIXTURE','SELF_CHECK','OBSERVED_EVIDENCE','NO_DATA') and (not candidate or review['evidence_kind']!='NO_DATA'),'REVIEW_EVIDENCE_KIND')
                    counts['candidate' if candidate else 'held']+=1
            parent=sha(raw)
        need(parent==tip,'TRUSTED_TIP_MISMATCH')
        need(materialize(root,seq,inventory)==files,'INPUT_DRIFT')
        common={'seq':seq,'tip_sha256':tip,'proof_authority':False,'action_authority':False}
        outputs=[{'status':'PASS_INTEGRITY_ONLY',**common,'rule_count':len(rules),'withdrawn_count':0,'watermarks':marks,'notification_intent_count':0,'obstruction_count':len(obstructions),'research_certificate_count':len(certs),'pb16_executed':0}, {'status':'PASS_SCOPE_RECORDS_ONLY',**common,'reviews':counts}]
        out.update(status='FROZEN_PROFILE_RECONSTRUCTED_ONLY',outputs=outputs,review_decisions=decisions,inventory_sha256=sha(canonical(inventory)))
    except ERRORS as exc:
        out['reason']=str(exc) if type(exc) is ValueError else 'AUDIT_INPUT_INVALID'
        if 'decisions' in locals(): out['review_decisions']=decisions
    return out


def verify_diverse(snapshot,**pair_inputs):
    """Direct audit must agree with both admitted reports; no majority override."""
    from runtime import kuuos_verifyos_execution_witness_v0_12 as witness
    pair=witness.verify_pair(**pair_inputs)
    out={'schema':SCHEMA,'status':'HOLD','reason':'PAIR_NOT_ADMITTED','pair':pair,**witness.BOUNDARY,**BOUNDARY}
    if pair['status']!='SEPARATE_KEY_EXECUTION_REPORTS_AGREE_ONLY': return out
    independent=audit(snapshot,pair_inputs['request'],pair_inputs['policy']['inventory']); out['audit']=independent
    if independent['status']!='FROZEN_PROFILE_RECONSTRUCTED_ONLY':
        out['reason']='DIVERSE_AUDIT_NOT_ADMITTED'; return out
    differences=[]
    try:
        for label in ('primary_raw','witness_raw'):
            actual=[decode(x['stdout'].encode()) for x in decode(pair_inputs[label])['receipt']['processes']]
            need(len(actual)==len(independent['outputs']),'OUTPUT_COUNT_MISMATCH')
            for i,(expected,observed) in enumerate(zip(independent['outputs'],actual)):
                if canonical(expected)!=canonical(observed): differences.append({'report':label,'gate':GATES[i],'expected':expected,'observed':observed})
        out['differences']=differences
        if differences: out['reason']='COMMON_OR_LOCAL_OUTPUT_DISAGREEMENT'; return out
        out.update(status='DIVERSE_FROZEN_PROFILE_AGREEMENT_ONLY',reason=None,answer_status=pair['answer_status'])
    except ERRORS: out['reason']='DIVERSE_COMPARISON_INVALID'
    return out
