import math
from lcg import LinearCongruentialGenerator
from bbs import BlumBlumShub

def exp_mod(base, exp, mod):
    # função para calcular (base^exp) % mod usando exponenciação modular rápida
    result = 1
    base = base % mod
    while exp > 0:
        # se o expoente for ímpar, multiplica o resultado por base
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod

    return result


def miller_rabin(n, rng):
    # testes básicos: n pequeno, negativo ou par
    if n == 2 or n == 3:
        return True
    elif n <= 1 or n % 2 == 0:
        return False

    # deve-se escrever n - 1 como 2^k * q, k > 0, q ímpar
    k, q = 0, n - 1
    while q % 2 == 0:
        # q ainda é par, então divide por 2 e incrementa k
        # até que d seja ímpar
        q //= 2
        k += 1

    # print(k, q)

    # quantidade de bits necessários para representar a (1 < a < n - 1)
    bits = math.floor(math.log2(n-1)) + 1

    # testes de Miller-Rabin
    for _ in range(k):
        # gera um a dentro do intervalo [2, n - 2]
        a = 2 + rng.next_bits(bits) % (n - 3)

        # x = a^q mod n
        x = exp_mod(a, q, n)

        # se x == 1 ou x == n - 1, então n é provavelmente primo
        if x == 1 or x == n - 1:
            continue

        # como ja temos x = a^q mod n, fazer x^2 obtem-se:
        # x^2 = (a^q mod n)^2 = (a^q)^2 mod n = a^(2q) mod n
        # sucessivamente
        # (x^2)^2 = ((a^q mod n)^2)^2 = (a^q)^2*2 mod n = a^(4q) mod n
        for _ in range(k - 1):
            # a^((2^i)*q) mod n
            x = exp_mod(x, 2, n)
            if x == n - 1:
                break
        else:
            # se não encontrar nenhum x tal que x ≡ n-1 (mod n), n é composto
            return False

    # se passou todas as rodadas, n provavelmente é primo
    return True


# Example usage
if __name__ == "__main__":
    n = 561

    # decide random number generator
    lcg = False
    if lcg:
        rng = LinearCongruentialGenerator(m=2**32, a=1664525, c=1013904223, x0=42)
    else:
        p = 3000000019
        q = 4000000007
        rng = BlumBlumShub(p, q)

    if miller_rabin(n, rng):
        print(f"{n} is probably prime.")
    else:
        print(f"{n} is composite.")
