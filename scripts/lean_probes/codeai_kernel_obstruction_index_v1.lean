import KuuOSFormal

/-!
Read-only index of theorem types in the imported canonical public root.
This file is a research probe, never a new public proof root.
Classify syntactic heads, not semantic impossibility. Keep original Expr.
-/
open Lean
namespace KuuOSKernelObstructionIndexProbe
set_option autoImplicit false

def headName (e : Expr) : String :=
  match e.getAppFn with
  | .const n _ => n.toString
  | .bvar _ => "bound-variable"
  | .fvar _ => "free-variable"
  | .sort _ => "sort"
  | .forallE .. => "forall"
  | .letE .. => "let"
  | .lam .. => "lambda"
  | .mdata .. => "metadata"
  | .proj .. => "projection"
  | _ => "other"

def negativeHead (e : Expr) : Bool :=
  e.isAppOf `Not || e.isAppOf `Ne || e.isAppOf `IsEmpty || e.isConstOf `False

def negativeMarker (e : Expr) : Bool :=
  e.getUsedConstants.any fun n =>
    n == `Not || n == `Ne || n == `IsEmpty || n == `False

def peel : Expr → List Expr × Expr
  | .forallE _ d b _ =>
    let (ds, c) := peel b
    (d :: ds, c)
  | .mdata _ e => peel e
  | e => ([], e)

def binderRow (e : Expr) : Json :=
  Json.mkObj [("head", toJson (headName e)),
              ("negative_head", toJson (negativeHead e)),
              ("negative_marker", toJson (negativeMarker e))]

def theoremRow (name : Name) (moduleName : String) (info : ConstantInfo) : Json :=
  let (domains, conclusion) := peel info.type
  Json.mkObj [
    ("name", toJson name.toString),
    ("module", toJson moduleName),
    ("type_expr_repr", toJson (reprStr info.type)),
    ("universe_parameters", toJson (info.levelParams.map Name.toString)),
    ("type_constants", toJson (info.type.getUsedConstants.map Name.toString)),
    ("binder_domains", toJson (domains.map binderRow)),
    ("conclusion_head", toJson (headName conclusion)),
    ("conclusion_negative_head", toJson (negativeHead conclusion)),
    ("conclusion_negative_marker", toJson (negativeMarker conclusion)),
    ("conclusion_constants", toJson (conclusion.getUsedConstants.map Name.toString)),
    ("unresolved_type", toJson (info.type.hasMVar || info.type.hasFVar || info.type.hasLooseBVars))]

set_option maxRecDepth 8192 in
set_option maxHeartbeats 0 in
run_cmd do
  let env ← getEnv
  let modules := env.allImportedModuleNames
  let requested ← Lean.Elab.Command.liftIO <| IO.FS.readFile "__MODULE_FILE__"
  let wanted : Std.HashSet String := (requested.splitOn "\n").foldl
    (fun acc name => acc.insert name) {}
  let selected : Array (Name × ConstantInfo × String) :=
    env.constants.fold (fun rows name info =>
      if info.isTheorem then
        match env.getModuleIdxFor? name with
        | some idx =>
          let moduleName := modules[idx]!.toString
          if wanted.contains moduleName then rows.push (name, info, moduleName) else rows
        | none => rows
      else rows) #[]
  let inventory := Json.mkObj [
    ("imported_modules", toJson (modules.map Name.toString)),
    ("selected_theorems", toJson selected.size)]
  Lean.Elab.Command.liftIO do
    IO.FS.writeFile "__META_FILE__" (inventory.compress ++ "\n")
    IO.FS.withFile "__ROWS_FILE__" .write fun handle => do
      for (name, info, moduleName) in selected do
        handle.putStr ((theoremRow name moduleName info).compress ++ "\n")
    IO.println s!"KUUOS_KERNEL_OBSTRUCTION_EXPORT {selected.size}"

end KuuOSKernelObstructionIndexProbe
