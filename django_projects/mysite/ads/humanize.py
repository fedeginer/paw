
# Really simple naturalsize that is missing from django humanize :(
def naturalsize(count):
    fcount = float(count)
    k = 1024                # 1 kb
    m = k * k               # 1024 kb que son 1 MB
    g = m * k               # 1024 MB que son 1 GB
    if fcount < k:
        return str(count) + 'B'
    if fcount >= k and fcount < m:
        return str(int(fcount / (k/10.0)) / 10.0) + 'KB'
    if fcount >= m and fcount < g:
        return str(int(fcount / (m/10.0)) / 10.0) + 'MB'
    return str(int(fcount / (g/10.0)) / 10.0) + 'GB'
