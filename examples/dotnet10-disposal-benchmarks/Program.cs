using BenchmarkDotNet.Running;

namespace DisposalBenchmarks;

internal static class Program
{
    public static int Main(string[] args)
    {
        if (args.Contains("--self-check", StringComparer.Ordinal))
        {
            return SelfCheck.Run();
        }

        BenchmarkSwitcher.FromAssembly(typeof(Program).Assembly).Run(args);
        return 0;
    }
}
