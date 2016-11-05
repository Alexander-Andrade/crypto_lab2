import numpy as np
import random
import string


def is_prime(n):
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n

# НОД
def gsd(a, b):
    while b:
        a, b = b, a % b
    return a


# НОД(a,b)=1
def are_coprime(a, b):
    return gsd(a, b) == 1


def are_mod_comparable(a, b, n):
    return a % n == b


class Abonent:

    def __init__(self, alphabet, p):
        self.p = p
        self.alphabet = alphabet
        self.prim_key = self.chose_primary_key()
        self.sec_key = self.chose_secondary_key()

    def chose_primary_key(self):
        coprime = []
        for i in range(2, self.p - 1):
            if are_coprime(i, self.p - 1):
                coprime.append(i)
        return random.choice(coprime)

    def chose_secondary_key(self):
        comparable = []
        for i in range(2, self.p - 1):
            if are_mod_comparable(self.prim_key*i, 1, self.p - 1):
                comparable.append(i)
        return random.choice(comparable)

    def gen_msg(self):
        return ord(random.choice(self.alphabet))

    def firstkey_srypt(self, mu):
        return mu**self.prim_key % self.p

    def secondkey_srypt(self, mu):
        return mu**self.sec_key % self.p

    def __repr__(self):
        return "p={}, prim_key={}, sec_key={}".format(self.p, self.prim_key, self.sec_key)


class Hacker:

    def __init__(self, alphabet, p, abonent1, abonent2):
        self.alphabet = alphabet
        self.p = p
        self.a1 = abonent1
        self.a2 = abonent2
        self.coprime_with_p_minus_1 = self.gen_all_possible_primary_keys()
        self.decode_table = self.fill_table()

    def fill_table(self):
        decode_table = dict()
        for mu in range(2, self.p-1):
            for alpha in self.coprime_with_p_minus_1:
                mu1 = self.encrypt(mu, alpha)
                for beta in self.coprime_with_p_minus_1:
                    mu2 = self.encrypt(mu1, beta)
                    decode_table[mu2] = {}
                    decode_table[mu2][beta] = {}
                    decode_table[mu2][beta][alpha] = {}
                    decode_table[mu2][beta][alpha] = mu
        return decode_table

    def get_msg_keys(self, mu2):
        keys = {}
        a_keys = []
        b_keys = []
        mu = []
        betas = self.decode_table.get(mu2)
        if betas:
            for beta in betas:
                alphas = self.decode_table[mu2].get(beta)
                for alpha in alphas:
                    mu.append(self.decode_table[mu2][beta][alpha])
                    a = self.get_secondary_key(alpha)
                    b = self.get_secondary_key(beta)
                    mu4 = self.get_encrypted_msg(mu2, a, b)

    def get_encrypted_msg(self, mu2, a, b):
        mu3 = self.encrypt(mu2, a)
        return self.encrypt(mu3, b)

    def gen_all_possible_primary_keys(self):
        return [i for i in range(2, self.p - 1) if are_coprime(i, self.p - 1)]

    def get_secondary_key(self, prim_key):
        for i in range(2, self.p - 1):
            if are_mod_comparable(prim_key*i, 1, self.p-1):
                return i

    def encrypt(self, mu, key):
        return mu**key % self.p




if __name__ == "__main__":
    alphabet = np.array(list(string.ascii_lowercase))
    p = 257
    a = Abonent(alphabet=alphabet, p=p)
    b = Abonent(alphabet=alphabet, p=p)
    c = Hacker(alphabet=alphabet, p=p, abonent1=a, abonent2=b)
    print(c.table)
    # print(a1)
    # print(a2)
    # msg = a.gen_msg()
    # mu1 = a.firstkey_srypt(msg)
    # mu2 = b.firstkey_srypt(mu1)
    # mu3 = a.secondkey_srypt(mu2)
    # mu4 = b.secondkey_srypt(mu3)

    # print("msg={},mu1={}, mu2={}, mu3={}, mu4={}".format(msg, mu1, mu2, mu3, mu4))




