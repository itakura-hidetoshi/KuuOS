"""Protocol integration fixtures, not real Lean/MCP certification."""
from __future__ import annotations
import hashlib,json,os,sys,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
from runtime import kuuos_codeai_memoryos_lean_repair_v0_1 as m
from scripts import kuuos_codeai_memoryos_lean_v0_1 as adapter

class AdapterTests(unittest.TestCase):
    def fixture(self,root,green=False):
        core=types.ModuleType('scripts.kuuos_v1104_codeai_four_cocycle_v1')
        gen=types.ModuleType('scripts.kuuos_v0_codeai_fixture')
        scan=types.ModuleType('scripts.check_kuuos_lean_mcp_fullsource_v1')
        for module in (core,gen):
            p=root/(module.__name__.split('.')[-1]+'.py');p.write_text('# fixture only\n');module.__file__=str(p)
        core.ROOT=root;core.OUT=root/'raw';core.MCP_OUT=root/'mcp'
        core.TARGET='formal/KUOS/Test.lean';core.MODULE='KUOS.Test';core.REPO='itakura-hidetoshi/KuuOS'
        core.require_event=lambda:('1'*40,'fixture','2'*40)
        core.require_pins=lambda root:None
        manifest=json.dumps({'packages':[{'name':'mathlib','rev':'5450b53e5ddc75d46418fabb605edbf36bd0beb6'}]})
        (root/'lake-manifest.json').write_text(manifest)
        (root/'lean-toolchain').write_text('leanprover/lean4:v4.30.0-rc2\n')
        scan.imports_of=lambda text:['Fixture']
        scan.declarations_of=lambda text,mod:[{'kind':'theorem','name_lexical':'Fixture.x','signature_sha256':'6'*64}]
        factory=lambda:{'fixture':'candidate'}
        def raw_main():
            proposals=core.proposals();core.OUT.mkdir();core.MCP_OUT.mkdir()
            log='\n' if green else 'file.lean:1:1: error: unsolved goals\n⊢ X\n'
            rows=[]
            for name,text in proposals.items():
                (core.OUT/(name+'.log')).write_text(log)
                rows.append({'variant':name,'candidate_blob':m.git_blob(text.encode()),'exit_code':0 if green else 1,'olean_exists':green,'log_sha256':hashlib.sha256(log.encode()).hexdigest(),'status':'SUCCESS' if green else 'FAILURE'})
            (core.OUT/'portfolio.json').write_text(json.dumps({'source_head':'1'*40,'source_tree':'2'*40,'source_restored':True,'candidates':rows}))
            (core.MCP_OUT/'receipt.json').write_text(json.dumps({
                'source_head':'1'*40,'candidate_count':1,
                'direct_lean_green':['fixture'] if green else [],
                'selected':'fixture' if green else None,
                'selected_blob':m.git_blob(b'candidate') if green else None,
                'mcp_success':green,'mcp_errors':0 if green else None,
                'second_direct_exit':0 if green else None,
                'second_direct_success':green,'source_restored':True
            }))
            return 0
        core.main=raw_main;core.proposals=factory
        def gen_main():core.proposals=factory;return core.main()
        gen.main=gen_main
        modules={x.__name__:x for x in (core,gen,scan)}
        bound=dict(repository=core.REPO,source_head='1'*40,source_tree='2'*40,target=core.TARGET,lean=(root/'lean-toolchain').read_text().strip(),mathlib='5450b53e5ddc75d46418fabb605edbf36bd0beb6',manifest_sha256=hashlib.sha256(manifest.encode()).hexdigest(),runner_sha256=hashlib.sha256(b'# fixture only\n'*2).hexdigest(),imports_sha256=m.digest(['Fixture']),signatures_sha256=m.digest([('theorem','Fixture.x','6'*64)]),flags=['-DwarningAsError=true','-Dweak.sorryAsError=true'])
        return core,gen,modules,bound

    def execute(self,green):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);history=root/'history';history.mkdir()
            core,gen,modules,bound=self.fixture(root,green)
            original=core.main
            with patch.dict(sys.modules,modules),patch.dict(os.environ,{'GITHUB_RUN_ID':'123'}):
                code=adapter.run(gen.__name__,history,root/'out')
            self.assertIs(core.main,original)
            report=json.loads((root/'out/receipt.json').read_text())
            rows=m.load(root/'out/observations')
            self.assertEqual(len(rows),1)
            self.assertEqual(rows[0]['binding'],bound)
            self.assertIs(report['independent_ci_certified'],False)
            return code,report

    def test_local_red_returns_failure_even_when_experiment_returns_zero(self):
        code,report=self.execute(False)
        self.assertEqual(code,4);self.assertEqual(report['status'],'LOCAL_UNCERTIFIED')

    def test_local_green_still_requires_independent_ci(self):
        code,report=self.execute(True)
        self.assertEqual(code,0);self.assertEqual(report['status'],'LOCAL_GREEN_REQUIRES_INDEPENDENT_CI')

    def test_exact_repeat_never_calls_lean_and_retains_reason(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);history=root/'history';history.mkdir()
            core,gen,modules,bound=self.fixture(root)
            m.append(history,m.observe(bound,candidate_blob=m.git_blob(b'candidate'),variant='old',diagnostic='error: unsolved goals',exit_code=1,olean_exists=False,evidence={'run_id':1}))
            with patch.dict(sys.modules,modules),patch.dict(os.environ,{'GITHUB_RUN_ID':'123'}):
                with self.assertRaises(ValueError):adapter.run(gen.__name__,history,root/'out')
            self.assertFalse(core.OUT.exists())
            report=json.loads((root/'out/receipt.json').read_text())
            self.assertEqual(report['status'],'REGENERATE_REQUIRED')
            self.assertEqual(report['decisions']['fixture']['decision'],'BLOCK_EXACT_FAILED')

    def test_guided_factory_receives_memory_before_generation(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);history=root/'history';history.mkdir()
            core,gen,modules,bound=self.fixture(root)
            seen=[]
            def guided(advice):
                seen.append(advice);self.assertTrue((root/'out/before_generation.json').exists())
                return {'fixture':'candidate'}
            gen.candidates_with_memory=guided
            with patch.dict(sys.modules,modules),patch.dict(os.environ,{'GITHUB_RUN_ID':'123'}):
                adapter.run(gen.__name__,history,root/'out')
            self.assertEqual(len(seen),1);self.assertFalse(seen[0]['proof_authority'])

if __name__=='__main__':unittest.main()
