using System.Runtime.CompilerServices;
using BenchmarkDotNet.Attributes;

namespace DisposalBenchmarks;

[MemoryDiagnoser]
[ShortRunJob]
public class ScopeOverheadBenchmarks
{
    private const int Operations = 1_024;

    [Benchmark(Baseline = true, OperationsPerInvoke = Operations)]
    public int UsingStatement()
    {
        var sum = 0;

        for (var i = 0; i < Operations; i++)
        {
            using (var probe = CreateProbe())
            {
                sum += probe.Read();
            }
        }

        return sum;
    }

    [Benchmark(OperationsPerInvoke = Operations)]
    public int UsingDeclaration()
    {
        var sum = 0;

        for (var i = 0; i < Operations; i++)
        {
            using var probe = CreateProbe();
            sum += probe.Read();
        }

        return sum;
    }

    [Benchmark(OperationsPerInvoke = Operations)]
    public int TryFinallyDispose()
    {
        var sum = 0;

        for (var i = 0; i < Operations; i++)
        {
            var probe = CreateProbe();
            try
            {
                sum += probe.Read();
            }
            finally
            {
                probe.Dispose();
            }
        }

        return sum;
    }

    [MethodImpl(MethodImplOptions.NoInlining)]
    private static DisposableProbe CreateProbe() => new();

    private sealed class DisposableProbe : IDisposable
    {
        private int _value = 42;

        [MethodImpl(MethodImplOptions.NoInlining)]
        public int Read() => _value;

        [MethodImpl(MethodImplOptions.NoInlining)]
        public void Dispose() => _value = 0;
    }
}
