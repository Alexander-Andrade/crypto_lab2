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

    def __init__(self, alphabet,a1, a2):
        self.alphabet = alphabet
        self.a1 = a1
        self.a2 = a2
        self.mu_dict = dict()

    def __m2_for_alphabet(self):
        for letter in range(self.alphabet):
            pass



if __name__ == "__main__":
    alphabet = np.array(list(string.ascii_lowercase))
    p = 257
    a1 = Abonent(alphabet=alphabet, p=p)
    a2 = Abonent(alphabet=alphabet, p=p)
    print(a1)
    print(a2)
    msg = a1.gen_msg()
    mu1 = a1.firstkey_srypt(msg)
    mu2 = a2.firstkey_srypt(mu1)
    mu3 = a1.secondkey_srypt(mu2)
    mu4 = a2.secondkey_srypt(mu3)

    print("msg={},mu1={}, mu2={}, mu3={}, mu4={}".format(msg, mu1, mu2, mu3, mu4))




