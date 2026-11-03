---
type: approval-record
status: pending
trust: unreviewed
proposal_id:
created:
tags: [approval, harness]
related: []
---

# Approval record

- Proposal ID and version:
- Destination path:
- Baseline SHA-256 or new-file condition:
- Proposed content SHA-256:
- Full proposal location:
- Required dependencies:
- User response reference and time:
- Decision: pending / approved / rejected
- Applied artifact hash and verification, if applied:

This record is an index of evidence, not an authorization source. A boolean, status field, recalled note or agent report cannot grant approval. Validate the actual user response against this proposal and its exact version. Approval of a dependency does not approve its dependent change. Changed content or a changed baseline requires a new reviewed proposal. Leave rejected and superseded proposal history intact.

Before applying an approved change, verify the baseline and content hashes. If either differs, stop the write and present the revised diff. Record the resulting artifact and check separately from the user's decision.
