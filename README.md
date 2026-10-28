# MockMill

```text
  +--------------------------------------------------+
  |                    MOCK MILL                    |
  |              fake data. real flow.              |
  +--------------------------------------------------+
```

[![CI](https://github.com/hamanakam1/mockmill/actions/workflows/ci.yml/badge.svg)](https://github.com/hamanakam1/mockmill/actions/workflows/ci.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-55d6be.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](pyproject.toml)
[![Offline by design](https://img.shields.io/badge/imports-offline%20only-e58f65.svg)](docs/crm-import-contracts.md)

> **Synthetic data with a memory.** Generate a coherent business history, validate its relationships and arithmetic, then inspect portable CRM mappings without touching a target system.

**Status:** public release candidate · MIT · deterministic · offline-only adapters

*A fictional wordplay nod to a stage-name convention; MockMill is independent, unaffiliated and not an impersonation of any artist.*

**Repository:** [github.com/hamanakam1/mockmill](https://github.com/hamanakam1/mockmill)

**Coherent fictional businesses, portable records and reviewable offline CRM import plans.** MockMill is a public MIT-licensed release. It generates fictional records and offline adapter fixtures; it does not perform live CRM imports.

MockMill generates an explicitly synthetic service-company history with reproducible seeds, stable external IDs, relationships, dated events and reconciled money. It includes failures, partial payment, cancellations, lost leads, repeated engagements, support and knowledge history—not only an idealized customer list. The canonical model is independent of any CRM. Five executable starter adapters map its account, contact and opportunity records into CSV/JSON fixtures for Salesforce, HubSpot, Dynamics 365, Zoho CRM and Pipedrive.

**Every person, company and transaction is fictional.** Examples use reserved invalid domains, fictional telephone numbers and non-deliverable addresses. No real roster, biography, conversation, customer evidence, credentials or account identifiers are bundled. The generic talent distribution is independently enumerated in `inputs/profile-shapes.json`.

## Start here

| If you want to… | Go to |
|---|---|
| See the product | [Visual guide](docs/VISUALS.md) |
| Generate a story | [Run locally](#run-locally) |
| Understand the data | [Schema](docs/schema.json) · [Data dictionary](docs/data-dictionary.md) |
| Compare CRM mappings | [Five-CRM contracts](docs/crm-import-contracts.md) |
| Build a package | [Release checklist](docs/RELEASE.md) |
| Contribute safely | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Why MockMill

Most fake-data fixtures are disconnected rows. MockMill creates a dated, relational business story with leads, accounts, contacts, opportunities, projects, tasks, support, knowledge, invoices, credits, payments and meetings. Deterministic validation keeps the story coherent while preserving failure cases, partial payment, cancellations, lost opportunities and future work.

The portable profile is deliberately broader than one CRM: firmographics, lifecycle, ownership, contactability, qualification, provenance, forecast, probability and next-action fields are retained canonically and translated into five target-shaped offline exports.

## Run locally

Python 3.10+ and the standard library are sufficient. No account, model, API key, paid service or installation step is needed.

```bash
python3 generate.py --output examples/service-company
python3 validate.py --data examples/service-company --receipt validation.json
python3 -m unittest -v
python3 import_preview.py --data examples/service-company --output examples/canonical-import-preview
python3 export_crm.py --data examples/service-company --output examples/crm-fixtures
```

The supplied fixture has 38 domains and 21,923 records: 100 fictional paying customers, 500 leads, 600 contacts, 1,000 fictional talent profiles, 40 engaged staff, 140 projects, 417 invoices and 440 meetings, including 40 future meetings. Its two-year history runs 29 October 2024–28 October 2026. These are scenario sizes, not claims about a business. The same configuration and seed yield identical canonical records and file hashes. A different seed uses a different external-ID namespace.

`templates/professional-services.json` and `templates/marketplace-advisory.json` are complete independent scenario configurations. Pass one with `--config`. Edit the six service offerings, dates, seed and population in a copy. The talent shape counts must equal configured talent; pass an alternate shape file with `--profiles` to generation and validation. Core CRM entities include a portable, vendor-neutral profile spanning firmographics, ownership, contactability, qualification, forecast and next-action fields so the same template can be adapted to multiple systems. An optional narrative file is inert, clearly labeled creative prose; financial facts and relationships come from deterministic tables.

## What the five adapters actually do

Each adapter executes locally and produces real CSV/JSON files, a relationship sidecar, official-source links, field/property prerequisites and a deterministic import-plan hash. **All five are offline foundations requiring target configuration. None has been tested by importing into a CRM account.** They do not call an API, create an account, send messages or authorize a write.

| Adapter | Selected mechanism | Replay and relationship boundary |
|---|---|---|
| Salesforce | Data Loader CSV, one object per file | Configured unique custom External ID fields and explicit relationship mapping; repeated insert is not upsert |
| HubSpot | UI CSV import with mapped properties and associations | Email/domain identification for appropriate objects; deals need real Record ID or a supported configured unique property, plus valid pipeline/stage |
| Dynamics 365 | Model-driven app CSV import wizard | A defined, selected Dataverse alternate key and verified lookup resolution; synthetic keys are not target GUIDs |
| Zoho CRM | Module CSV import; Accounts before child modules | Required layout fields and permitted unique-field/module-ID update mode; no claim that CSV generically updates external-ID fields |
| Pipedrive | Spreadsheet import with mapped person/organization/deal columns | Rows link entities; subsequent updates require genuine Pipedrive System IDs, which the generator never fabricates |

Only three entity families are mapped natively in this version. The other 35 domains remain available as canonical JSONL/CSV and are explicitly listed as unmapped in every plan. Their native extensions require research and separate implementation. Target layouts, editions, permissions, required properties, date/currency handling, validation rules, duplicate policies and side effects must be qualified before any authorized import. The default HubSpot pipeline is deliberately `CONFIGURE_EXISTING_PIPELINE`.

See [foundation contracts](docs/crm-foundations.md), [adapter API](docs/adapter-api.md) and [canonical contract](docs/canonical-contract.md). A locally valid CSV is not evidence that a CRM accepted its data.

## Visual tour

The [visual guide](docs/VISUALS.md) shows the product flow, validation evidence and the exact boundary between the canonical model and the five offline adapters.

For the satire layer, see the [full-color MockMill ASCII portrait](docs/visuals/mockmill-meek-mill-color-ascii.html). It is an explicitly fan-made, unaffiliated character-mosaic transformation; the source photograph is not included.

## Model, story and evidence

The canonical domains cover company, accounts/customers/contacts, leads/opportunities, services/campaigns, talent/skills/staff, contracts/projects/milestones/tasks, time/expenses, invoices/credits/payments, support, meetings, conversations, notes/activity and knowledge versions. JSONL is canonical; CSV carries the same IDs and an explicit synthetic marker. Every mapped CRM row also carries a synthetic-marker column requiring explicit target mapping.

Money uses integer cents and decimal export, never binary floating-point rounding. Issued invoice total minus posted credits equals posted payments plus outstanding balance. Every paying customer has a synthetic payment. Future billing schedules are separate from issued invoices; future meetings are scheduled, not completed. Stable reference contracts and dated notes support the generated story. No real revenue, tax advice, customer endorsement, certification or Marketplace approval is implied.

`examples/service-company/STORY_BIBLE.md`, `summary.json`, standalone SVG charts and their monthly CSV make the story auditable. Optional model prose cannot alter numerical facts. Tests inject broken references, cycles, invoice imbalance, future payments, wrong-account meeting contacts and non-reserved endpoints; they also verify replay, CSV safety and each adapter's relationship semantics.

## Import safety and rollback

There is no `push`, `apply` or live execution command. `import_preview.py` emits `DRY_RUN_ONLY`, `execution_authorized: false` and a prospective rollback inventory with `NONE_DRY_RUN` and deletion disabled. An actual importer must be separately designed and authorized, capture target IDs and preimages, reconcile uncertain results, and prove target-specific replay behavior. Never delete a pre-existing target row or assume a source ID is a vendor-native record ID.

Formula-leading text is escaped with an apostrophe in CSV. Preserve the canonical JSON value and document any target-specific decoding. Blank values do not universally mean “clear,” especially for HubSpot; mappings must distinguish omission, empty value and explicit clearing.

## Position and roadmap

The intended distinction is a coherent business story and chronology, auditable consistency checks, and researched offline CRM mappings. Reproducible seeds, foreign keys and dependency handling already exist in other generators; this project does not claim those as novel. A separately researched competitive review and 100-candidate prioritization distinguish future candidates from the five implemented file adapters. Rankings are product-roadmap proposals, not measured market-share claims or 100 completed integrations.

The public candidate contains independently authored generic profiles and fixtures only. Publication review must confirm the chosen license, attribution, fixture privacy, build evidence and exact file inventory. See [publication review](docs/PUBLICATION_REVIEW.md).

## Package install

The package has no runtime dependencies and exposes four command-line entry points:

```bash
python -m pip install mockmill-0.2.0.tar.gz
mockmill-generate --output examples/service-company
mockmill-validate --data examples/service-company --receipt validation.json
mockmill-preview --data examples/service-company --output examples/canonical-import-preview
mockmill-export --data examples/service-company --output examples/crm-fixtures
```

The package build is intended for reproducible local use. It does not add credentials, network clients or live-import behavior.

## License

MockMill is licensed under the [MIT License](LICENSE). Public release assets and package metadata preserve the offline-only boundary.
