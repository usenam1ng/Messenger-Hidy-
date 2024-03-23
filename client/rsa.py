import random


def encryption(private_key, cipher):
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in cipher]
    return ''.join(plain)
    

def decryption(public_key, plaintext):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def is_prime(num):
    test_count = 5
    if num == 2 or num == 3:
        return True
    if num < 2 or num % 2 == 0:
        return False

    def check(a, s, d, n):
        x = pow(a, d, n)
        if x == 1:
            return True
        for _ in range(s - 1):
            if x == n - 1:
                return True
            x = pow(x, 2, n)
        return x == n - 1

    s = 0
    d = num - 1
    while d % 2 == 0:
        d >>= 1
        s += 1

    for _ in range(test_count):
        a = random.randrange(2, num - 1)
        if not check(a, s, d, num):
            return False
    return True

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def generate_keypair():
    p = 0
    q = 0
    while True:
        p = random.getrandbits(1024)
        q = random.getrandbits(1024)
        if is_prime(p) and is_prime(q):
            break

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    g = egcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g, x, y = egcd(e, phi)

    d = x % phi
    return (e, n), (d, n)