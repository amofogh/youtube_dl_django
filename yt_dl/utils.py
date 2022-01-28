# convert size to human readable
def bytes_to(byte, to, bsize=1024):
    a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
    r = float(byte)
    return byte / (bsize ** a[to])
