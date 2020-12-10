import sys

def ror12(x):
    return (x << 20 | x >> 12) & 0xffffffff

def to_dwords(res):
    out = []
    for i in xrange(8):
        t = (res[i*4+3] << 24)| (res[i*4+2] << 16)| (res[i*4+1] << 8) | res[i*4]
        out.append(t)
    return out

def from_dwords(out):
    res = []
    for i in xrange(8):
        res.append(out[i] & 0xff)
        res.append((out[i] >> 8) & 0xff)
        res.append((out[i] >> 16) & 0xff)
        res.append((out[i] >> 24) & 0xff)
    return res

def rev_func2(res):
    dw = to_dwords(res)
    dw[7] = dw[7] ^ dw[6]
    dw[6] = ror12(dw[6]) ^ dw[5]
    dw[5] = ror12(dw[5]) ^ dw[4]
    dw[4] = ror12(dw[4]) ^ dw[3]
    dw[3] = ror12(dw[3]) ^ dw[2]
    dw[2] = ror12(dw[2]) ^ dw[1]
    dw[1] = ror12(dw[1]) ^ dw[0]
    dw[0] = ror12(dw[0])
    return from_dwords(dw)

def rev_func1(res, funge):
    num = (32 + 17 * 8) % len(funge)
    idx = 32
    for _ in xrange(8):
        idx -= 4
        num = (num - 17) % len(funge)
        res[idx+3] = (res[idx+3] - funge[(num + 50) % len(funge)]) & 0xff
        res[idx+2] = (res[idx+2] - funge[(num + 40) % len(funge)]) & 0xff
        res[idx+1] = (res[idx+1] - funge[(num + 30) % len(funge)]) & 0xff
        res[idx]   = (res[idx]   - funge[(num + 20) % len(funge)]) & 0xff
    return res

def rev_func4(res, n):
    arr = [
        0x1d, 0x0d, 0x10, 0x14,
        0x04, 0x16, 0x15, 0x18,
        0x1f, 0x0b, 0x01, 0x00,
        0x09, 0x07, 0x08, 0x05,
        0x19, 0x06, 0x13, 0x0f,
        0x17, 0x1b, 0x03, 0x02,
        0x1a, 0x12, 0x1e, 0x1c,
        0x0a, 0x0c, 0x11, 0x0e
    ]
    n_ = n + 32
    print(res)
    for _ in xrange(16):
        n_ -= 2
        idx0 = arr[n_ % 32]
        idx1 = arr[(n_ + 1) % 32]
        t = res[idx0]
        x = (res[idx1] - (t % 50)) & 0xff
        y = (t - (x % 70)) & 0xff
        res[idx0] = x
        res[idx1] = y
        print(res)
    return res

def solve(fn):
    f = open(fn, 'rb')
    binary = f.read()
    f.close()

    result = list(map(ord, binary[0x8238:0x8258]))
    funge = list(map(ord, binary[0x2940:0x2980]))
    print ''.join(map(chr, result))
    result = rev_func2(result)
    print ''.join(map(chr, result))
    result = rev_func4(result, 13)
    print ''.join(map(chr, result))
    result = rev_func1(result, funge)
    print ''.join(map(chr, result))
    result = rev_func2(result)
    print ''.join(map(chr, result))
    result = rev_func4(result, 1)
    print ''.join(map(chr, result))
    result = rev_func1(result, funge)

    print ''.join(map(chr, result))

if __name__ == '__main__':
    solve(sys.argv[1])