"""Local transport for the unchanged synthetic-only v0.24 bridge.
Not a registered MCP server, production verifier, or ChatGPT display hook.
Only trusted in-process host code may arm. Linux same-UID Unix socket transport.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import socket
import stat
import struct
import threading
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
if __package__:
    from . import kuuos_verifyos_mcp_bridge_v0_24 as m
else:
    import kuuos_verifyos_mcp_bridge_v0_24 as m

MAX_REQUEST = 1024
MAX_RESPONSE = 1024 * 1024
READ_SECONDS = 2.0
SCHEMA = 'kuuos.verifyos.local-host.v0.25'
HEX64 = re.compile(r'[0-9a-f]{64}\Z')


def hold(reason):
    return {'schema': SCHEMA, 'status': 'HOLD', 'reason': reason,
            'production_status': 'HOLD', 'claims': [], 'receipt': None}


def decode_request(raw):
    """Exactly one JSON object; no duplicate keys, extra fields or nonfinite values."""
    if type(raw) is not bytes or not (0 < len(raw) <= MAX_REQUEST):
        raise ValueError('REQUEST_SIZE')
    def unique(pairs):
        out = {}
        for k, v in pairs:
            if k in out: raise ValueError('DUPLICATE_KEY')
            out[k] = v
        return out
    def bad(_): raise ValueError('NONFINITE')
    obj = json.loads(raw.decode('utf-8', errors='strict'), object_pairs_hook=unique, parse_constant=bad)
    if type(obj) is not dict or set(obj) != {'challenge'} or type(obj['challenge']) is not str or not HEX64.fullmatch(obj['challenge']):
        raise ValueError('REQUEST_SCHEMA')
    return obj


class LocalGate:
    """Trusted host object; no network path to arm or choose any policy/input.
    A generation change during execution discards that execution's response.
    A returned receipt is snapshot evidence only, not a current display grant.
    """
    def __init__(self, bridge, policy, receipt_public_key):
        if type(bridge) is not m.McpBridge or type(policy) is not m.HostPolicy or not isinstance(receipt_public_key, Ed25519PublicKey):
            raise ValueError('HOST_CONFIG')
        policy.validate()  # v0.24 expressly prohibits production.
        self._bridge, self._policy, self._key = bridge, policy, receipt_public_key
        self._lock = threading.Lock()
        self._pending = None
        self._generation = 0
        self._closed = False

    def arm(self, question, *, snapshot, lean, pair_inputs):
        with self._lock:
            if self._closed: return None
            self._generation += 1
            self._pending = None
            try:
                result = self._bridge.arm(question, snapshot=snapshot, lean=lean, pair_inputs=pair_inputs)
                if result is not None:
                    binding, _ = result
                    binding.validate()
                    self._pending = (self._generation, binding)
                return result
            except Exception:
                self._bridge.invalidate()
                return None

    def invalidate(self):
        with self._lock:
            self._generation += 1
            self._pending = None
            self._bridge.invalidate()

    def close(self):
        with self._lock:
            self._closed = True
            self._generation += 1
            self._pending = None
            self._bridge.invalidate()

    def dispatch(self, raw):
        try: req = decode_request(raw)
        except (ValueError, TypeError, RecursionError): return hold('REQUEST_INVALID')
        with self._lock:
            pending = self._pending
            if self._closed or pending is None or req['challenge'] != pending[1].challenge.nonce:
                return hold('NO_MATCHING_HOST_CHALLENGE')
            self._pending = None  # consume before execution, even on failure
        generation, binding = pending
        try:
            result = self._bridge.handle(req)
            checked = m.inspect_receipt(result, self._key, binding, self._policy)
            accepted = (checked.get('status') == 'SYNTHETIC_RECEIPT_SIGNATURE_MATCHED_ONLY'
                        and checked.get('production_status') == 'HOLD')
        except Exception:
            accepted = False
        with self._lock:
            if self._closed or generation != self._generation:
                return hold('STALE_EXECUTION')
            if not accepted:
                self._bridge.invalidate()
                return hold('EXECUTION_OR_RECEIPT_UNAVAILABLE')
            return {'schema': SCHEMA, 'status': 'SYNTHETIC_RECEIPT_MATCHED_ONLY',
                    'production_status': 'HOLD', 'claims': [], 'receipt': result}


def read_line(conn, max_bytes, seconds=READ_SECONDS):
    """Absolute receive deadline; exactly one LF-delimited request per socket."""
    end = time.monotonic() + seconds
    data = bytearray()
    while True:
        remaining = end - time.monotonic()
        if remaining <= 0: raise TimeoutError('READ_DEADLINE')
        conn.settimeout(remaining)
        chunk = conn.recv(min(4096, max_bytes + 1 - len(data)))
        if not chunk: raise ValueError('INCOMPLETE_LINE')
        data.extend(chunk)
        if len(data) > max_bytes: raise ValueError('FRAME_SIZE')
        if b'\n' in data:
            if data.count(b'\n') != 1 or data[-1] != 10: raise ValueError('EXTRA_FRAME')
            return bytes(data[:-1])


class UnixGateServer:
    """Linux local-only same-UID IPC. No TCP, no secret or raw ledger transfer.
    Same UID is one trust domain, not independent organizational identity.
    The parent directory must be pre-provisioned, owned, and mode 0700.
    """
    def __init__(self, path, gate):
        if type(gate) is not LocalGate or not hasattr(socket, 'SO_PEERCRED'):
            raise ValueError('LOCAL_LINUX_HOST_REQUIRED')
        path = Path(path)
        if not path.is_absolute() or path.parent.resolve(strict=True) != path.parent:
            raise ValueError('SOCKET_PATH')
        parent = path.parent.stat()
        if parent.st_uid != os.geteuid() or stat.S_IMODE(parent.st_mode) != 0o700 or not stat.S_ISDIR(parent.st_mode):
            raise ValueError('PRIVATE_SOCKET_DIRECTORY_REQUIRED')
        if os.path.lexists(path): raise ValueError('SOCKET_EXISTS')
        self.path, self.gate = path, gate
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._identity = None
        try:
            self.sock.bind(str(path))
            st = path.lstat(); self._identity = (st.st_dev, st.st_ino)
            os.chmod(path, 0o600)
            self.sock.listen(8)
        except BaseException:
            self.close(); raise

    def serve_once(self, accept_seconds=3.0):
        self.sock.settimeout(accept_seconds)
        conn, _ = self.sock.accept()
        with conn:
            try:
                credentials = conn.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, struct.calcsize('3i'))
                _, uid, _ = struct.unpack('3i', credentials)
                if uid != os.geteuid(): result = hold('PEER_UID_MISMATCH')
                else: result = self.gate.dispatch(read_line(conn, MAX_REQUEST))
            except (OSError, ValueError, TypeError, RecursionError): result = hold('TRANSPORT_INVALID')
            raw = json.dumps(result, sort_keys=True, separators=(',', ':'), allow_nan=False).encode() + b'\n'
            if len(raw) > MAX_RESPONSE:
                raw = json.dumps(hold('RESPONSE_SIZE'), separators=(',', ':')).encode() + b'\n'
            try:
                conn.settimeout(READ_SECONDS)
                conn.sendall(raw)
            except OSError:
                pass  # consumed challenge stays consumed; never retry automatically

    def close(self):
        self.sock.close()
        if self._identity is not None:
            try:
                st = self.path.lstat()
                if stat.S_ISSOCK(st.st_mode) and (st.st_dev, st.st_ino) == self._identity:
                    self.path.unlink()
            except FileNotFoundError: pass

    def __enter__(self): return self
    def __exit__(self, *exc): self.close()


def invoke_local(path, request, timeout=360.0):
    """Local client helper, no verification or display authority of its own."""
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as conn:
        conn.settimeout(READ_SECONDS)
        conn.connect(str(path))
        conn.sendall(json.dumps(request, separators=(',', ':'), allow_nan=False).encode() + b'\n')
        return json.loads(read_line(conn, MAX_RESPONSE, timeout))
