# Release checklist

MockMill releases are deterministic, synthetic-only artifacts. A release must preserve the distinction between package availability, offline fixture generation and native target acceptance.

## Local verification

```bash
python -m unittest -v
python generate.py --output /tmp/mockmill-fixture
python validate.py --data /tmp/mockmill-fixture --receipt /tmp/mockmill-validation.json
python import_preview.py --data /tmp/mockmill-fixture --output /tmp/mockmill-preview
python export_crm.py --data /tmp/mockmill-fixture --output /tmp/mockmill-adapters
python -m build
```

## Release meaning

- The Python package contains deterministic generation and offline mapping code.
- Release assets may contain source and checksums; they must contain no credentials, real customer data, native IDs or production exports.
- A successful build does not prove that any CRM accepts the fixture.
- Native imports remain outside the release claim until a target-specific, authorized non-production acceptance run exists.
