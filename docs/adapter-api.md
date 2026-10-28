# Offline adapter API

`build_adapter(name, tables, options=None) -> (files, plan)` is a pure mapping operation. `tables` is a dictionary of canonical domain names to record lists. `files` maps filename to mapped row dictionaries. `plan` describes the mechanism, official sources, required target configuration, covered/unmapped domains, relationships and replay limits. It grants no execution authority.

`export_adapter(name, tables, output, options=None)` writes UTF-8 CSV, mirrored JSON and `import-plan.json`. A plan hash excludes its own hash field. Identical inputs and options reproduce identical files. The five adapter identifiers are `salesforce`, `hubspot`, `dynamics365`, `zoho_crm`, `pipedrive`.

`export_crm.py` validates the canonical dataset before mapping. Its `--options` file is keyed by adapter; `pipeline` and `stage_map` are caller assertions that must be checked against the real target. A conventional fixture stage label is never native-validation evidence. Example:

```json
{"hubspot":{"pipeline":"YOUR_EXISTING_PIPELINE","stage_map":{"closed_won":"YOUR_WON_STAGE","closed_lost":"YOUR_LOST_STAGE"}}}
```

Transformations preserve a stable source key, express integer cents as an exact two-place decimal, retain ISO dates, project canonical customer status into descriptive metadata, and resolve each source relationship to an existing canonical account/contact before export. No synthetic key is written as a Salesforce Id, HubSpot Record ID, Dataverse GUID, Zoho module ID or Pipedrive System ID.

Salesforce's relationship column is `Account.StoryFoundry_ID__c`, conditional on the custom unique external-ID field and selected loader behavior. HubSpot's company domain accompanies child rows for explicitly configured association mapping. Dynamics and Zoho carry a unique fictional account name for lookup mapping, with a source-ID sidecar; a target duplicate or ambiguous lookup must stop actual import. Pipedrive uses combined person/organization/deal rows and explicit provenance columns. The caller must not infer successful linking from a row's presence.

All adapter plans carry `OFFLINE_FIXTURE_TARGET_CONFIGURATION_REQUIRED`, `live_import_tested: false`, `execution_authorized: false` and `network_calls: 0`. Required custom synthetic marker/provenance properties, target keys, stages, layouts and permissions are holds. A future real importer belongs behind a separate interface that accepts exact action authority, a target-verified mapping, bounded batches, preimages, target IDs and an uncertainty ledger.

Canonical data includes a contract/project cycle. A future system importer must create object shells first and link after target IDs are known, or use a proven target transaction mechanism. Native adapters in this release map only accounts, contacts and opportunities and list the rest as unmapped.
