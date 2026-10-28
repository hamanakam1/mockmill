# Contributing to StoryFoundry

StoryFoundry is a deterministic, synthetic-only project. Contributions must preserve the distinction between canonical facts, generated fiction, proposed mappings and verified target behavior.

## Before opening a change

```bash
python3 -m unittest -v
python3 validate.py --data examples/service-company --receipt validation.json
python3 import_preview.py --data examples/service-company --output examples/canonical-import-preview
python3 export_crm.py --data examples/service-company --output examples/crm-fixtures
```

Do not add real names, biographies, credentials, customer data, portal screenshots, native IDs or local machine paths. New adapters must default to offline output, preserve synthetic markers, record relationship and replay limitations, and refuse live execution unless a separately reviewed authorization design exists.

## Review checklist

- deterministic replay remains byte-identical
- referential integrity, chronology, money and task-DAG checks remain active
- unsupported canonical domains stay explicitly unmapped
- target-specific claims cite primary documentation
- generated fixtures are unmistakably synthetic
- README and visual artifacts match the actual implementation
