import TypedProjection
import Lean.Data.Json.Parser
import Lean.Data.Json.Printer

/-!
# VerifyOS v0.16: bounded strict JSON input to the typed projection

The syntax profile rejects decimal/exponent tokens and Unicode escapes
rather than normalizing them. Literal Unicode and the usual short JSON
escapes are supported. Parsing is bounded and duplicate object keys are
rejected before building a tree map. This is a syntax/extraction bridge,
not a proof of all JSON parsing or external receipt admission.
-/

namespace KUOS.VerifyOS.JsonProjectionV0_16

open KUOS.VerifyOS.TypedProjectionV0_15
open KUOS.VerifyOS.MethodSoundCoverageV0_14
open Std.Internal.Parsec Std.Internal.Parsec.String
set_option autoImplicit false

def uniqueInsert (k : String) (j : Lean.Json)
    (pairs : List (String × Lean.Json)) : Option (List (String × Lean.Json)) :=
  if pairs.any (fun p => p.1 == k) then none else some ((k,j) :: pairs)

theorem duplicate_insert_rejected (k : String) (j : Lean.Json)
    (pairs : List (String × Lean.Json))
    (h : pairs.any (fun p => p.1 == k) = true) :
    uniqueInsert k j pairs = none := by
  simp [uniqueInsert, h]

theorem fresh_insert_preserves_entries (k : String) (j : Lean.Json)
    (pairs : List (String × Lean.Json))
    (h : pairs.any (fun p => p.1 == k) = false) :
    uniqueInsert k j pairs = some ((k,j) :: pairs) := by
  simp [uniqueInsert, h]

/-- Deliberately conservative: refuse Unicode-escape spelling in this profile,
including that spelling within escaped strings. Do not replace surrogates. -/
def noUnicodeEscape : List Char → Bool
  | '\\' :: 'u' :: _ => false
  | _ :: xs => noUnicodeEscape xs
  | [] => true

def isDigit (c : Char) : Bool := '0' <= c && c <= '9'

def digits : Nat → Nat → Parser Nat
  | 0, a => do
    if ← isEof then return a
    let c ← peek!
    if isDigit c then fail "integer digit limit" else return a
  | n+1, a => do
    if ← isEof then return a
    let c ← peek!
    if isDigit c then
      skip
      digits n (10*a + (c.val - '0'.val).toNat)
    else
      return a

def strictNumber : Parser Lean.Json := do
  let sign ← Lean.Json.Parser.numSign
  let c ← peek!
  if !isDigit c then fail "integer expected"
  let n ← if c == '0' then do
      skip
      pure 0
    else digits 64 0
  if !(← isEof) then
    let next ← peek!
    if next == '.' || next == 'e' || next == 'E' then
      fail "noninteger spelling outside profile"
  ws
  return .num ⟨sign * Int.ofNat n, 0⟩

def quoted : Parser String := do
  Lean.Json.Parser.lookahead (fun c => c == '"') "quoted string"
  skip
  let s ← Lean.Json.Parser.str
  ws
  return s

/- Every recursive call consumes a unit of explicit fuel. The bounded object
parser retains the member list until uniqueness is checked. -/
mutual
  def parseValue : Nat → Parser Lean.Json
    | 0 => fail "value limit"
    | n+1 => do
      let c ← peek!
      if c == '{' then
        skip; ws
        if (← peek!) == '}' then
          skip; ws
          return Lean.Json.mkObj []
        else
          return Lean.Json.mkObj (← parseObject n [])
      else if c == '[' then
        skip; ws
        if (← peek!) == ']' then
          skip; ws
          return .arr #[]
        else
          return .arr (← parseArray n #[])
      else if c == '"' then
        return .str (← quoted)
      else if c == 't' then
        skipString "true"; ws
        return .bool true
      else if c == 'f' then
        skipString "false"; ws
        return .bool false
      else if c == 'n' then
        skipString "null"; ws
        return .null
      else if c == '-' || isDigit c then
        strictNumber
      else
        fail "unexpected JSON token"

  def parseObject : Nat → List (String × Lean.Json) → Parser (List (String × Lean.Json))
    | 0, _ => fail "object member limit"
    | n+1, pairs => do
      let key ← quoted
      Lean.Json.Parser.lookahead (fun c => c == ':') "colon"
      skip; ws
      let val ← parseValue n
      let some next := uniqueInsert key val pairs | fail "duplicate JSON key"
      let c ← any
      if c == '}' then
        ws
        return next
      else if c == ',' then
        ws
        parseObject n next
      else
        fail "object delimiter"

  def parseArray : Nat → Array Lean.Json → Parser (Array Lean.Json)
    | 0, _ => fail "array member limit"
    | n+1, acc => do
      let item ← parseValue n
      let next := acc.push item
      let c ← any
      if c == ']' then
        ws
        return next
      else if c == ',' then
        ws
        parseArray n next
      else
        fail "array delimiter"
end

def strictJson (s : String) : Except String Lean.Json :=
  if s.utf8ByteSize > 262144 then .error "JSON byte limit"
  else if !noUnicodeEscape s.toList then .error "Unicode escape outside profile"
  else Parser.run (do ws; let j ← parseValue 512; eof; return j) s

def decodeValue : Lean.Json → Option Value
  | .str s => some (.text s)
  | .num ⟨Int.ofNat n, 0⟩ => some (.nat n)
  | _ => none

theorem decode_natural (n : Nat) :
    decodeValue (.num ⟨Int.ofNat n, 0⟩) = some (.nat n) := rfl

theorem decode_string (s : String) :
    decodeValue (.str s) = some (.text s) := rfl

theorem decode_bool_hold (v : Bool) : decodeValue (.bool v) = none := rfl

theorem decode_null_hold : decodeValue .null = none := rfl

theorem decode_negative_hold (n e : Nat) :
    decodeValue (.num ⟨Int.negSucc n, e⟩) = none := rfl

theorem decode_fraction_hold (n e : Nat) :
    decodeValue (.num ⟨Int.ofNat n, e+1⟩) = none := rfl

def lookupPath (j : Lean.Json) : List String → Option Lean.Json
  | [] => some j
  | key :: ks =>
    match (j.getObjVal? key).toOption with
    | none => none
    | some v => lookupPath v ks

structure GateView where
  integrity : Lean.Json
  scope : Lean.Json
  integrityProcess : Lean.Json
  scopeProcess : Lean.Json

/-- Fixed v0.3 field registry; no input-supplied JSON paths. -/
def jsonField (g : GateView) : Claim → Option Lean.Json
  | .integrity_status => lookupPath g.integrity ["status"]
  | .scope_status => lookupPath g.scope ["status"]
  | .integrity_exit_code => lookupPath g.integrityProcess ["exit_code"]
  | .scope_exit_code => lookupPath g.scopeProcess ["exit_code"]
  | .snapshot_seq => lookupPath g.integrity ["seq"]
  | .snapshot_tip => lookupPath g.integrity ["tip_sha256"]
  | .rule_count => lookupPath g.integrity ["rule_count"]
  | .withdrawn_count => lookupPath g.integrity ["withdrawn_count"]
  | .obstruction_count => lookupPath g.integrity ["obstruction_count"]
  | .research_certificate_count => lookupPath g.integrity ["research_certificate_count"]
  | .scope_candidate_count => lookupPath g.scope ["reviews","candidate"]
  | .scope_held_count => lookupPath g.scope ["reviews","held"]
  | .scope_no_use_count => lookupPath g.scope ["reviews","no_use"]
  | .action_permission | .current_tip | .external_truth | .lean_proof | .new_context_validity => none

def decodedRaw (g : GateView) (x : Claim) : Option Value :=
  (jsonField g x).bind decodeValue

theorem decoded_field_present (g : GateView) (x : Claim) (j : Lean.Json)
    (h : jsonField g x = some j) : decodedRaw g x = decodeValue j := by
  simp [decodedRaw,h]

theorem decoded_field_missing (g : GateView) (x : Claim)
    (h : jsonField g x = none) : decodedRaw g x = none := by
  simp [decodedRaw,h]

theorem decoded_raw_iff (g : GateView) (x : Claim) (y : Value) :
    decodedRaw g x = some y ↔
      ∃ j, jsonField g x = some j ∧ decodeValue j = some y := by
  constructor
  · intro h
    cases hf : jsonField g x with
    | none =>
      rw [decoded_field_missing g x hf] at h
      cases h
    | some j =>
      exact ⟨j, rfl, (decoded_field_present g x j hf).symm.trans h⟩
  · rintro ⟨j, hj, hy⟩
    exact (decoded_field_present g x j hj).trans hy

def receiptView (g : GateView) (admitted : Bool) (source : SnapshotContext) : ReceiptView :=
  ⟨admitted, source, decodedRaw g⟩

theorem observed_iff_json_field (g : GateView) (admitted : Bool)
    (source ctx : SnapshotContext) (x : Claim) (y : Value) :
    observed (receiptView g admitted source) ctx x = some y ↔
      admitted = true ∧ source = ctx ∧ FieldValid ctx.tip (kind x) y ∧
        ∃ j, jsonField g x = some j ∧ decodeValue j = some y := by
  constructor
  · intro h
    have hv := (observed_iff_sourceValid (receiptView g admitted source) ctx x y).1 h
    exact ⟨hv.1,hv.2.1,hv.2.2.2,(decoded_raw_iff g x y).1 hv.2.2.1⟩
  · rintro ⟨ha,hc,hv,hj⟩
    exact (observed_iff_sourceValid (receiptView g admitted source) ctx x y).2
      ⟨ha,hc,(decoded_raw_iff g x y).2 hj,hv⟩

theorem missing_field_hold (g : GateView) (admitted : Bool)
    (source ctx : SnapshotContext) (x : Claim)
    (h : jsonField g x = none) :
    observed (receiptView g admitted source) ctx x = none := by
  cases ho : observed (receiptView g admitted source) ctx x with
  | none => rfl
  | some y =>
    obtain ⟨_,_,_,j,hj,_⟩ := (observed_iff_json_field g admitted source ctx x y).1 ho
    rw [h] at hj
    cases hj

theorem json_projection_forced (g : GateView) (admitted : Bool)
    (source ctx : SnapshotContext) (x : Claim) (y : Value) :
    observed (receiptView g admitted source) ctx x = some y ↔
      Forced (methodAdmission (receiptView g admitted source)) methodScope
        (methodReport (receiptView g admitted source)) ctx x y :=
  observed_iff_forced (receiptView g admitted source) ctx x y

theorem json_rows_preserved (g : GateView) (admitted : Bool)
    (source ctx : SnapshotContext) (required : List Claim) :
    (rows (receiptView g admitted source) ctx required).map Prod.fst = required :=
  row_ids_preserved (receiptView g admitted source) ctx required

theorem json_wrong_context_hold (g : GateView) (admitted : Bool)
    (source ctx : SnapshotContext) (x : Claim) (h : source ≠ ctx) :
    observed (receiptView g admitted source) ctx x = none :=
  wrong_context_hold (receiptView g admitted source) ctx x h

theorem json_unadmitted_hold (g : GateView) (source ctx : SnapshotContext) (x : Claim) :
    observed (receiptView g false source) ctx x = none :=
  unadmitted_hold (receiptView g false source) ctx x rfl

def gateView (raw expectedRequest : String) : Except String GateView := do
  let bundle ← strictJson raw
  let receipt ← bundle.getObjVal? "receipt"
  let _ ← bundle.getObjVal? "answer"
  let schema ← (← receipt.getObjVal? "schema").getStr?
  if schema != "kuuos.verifyos.execution-answer-binding.v0.1" then
    throw "receipt schema"
  let req ← (← receipt.getObjVal? "request_sha256").getStr?
  if req != expectedRequest || !hex64 expectedRequest then
    throw "request binding"
  let processes ← receipt.getObjVal? "processes"
  let arr ← processes.getArr?
  if arr.size != 2 then throw "process inventory"
  let p0 ← processes.getArrVal? 0
  let p1 ← processes.getArrVal? 1
  if (← (← p0.getObjVal? "gate").getStr?) != "kuuos_inheritance_gate_v16.py" ||
     (← (← p1.getObjVal? "gate").getStr?) != "kuuos_scope_guard_v16_1.py" then
    throw "gate order"
  let j0 ← strictJson (← (← p0.getObjVal? "stdout").getStr?)
  let j1 ← strictJson (← (← p1.getObjVal? "stdout").getStr?)
  let _ ← j0.getObj?
  let _ ← j1.getObj?
  return ⟨j0,j1,p0,p1⟩

def allClaims : List Claim :=
  [.integrity_status,.scope_status,.integrity_exit_code,.scope_exit_code,
   .snapshot_seq,.snapshot_tip,.rule_count,.withdrawn_count,.obstruction_count,
   .research_certificate_count,.scope_candidate_count,.scope_held_count,.scope_no_use_count,
   .action_permission,.current_tip,.external_truth,.lean_proof,.new_context_validity]

def claimName : Claim → String
  | .integrity_status => "integrity_status"
  | .scope_status => "scope_status"
  | .integrity_exit_code => "integrity_exit_code"
  | .scope_exit_code => "scope_exit_code"
  | .snapshot_seq => "snapshot_seq"
  | .snapshot_tip => "snapshot_tip"
  | .rule_count => "rule_count"
  | .withdrawn_count => "withdrawn_count"
  | .obstruction_count => "obstruction_count"
  | .research_certificate_count => "research_certificate_count"
  | .scope_candidate_count => "scope_candidate_count"
  | .scope_held_count => "scope_held_count"
  | .scope_no_use_count => "scope_no_use_count"
  | .action_permission => "action_permission"
  | .current_tip => "current_tip"
  | .external_truth => "external_truth"
  | .lean_proof => "lean_proof"
  | .new_context_validity => "new_context_validity"

def valueJson : Option Value → Lean.Json
  | none => .null
  | some (.text s) => .str s
  | some (.nat n) => .num (Lean.JsonNumber.fromNat n)

def output (raw requestDigest sourceBinding targetBinding tip : String)
    (admitted : Bool) : Lean.Json :=
  let parsed := gateView raw requestDigest
  let allowed := hex64 sourceBinding && hex64 targetBinding && hex64 tip
  let values : List (Claim × Option Value) :=
    match parsed with
    | .ok g => rows (receiptView g (admitted && allowed) ⟨sourceBinding,tip⟩)
        ⟨targetBinding,tip⟩ allClaims
    | .error _ => allClaims.map (fun x => (x,none))
  let reason := match parsed with
    | .ok _ => if !allowed then "context encoding" else if !admitted then "unadmitted"
      else if sourceBinding != targetBinding then "context mismatch" else ""
    | .error err => err
  Lean.Json.mkObj [
    ("status", .str (if reason == "" then "TYPED_JSON_PROJECTION_ONLY" else "HOLD")),
    ("reason", .str reason),
    ("claims", .arr (values.map (fun (x,y) => Lean.Json.mkObj
      [("claim_id", .str (claimName x)), ("value", valueJson y)])).toArray),
    ("proof_authority", .bool false),
    ("action_authority", .bool false),
    ("complete_python_refinement_proved", .bool false)]

#print axioms uniqueInsert
#print axioms duplicate_insert_rejected
#print axioms fresh_insert_preserves_entries
#print axioms noUnicodeEscape
#print axioms isDigit
#print axioms digits
#print axioms strictNumber
#print axioms quoted
#print axioms parseValue
#print axioms parseObject
#print axioms parseArray
#print axioms strictJson
#print axioms decodeValue
#print axioms decode_natural
#print axioms decode_string
#print axioms decode_bool_hold
#print axioms decode_null_hold
#print axioms decode_negative_hold
#print axioms decode_fraction_hold
#print axioms lookupPath
#print axioms GateView
#print axioms jsonField
#print axioms decodedRaw
#print axioms decoded_field_present
#print axioms decoded_field_missing
#print axioms decoded_raw_iff
#print axioms receiptView
#print axioms observed_iff_json_field
#print axioms missing_field_hold
#print axioms json_projection_forced
#print axioms json_rows_preserved
#print axioms json_wrong_context_hold
#print axioms json_unadmitted_hold
#print axioms gateView
#print axioms allClaims
#print axioms claimName
#print axioms valueJson
#print axioms output

end KUOS.VerifyOS.JsonProjectionV0_16
