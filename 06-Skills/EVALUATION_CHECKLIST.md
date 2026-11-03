# Skill Evaluation Checklist

Evaluate the exact surface proposed for activation. Record source URL, revision, selected files and scan receipts. A study verdict is separate from permission to install.

| Item | Evidence required |
|---|---|
| Purpose | Read the README or equivalent package description and locate the real entry point. |
| Readability | Inspect the implementation and referenced execution surfaces; unexplained obfuscation fails. |
| Network | Identify destinations and data sent for the inspected paths; uninspected paths are unknown. |
| Filesystem | Name read/write roots and prove containment for executable paths. |
| Execution | Identify shell, hooks, startup and lifecycle behavior; all required side effects need authorization. |
| Compatibility | Record the target runtime and actual validation performed. Static inspection alone leaves runtime compatibility unknown. |
| License | Identify the applicable license for each borrowed surface. Missing or unclear permission blocks import. |
| Local fit | Show the adapted content, unmet need and overlap assessment. A proposed adaptation is not an applied customization. |

Each row is pass, fail or unknown with file-and-line evidence. Score only proven passes out of eight; report fail and unknown counts separately. Unknown earns no point.

Unsafe execution, credential exposure, unbounded filesystem access, instruction hijacking or missing license permission veto activation regardless of total. Eight passes make a candidate eligible for a separate approval; six or seven passes require an exact remediation proposal and re-evaluation; fewer than six reject activation. A rejected activation can still yield an independently written borrow-only pattern.

During evaluation, never run a candidate installer, setup script, lifecycle hook or pipe-to-shell command. Inspect inert source first. Any later installation is a separate task with its own scope and approval; this checklist never authorizes it.
