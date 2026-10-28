# MockMill data dictionary

This dictionary describes the generated canonical fixture, not a recovered CloudTeams or CRM schema. Every domain is available as JSONL and CSV; adapters currently map only accounts, contacts and opportunities.

| Field family | Meaning | Contract |
|---|---|---|
| `id` | Stable synthetic row identity | Namespaced by seed/configuration/profile-shape fingerprint; never a vendor-native ID |
| `dataset_id` | Fixture/configuration identity | Constant within one generated dataset |
| `synthetic` | Provenance marker | Always boolean `true`; CSV is lower-case `true` |
| `*_id` | Foreign-key reference | Must resolve through `relationships.json`; unmapped target relationships remain in canonical output |
| `*_date`, `*_at` | Business date or UTC timestamp | ISO date or UTC `Z`; chronology is validated |
| `*_cents` | Monetary amount | Nonnegative integer minor units; decimal export is a presentation projection |
| `status` | Domain lifecycle state | Validated against domain chronology and configured transitions |
| `currency` | Scenario currency | Target currency mapping remains a prerequisite |

Population and story configuration live in `inputs/company.json` and `inputs/profile-shapes.json`. Templates declare chronology, relationships, currencies, identifiers and target prerequisites. A target adapter may omit fields only when its plan records the omission and preserves the canonical source.

## Portable CRM profile

The core CRM entities intentionally carry vendor-neutral fields that can be templated across the five foundation targets. Accounts include lifecycle, ownership, firmographic, regional and financial-context fields; contacts include role, department, language and contactability fields; leads include qualification, provenance and next-action fields; opportunities include forecast, probability, type and next-step fields. Adapters translate these into target naming conventions without asserting that a target accepts every field or that a custom field already exists.
