# Synthetic Private Consumer

This directory simulates a private repository using only public, synthetic data.

Run the complete consumer, Feature Delivery Case, reusable-asset, evidence, manager-claim, negative-case, asset-pack, and golden-output checks:

```bash
python examples/synthetic-private-consumer/run_conformance.py \
  --root examples/synthetic-private-consumer \
  --lattice-root . \
  --check
```

Generate a review copy outside the golden directory:

```bash
python examples/synthetic-private-consumer/run_conformance.py \
  --root examples/synthetic-private-consumer \
  --lattice-root . \
  --out /tmp/manager-ready-delivery-asset-pack
```

The fixed `v0.0.0-synthetic` and all-zero commit are deterministic fixture sentinels. Local Git resolution is bypassed only for that exact sentinel pair on a `synthetic_reference`; every other synthetic or real pin must match the local pinned checkout.

Generation refuses to replace an existing output directory unless `--force` is explicit.

The example proves contract shape, local generation, validator dispatch, negative rejection, and golden stability. It does not prove real use, reuse, team adoption, manager acceptance, ROI, business value, or approval.
