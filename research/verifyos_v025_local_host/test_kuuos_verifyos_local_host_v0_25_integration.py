"""Actual pinned Lean plus separate-process local IPC; synthetic fixtures only.
Stage in tests/ beside the exact v0.24 integration fixture. No mocked Lean.
"""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
from runtime import kuuos_verifyos_local_host_v0_25 as v
import test_kuuos_verifyos_mcp_bridge_v0_24_integration as fixture

m=v.m


class ActualLocalHostIntegration(fixture.ActualMcpBridgeIntegration):
    def run_fixture(self,mode,missing_lean=False):
        root,args=self.fixture.pair(mode)
        req=args['request']; question=args['seed']['question']; b=fixture.predecessor.b
        inputs=(question,b.canonical(req),b.canonical(args['context']))
        self.assertEqual(inputs[1],m.upstream_canonical(req));self.assertEqual(inputs[2],m.upstream_canonical(args['context']))
        self.assertIsNotNone(self.client.select_turn(*inputs))
        self.policy=m.HostPolicy(m.g.sha(b'synthetic target'),req['seq'],req['tip'],tuple(sorted(req['expected_hashes'].items())),self.lean_sha)
        self.bridge=m.McpBridge(self.host,self.policy,self.verifier,self.receipt_key)
        gate=v.LocalGate(self.bridge,self.policy,self.receipt_key.public_key());self.addCleanup(gate.close)
        armed=gate.arm(question,snapshot=Path(root).absolute(),lean=self.dir/'missing' if missing_lean else self.lean,pair_inputs=args)
        self.assertIsNotNone(armed);self.binding,event=armed;self.client.notify(event)
        self.tool_args={'challenge':self.binding.challenge.nonce}
        socket_dir=self.dir/'ipc';socket_dir.mkdir(mode=0o700);path=socket_dir/'gate.sock'
        # The child receives only the socket path and public test challenge.
        child_code=('import json,socket,sys\n'
                    'with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as s:\n'
                    ' s.settimeout(360); s.connect(sys.argv[1]); s.sendall(sys.argv[2].encode()+b"\\n"); print(s.makefile("rb").readline().decode(),end="")\n')
        with v.UnixGateServer(path,gate) as server,ThreadPoolExecutor(max_workers=1) as pool:
            job=pool.submit(server.serve_once)
            child=subprocess.run([sys.executable,'-c',child_code,str(path),json.dumps(self.tool_args)],capture_output=True,check=True,timeout=370)
            job.result(timeout=10)
            transport=json.loads(child.stdout)
            replay=pool.submit(server.serve_once)
            rejected=v.invoke_local(path,self.tool_args)
            replay.result(timeout=10)
        self.assertEqual(transport['production_status'],'HOLD');self.assertEqual(transport['claims'],[])
        self.assertEqual((rejected['status'],rejected['production_status'],rejected['receipt']),('HOLD','HOLD',None))
        if mode=='correct' and not missing_lean:
            self.assertEqual(transport['status'],'SYNTHETIC_RECEIPT_MATCHED_ONLY',transport)
            response=transport['receipt']
        else:
            self.assertEqual((transport['status'],transport['receipt']),('HOLD',None))
            response=transport
        nonce=self.client.request_checkpoint();self.assertIsNotNone(nonce)
        if not self.client.accept_checkpoint(nonce,self.host.checkpoint(nonce)):
            return response,self.client.current(),inputs
        request,wire=self.client.request();shown=self.client.accept(request,self.host.present(wire))
        return response,shown,inputs
