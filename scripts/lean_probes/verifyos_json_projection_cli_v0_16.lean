import JsonProjection

open KUOS.VerifyOS.JsonProjectionV0_16
set_option autoImplicit false

/-- The trusted host supplies each exact receipt file and the separately
bound request/context/tip. Exit zero means that the batch returned results,
not that every claim or any external fact is certified. -/
def runCases : List String → IO UInt32
  | [] => pure 0
  | path :: requestDigest :: sourceBinding :: targetBinding :: tip :: flag :: rest => do
    let admitted ← match flag with
      | "true" => pure true
      | "false" => pure false
      | _ => throw (IO.userError "admission argument")
    let raw ← IO.FS.readFile path
    IO.println (output raw requestDigest sourceBinding targetBinding tip admitted).compress
    runCases rest
  | _ => throw (IO.userError "expected six arguments per case")

def main (args : List String) : IO UInt32 := runCases args

#print axioms runCases
#print axioms main
