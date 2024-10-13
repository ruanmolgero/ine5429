# import random
import time
import sympy
from lcg import LinearCongruentialGenerator


def gcd(a, b):
    # algoritmo de euclides para calcular o gcd
    # a > b, se não, troca a poor b e vice-versa
    if a < b:
        a, b = b, a

    while b != 0:
        a, b = b, a % b
    return a


def next_usable_prime(n):
    # função para achar o próximo primo usável pelo bbs (congruente a 3 mod 4)
    p = sympy.nextprime(n)
    while p % 4 != 3:
        p = sympy.nextprime(p)
    return p


class BlumBlumShub:
    # 1: escolher 2 numeros primos (p e q) grandes que sejam congruentes a 3 mod 4
    # ou seja, (p mod 4) = (q mod 4) = 3, ex: 7 e 11.
    # 2: fazer n = p * q
    # 3: escolher número s (seed) que é um primo relativo a n (nem p nem q podem dividir s)
    # para inicializar o algoritmo (seed será o "x_(-1)")
    def __init__(self, p, q, seed=None):
        if p % 4 != 3 or q % 4 != 3:
            raise ValueError("p e q devem ambos ser congruentes a 3 mod 4")

        self.n = p * q

        if seed is None:
            lcg = LinearCongruentialGenerator(
                m=2**128, a=12345678, c=12345, x0=42)

            # garantindo que a seed tem 64 bit e esta dentro da faixa de 0 <= seed < n
            seed = lcg.next_with_bit_length(64) % self.n
            while gcd(seed, self.n) != 1:
                seed = lcg.next_with_bit_length(64)

        # x pode ser interpretado como o estado atual do gerador
        self.x = seed % self.n

    def next_bit(self):
        self.x = (self.x ** 2) % self.n
        # print(f"Xi = {self.x} \t{self.x & 1}")
        # extraindo LSB
        return self.x & 1

    def next_bits(self, bit_length):
        bits = 0
        for _ in range(bit_length):
            # abrindo espaço para o próximo bit e o concatenando
            bits = (bits << 1) | self.next_bit()
        return bits


if __name__ == "__main__":
    teste = False

    if teste:
        # valores do livro do stallings
        bbs = BlumBlumShub(p=383, q=503, seed=101355)
        for _ in range(20):
            print(bbs.next_bit())
            print()
    else:
        num_bits = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

        for nb in num_bits:
            # criar um BBS a cada iteração do for para poder
            # medir o tempo corretamente
            p = next_usable_prime(3 * 10**9)
            q = next_usable_prime(4 * 10**9)
            bbs = BlumBlumShub(p, q)

            dif_times = []
            for i in range(100000):
                start_time = time.time()
                generatetd_number_bits = bbs.next_bits(nb)
                # bits = bbs.next_bits(nb)
                final_time = time.time()
                dif_times.append(final_time - start_time)

            avg_time = sum(dif_times) / len(dif_times)
            print(f"--- {nb} bits ---")
            print(f"Average time: {avg_time} seconds")

            # print(f"{nb} bits gerados: {bits:040b}")
            # print(f"{nb} bits gerados: {bits:b}")
