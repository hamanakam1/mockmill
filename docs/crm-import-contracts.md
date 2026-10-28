# Five CRM import contracts

The five contracts are maintained as machine-readable data in the research bundle's `crm-import-contracts.json` and summarized by the public-safe adapter plans generated locally. This candidate intentionally does not vendor-bundle the research archive. They define proposed offline mappings, not vendor contracts or native acceptance. Each adapter remains `execution_authorized: false`; target configuration, permissions, identifiers, required fields, replay behavior and rollback must be verified in an authorized non-production tenant before any import design can be activated.

The implementation status is five offline adapters for accounts, contacts and opportunities. The other canonical domains are explicitly unmapped. See the generated adapter plans under `examples/crm-fixtures/` after running `export_crm.py`.
