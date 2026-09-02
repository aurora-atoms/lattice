namespace DisposalBenchmarks;

internal static class SelfCheck
{
    public static int Run()
    {
        try
        {
            VerifySuccessPath();
            VerifyExceptionPath();
            VerifyEquivalentLifetimeBoundary();
            Console.WriteLine("Self-check passed: using and equivalent try/finally dispose exactly once on success and exception paths, with the same lifetime boundary.");
            return 0;
        }
        catch (Exception exception)
        {
            Console.Error.WriteLine($"Self-check failed: {exception}");
            return 1;
        }
    }

    private static void VerifySuccessPath()
    {
        var usingProbe = new CountingDisposable();
        using (usingProbe)
        {
            usingProbe.Touch();
        }

        var manualProbe = new CountingDisposable();
        try
        {
            manualProbe.Touch();
        }
        finally
        {
            manualProbe.Dispose();
        }

        Require(usingProbe.DisposeCount == 1, "using success path did not dispose exactly once");
        Require(manualProbe.DisposeCount == 1, "try/finally success path did not dispose exactly once");
        Require(usingProbe.TouchCount == manualProbe.TouchCount, "success paths performed different work");
    }

    private static void VerifyExceptionPath()
    {
        var usingProbe = new CountingDisposable();
        try
        {
            using (usingProbe)
            {
                usingProbe.Touch();
                throw new ExpectedException();
            }
        }
        catch (ExpectedException)
        {
        }

        var manualProbe = new CountingDisposable();
        try
        {
            try
            {
                manualProbe.Touch();
                throw new ExpectedException();
            }
            finally
            {
                manualProbe.Dispose();
            }
        }
        catch (ExpectedException)
        {
        }

        Require(usingProbe.DisposeCount == 1, "using exception path did not dispose exactly once");
        Require(manualProbe.DisposeCount == 1, "try/finally exception path did not dispose exactly once");
        Require(usingProbe.TouchCount == manualProbe.TouchCount, "exception paths performed different work");
    }

    private static void VerifyEquivalentLifetimeBoundary()
    {
        var usingTracker = new LifetimeTracker();
        using (var lease = usingTracker.Acquire(1_024))
        {
            Require(usingTracker.OutstandingBytes == 1_024, "using resource was not live inside its scope");
            lease.Touch();
        }
        Require(usingTracker.OutstandingBytes == 0, "using resource remained live after its scope");

        var manualTracker = new LifetimeTracker();
        var manualLease = manualTracker.Acquire(1_024);
        try
        {
            Require(manualTracker.OutstandingBytes == 1_024, "manual resource was not live inside try");
            manualLease.Touch();
        }
        finally
        {
            manualLease.Dispose();
        }
        Require(manualTracker.OutstandingBytes == 0, "manual resource remained live after finally");
    }

    private static void Require(bool condition, string message)
    {
        if (!condition)
        {
            throw new InvalidOperationException(message);
        }
    }

    private sealed class CountingDisposable : IDisposable
    {
        public int DisposeCount { get; private set; }
        public int TouchCount { get; private set; }

        public void Touch() => TouchCount++;
        public void Dispose() => DisposeCount++;
    }

    private sealed class LifetimeTracker
    {
        public int OutstandingBytes { get; private set; }

        public Lease Acquire(int bytes)
        {
            OutstandingBytes += bytes;
            return new Lease(this, bytes);
        }

        internal void Release(int bytes) => OutstandingBytes -= bytes;
    }

    private sealed class Lease : IDisposable
    {
        private LifetimeTracker? _owner;
        private readonly int _bytes;

        public Lease(LifetimeTracker owner, int bytes)
        {
            _owner = owner;
            _bytes = bytes;
        }

        public void Touch()
        {
            _ = _owner ?? throw new ObjectDisposedException(nameof(Lease));
        }

        public void Dispose()
        {
            var owner = Interlocked.Exchange(ref _owner, null);
            owner?.Release(_bytes);
        }
    }

    private sealed class ExpectedException : Exception
    {
    }
}
