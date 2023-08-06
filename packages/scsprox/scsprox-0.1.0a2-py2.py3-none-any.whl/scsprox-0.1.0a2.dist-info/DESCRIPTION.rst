Converts a CVXPY problem and a dict of CVXPY variables to a fast proximal operator object, which uses CySCS to provide fast evaluation, via one-time matrix stuffing, CySCS factorization caching, and automatic warm-starting of variables.


