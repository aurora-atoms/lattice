# Private Repository Consumer Templates

Copy these files into a private downstream repository. Replace every `REPLACE_...` value before validation. Templates are intentionally public and synthetic; they contain no real evidence.

```text
downstream-consumer-manifest.template.json
private-capability-extension.template.json
```

Run locally from the private repository:

```bash
python vendor/lattice/scripts/validate_downstream_consumer.py \
  downstream-consumer-manifest.json \
  --lattice-root vendor/lattice \
  --consumer-root .
```

The validator reads the manifest, declared extension manifests, and the pinned public canonical capability manifest. It does not read `evidence_storage`, use the network, or upload private data.
