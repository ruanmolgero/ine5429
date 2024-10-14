import time

# implementação do linear congruential generator (lgc)
# o lgc é definido pela seguinte equação de recorrência:
#
# Xn+1 = (aXn + c) mod m
#
# onde:
#   m é o módulo, 0 < m
#   a é o multiplicador, 0 < a < m
#   c é o incremento, 0 <= c < m
#   x0 é a semente, 0 <= x0 < m

#REF STALLINGS p260


class LinearCongruentialGenerator:
    # definição do construtor como os atributos sendo os
    # parâmetros da equação de recorrência
    def __init__(self, m, a, c, x0):
        self.m = m
        self.a = a
        self.c = c
        self.x = x0

    # implementação da equação de recorrência (retorna Xn+1)
    # leva em consideração self.x portando cada execução atualiza
    # o valor de self.x para o novo valor atual
    def next(self):
        self.x = (self.a * self.x + self.c) % self.m
        return self.x

    # reimplementação da equação de recorrência agora com parâmetro bit_length
    # para gerar um número com "bit_length" bits
    def next_bits(self, bit_length):
        while self.x.bit_length() < bit_length:
            self.next()
            # print(self.x)
            # print(self.x.bit_length() < bit_length)
        # return self.x, self.x.bit_length()
        return self.x


if __name__ == "__main__":
    teste = False

    # lgc = LinearCongruentialGenerator(m=2**2048, a=12345678, c=12345, x0=42)
    # print(lgc.next_bits(2048))

    if teste:
        # Exemplo de uso:
        # teste inicial usando os valores do livro do stallings
        # para garantir que a implementação está correta
        lgc = LinearCongruentialGenerator(m=32, a=7, c=0, x0=1)
        for i in range(10):
            print(lgc.next())

        print()

        # observa-se que o m é um "limitante", portanto os valores de x ficarão entre 0 e m-1
        # como 32 == 2**5, os valores de x terão no máximo 5 bits
        # com os parametros acima, observa-se uma repetição após o 4º número {7, 17, 23, 1, 7...}

        # para m=32, a=5, c=0, x0=1 tem-se:
        lgc = LinearCongruentialGenerator(m=32, a=5, c=0, x0=1)
        for i in range(10):
            print(lgc.next())

    else:
        # deseja-se gerar um número com 40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048 e 4096 bits:
        # será usado então o método next_bits criado para garantir o número de bits desejado
        num_bits = [40, 56, 80, 128, 168, 224, 256, 512, 1024, 2048, 4096]

        for nb in num_bits:
            lgc = LinearCongruentialGenerator(
                m=2**nb, a=12345678, c=12345, x0=42)

            dif_times = []
            for i in range(100000):
                start_time = time.time()
                generatetd_number = lgc.next_bits(nb)
                final_time = time.time()
                dif_times.append(final_time - start_time)

            avg_time = sum(dif_times) / len(dif_times)
            print(f"--- {nb} bits ---")
            print(f"Average time: {avg_time} seconds")
