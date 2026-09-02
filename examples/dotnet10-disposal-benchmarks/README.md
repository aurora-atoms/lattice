# .NET 10 disposal benchmark: `using` vs `try/finally`

This is a deliberately small, synthetic benchmark used to answer one bounded question:

> On .NET 10, does `using` itself improve execution time or managed-memory allocation compared with an equivalent hand-written `try/finally` that calls `Dispose()` at the same lifetime boundary?

It also verifies the more important semantic property: both forms dispose exactly once on normal and exceptional exit when ownership and scope are equivalent.

## Hypothesis

For equivalent code and the same disposal boundary:

- `using (...) { ... }` should have no material steady-state performance advantage over hand-written `try/finally`;
- `using var` inside an equivalent lexical scope should likewise have no material advantage;
- managed allocations should be the same, because `using` is a lifetime/cleanup construct rather than an allocation-elimination feature;
- the practical resource benefit comes from disposing scarce resources correctly and at the earliest appropriate boundary, not from the syntax itself.

The benchmark is intentionally capable of falsifying that hypothesis. Treat differences smaller than benchmark noise as equivalent rather than declaring a winner from a single run.

## Runtime

- Target framework: `net10.0`
- Language version: C# 14
- Benchmark harness: BenchmarkDotNet 0.15.8
- Memory measurement: BenchmarkDotNet `MemoryDiagnoser`

## What is measured

### 1. Scope overhead

`ScopeOverheadBenchmarks` compares three equivalent forms over the same disposable object and workload:

```csharp
using (var resource = Create())
{
    Use(resource);
}
```

```csharp
using var resource = Create();
Use(resource);
```

```csharp
var resource = Create();
try
{
    Use(resource);
}
finally
{
    resource.Dispose();
}
```

The disposable factory and hot methods are marked `NoInlining` so the benchmark is less likely to collapse into an optimizer artifact. Each benchmark invocation performs 1,024 operations and BenchmarkDotNet normalizes the result per operation.

### 2. Managed allocation

`MemoryStreamBenchmarks` compares `using` with equivalent `try/finally` around `MemoryStream` for 1 KiB and 64 KiB payloads. This demonstrates whether the syntax changes managed allocation when object creation and lifetime boundaries are otherwise identical.

The payload is allocated in `GlobalSetup`, so the reported per-operation allocation is attributable to the measured stream work rather than test-data creation.

### 3. Semantic self-check

`SelfCheck` verifies before benchmarking that:

- normal exit disposes exactly once in both forms;
- exception exit disposes exactly once in both forms;
- the tracked resource is live inside the protected scope and released immediately after the equivalent lifetime boundary.

This is not a performance measurement. It guards the experiment against accidentally benchmarking semantically different code.

## Run locally

From this directory:

```bash
dotnet restore
dotnet build -c Release --no-restore
dotnet run -c Release --no-build -- --self-check
dotnet run -c Release --no-build -- --filter "*"
```

Do not use Debug builds for performance conclusions.

BenchmarkDotNet writes detailed environment metadata and result files under `BenchmarkDotNet.Artifacts/`.

## CI

The repository workflow `.github/workflows/dotnet10-disposal-benchmark.yml` runs on pull requests that change this experiment and can also be started manually.

CI performs:

1. .NET 10 SDK setup;
2. restore and Release build;
3. semantic self-check;
4. the complete short BenchmarkDotNet suite;
5. upload of `BenchmarkDotNet.Artifacts` for inspection.

GitHub-hosted runners are shared infrastructure, so CI numbers are useful for confirming order-of-magnitude behavior and allocation equivalence, not for claiming tiny nanosecond differences. Repeat locally on controlled hardware before making a micro-optimization decision.

## How to interpret the result

If the experiment behaves as expected, the important conclusion is not "using is faster." It is:

> For equivalent ownership and scope, `using` and explicit `try/finally + Dispose()` should compile down to equivalent cleanup behavior and should have effectively the same runtime/allocation cost. `using` is preferred because it expresses ownership and guaranteed cleanup more clearly and is harder to implement incorrectly.

A real application can still gain large memory or throughput benefits from **earlier disposal** of file handles, pooled database connections, sockets, native buffers, or other scarce resources. That is a resource-lifetime effect. It should not be attributed to `using` syntax when an equivalent `try/finally` would dispose at the same point.

## Non-goals

This experiment does not claim to measure:

- database connection-pool throughput;
- socket exhaustion;
- OS file-handle pressure;
- native-memory release behavior for every `IDisposable` implementation;
- `await using` / `IAsyncDisposable`;
- finalizer behavior;
- application-specific effects of broad versus narrow scopes.

Those require workload-specific benchmarks because the cost is dominated by the underlying resource rather than by the C# cleanup syntax.
