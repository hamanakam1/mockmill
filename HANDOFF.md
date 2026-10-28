# StoryFoundry successor handoff — stopped at operator checkpoint

Status: working local public-release candidate; not yet initialized as its own Git repository, not committed or published. No process from this worker remains running. Preserve the current independent generic fixture and code.

## Current implementation

- Standard-library deterministic canonical generator: 38 domains and 21,923 generic example records, including 100 fictional customers, 500 leads, 1,000 independently generated talent profiles, 40 staff and 40 future meetings.
- Independent generic profile input: ten job families, three independently enumerated skills per family. No imported/private roster, original names or biographies, private portal evidence or model-run receipt was copied into this candidate.
- Two complete templates: professional services and marketplace advisory. Canonical JSONL/CSV, computed story bible, monthly cohort data and standalone SVG charts are generated.
- Five actual offline adapter implementations and generated CSV/JSON fixtures: Salesforce, HubSpot, Dynamics 365, Zoho CRM, Pipedrive. Core mapping is accounts, contacts and opportunities only. Other 35 canonical domains are explicitly unmapped natively. No API client, target credentials, push/apply command or live import exists.
- Plans retain target-configuration holds, source references, relationship sidecars, deterministic hashes and explicit synthetic columns. Source IDs are never vendor-native IDs. HubSpot pipeline is deliberately CONFIGURE_EXISTING_PIPELINE. Pipedrive replay needs genuine System IDs. Zoho CSV is not presented as arbitrary external-ID upsert.

## Verification already completed

`PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -q`: **26 tests PASS**, after the explicit synthetic-marker columns were added to all five adapters. The full generic fixture validator PASSed. All five adapter exporters and canonical import preview executed successfully locally. Tests cover financial imbalance, dates, references, task cycles, wrong-account meeting contacts, CSV formulas, identity namespaces, exact replay and adapter relationship/replay limits. No target import validation has occurred.

## Remaining work — do not claim finished release

1. Integrate the independent research worker's completed competitive/licensing comparison, first-five import contracts and **100 ranked candidates roadmap** when available. That research is not yet copied into this tree. A 100-candidate roadmap is not 100 adapters.
2. Finish privacy/license/publication review. `docs/PUBLICATION_REVIEW.md` explicitly leaves license selection pending the repository owner. No license grant or remote publication is claimed.
3. `docs/canonical-contract.md` currently mentions schemas/data dictionary, but standalone schema/data-dictionary artifacts have not yet been added. Either implement those artifacts or remove that claim before publication.
4. Add a consolidated verification receipt and exact public-candidate file inventory; review docs for claims versus actual outputs. Full-data receipts already exist as validation.json and generated manifests.
5. Initialize this exact directory as a new local Git repository, stage explicit owned paths and commit after final checks. Parent owns remote creation/push. No .git currently exists here; do not accidentally stage from an ancestor repository.

## Exact continuation commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v
PYTHONDONTWRITEBYTECODE=1 python3 validate.py --data examples/service-company --receipt validation.json
PYTHONDONTWRITEBYTECODE=1 python3 export_crm.py --data examples/service-company --output examples/crm-fixtures
PYTHONDONTWRITEBYTECODE=1 python3 import_preview.py --data examples/service-company --output examples/canonical-import-preview
```

No regeneration or expanded tests are needed unless changes justify them. Current examples already reflect the generic independent profile input and the explicit native-file synthetic-marker columns. Official-source import constraints are documented in docs/crm-foundations.md and each generated import plan. No competitor benchmark, market-share ranking or native acceptance should be inferred.
