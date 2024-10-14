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


def fermat(n, k, rng):
    if n == 2:
        return True

    if n < 2 or n % 2 == 0:
        return False

    # quantidade de bits necessários para representar a (1 < a < n - 1)
    # para usar em rng.next_bits(bits)
    bits = math.floor(math.log2(n-1)) + 1

    # tetsta o número n k vezes
    for _ in range(k):
        a = 2 + rng.next_bits(bits) % (n - 3)

        # Calcula a^(n-1) mod n
        if exp_mod(a, n-1, n) != 1:
            return False  # Se falhar o teste, n é composto

    return True  # Se passar todos os testes, n é "provavelmente primo"


if __name__ == "__main__":
    n = 561  # Número a ser testado (composto de Carmichael)
    k = 5  # Número de iterações do teste de Fermat

    # decide random number generator
    lcg = True
    if lcg:
        rng = LinearCongruentialGenerator(m=2**128, a=12345678, c=12345, x0=42)
    else:
        p = 3000000019
        q = 4000000007
        rng = BlumBlumShub(p, q)

    if fermat(n, k, rng):
        print(f"{n} é provavelmente primo.")
    else:
        print(f"{n} é composto.")
