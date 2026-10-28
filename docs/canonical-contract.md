# Canonical business history contract

Every row has a stable `id`, `dataset_id` and `synthetic: true`. IDs are namespaced by seed/configuration/profile-shape fingerprint. They are external identity keys, not identifiers in any installed CRM. A replay of the same scenario preserves IDs; a distinct seed creates a distinct namespace. Dates are ISO dates and event timestamps are UTC with `Z`.

All currency amounts ending `_cents` are nonnegative integer minor units in the scenario currency. Line quantity times unit amount equals line total. Invoice subtotal plus tax equals gross. Gross minus posted credit minus posted payment equals outstanding. Billing schedules may be future-dated; issued invoices and posted payments may not exceed the anchor. “Paying customer” requires a posted synthetic payment and a won lead, not a label alone.

`relationships.json` enumerates foreign keys, including polymorphic notes/activity subjects. The local validator rejects dangling keys, inconsistent payment/customer linkage, meeting contacts from a different account and task dependency cycles. A fixture can demonstrate a property of this model; it cannot prove target authorization, accounting policy or external workflow behavior.

The explicit fictional talent pool is independent from the smaller engaged staff list. Talent-skill links are unique per person and skill. Generic profile shapes are independently enumerated and balanced; no real biography or private roster is included. Contacts, companies, conversations and knowledge text are authored fiction, not anonymized customer data.

CSV is a transport projection of canonical JSONL. Nested values are JSON strings; null is empty; booleans are lower-case text; potentially active spreadsheet text is apostrophe-escaped. Schemas and data dictionary describe the actual example shapes. A consumer must choose target-specific null/empty/clear semantics and preserve all unmapped data rather than silently discarding it.
