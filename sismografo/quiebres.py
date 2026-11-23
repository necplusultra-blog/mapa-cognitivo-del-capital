import numpy as np

def seg_ssr(y):
    n = len(y); x = np.arange(n)
    X = np.column_stack([np.ones(n), x])
    b, res, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(((y - X @ b) ** 2).sum())

def breaks(y, years, h=8, mmax=5):
    y = np.asarray(y, float); n = len(y)
    cost = np.full((n + 1, n + 1), np.inf)
    for i in range(n):
        for j in range(i + h, n + 1):
            cost[i, j] = seg_ssr(y[i:j])
    # dp[m][j] = min SSR de dividir y[0:j] en m+1 tramos
    dp = np.full((mmax + 1, n + 1), np.inf); arg = np.zeros((mmax + 1, n + 1), int)
    dp[0] = cost[0]
    for m in range(1, mmax + 1):
        for j in range((m + 1) * h, n + 1):
            cand = [dp[m - 1, i] + cost[i, j] for i in range(m * h, j - h + 1)]
            k = int(np.argmin(cand)); dp[m, j] = cand[k]; arg[m, j] = m * h + k
    bics = []
    for m in range(mmax + 1):
        if not np.isfinite(dp[m, n]): continue
        k = 3 * m + 2
        bics.append((n * np.log(dp[m, n] / n) + k * np.log(n), m))
    _, m = min(bics)
    bps, j = [], n
    for mm in range(m, 0, -1):
        i = arg[mm, j]; bps.append(i); j = i
    return sorted(int(years[i]) for i in bps)

