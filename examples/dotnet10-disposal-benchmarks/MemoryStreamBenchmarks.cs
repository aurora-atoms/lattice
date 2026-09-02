using BenchmarkDotNet.Attributes;

namespace DisposalBenchmarks;

[MemoryDiagnoser]
[ShortRunJob]
public class MemoryStreamBenchmarks
{
    private byte[] _payload = null!;

    [Params(1_024, 64 * 1_024)]
    public int PayloadSize { get; set; }

    [GlobalSetup]
    public void Setup()
    {
        _payload = GC.AllocateUninitializedArray<byte>(PayloadSize);
        for (var i = 0; i < _payload.Length; i++)
        {
            _payload[i] = (byte)(i & 0xFF);
        }
    }

    [Benchmark(Baseline = true)]
    public long UsingDispose()
    {
        using var stream = new MemoryStream(PayloadSize);
        stream.Write(_payload);
        return stream.Length;
    }

    [Benchmark]
    public long TryFinallyDispose()
    {
        var stream = new MemoryStream(PayloadSize);
        try
        {
            stream.Write(_payload);
            return stream.Length;
        }
        finally
        {
            stream.Dispose();
        }
    }
}
