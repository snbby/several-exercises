def code6_seq(n: int) -> str:
    if n < 0:
        raise ValueError('n must be >= 0')

    total_capacity = 0

    for s in range(0, 7):
        d = 6 - s
        block = (10 ** d) * (26 ** s)
        if n < total_capacity + block:
            offset = n - total_capacity
            number_index = offset % (10 ** d)
            suffix_index = offset // (10 ** d)

            # digits part
            digits = f'{number_index:0{d}d}' if d > 0 else ''

            if s == 0:
                letters = ""
            else:
                letters = []
                x = suffix_index
                for _ in range(s):
                    letters.append(chr(ord('A') + (x % 26)))
                    x //= 26
                letters = ''.join(reversed(letters))

            return digits + letters
        total_capacity += block

    raise ValueError('n too large: exceeds the 6-character code space')

    