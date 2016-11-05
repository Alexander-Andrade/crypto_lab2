import random
import string
import copy


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


def encrypt(mu, key, p):
    return mu ** key % p


def gen_all_possible_primary_keys(p):
    return [i for i in range(2, p - 1) if are_coprime(i, p - 1)]


def get_secondary_key(prim_key, p):
    for i in range(2, p - 1):
        if are_mod_comparable(prim_key * i, 1, p - 1):
            return i


def Fermats_theorem_check(alpha, beta, a, b, p):
    return are_mod_comparable(alpha*beta*a*b, 1, p-1)


class Abonent:

    def __init__(self, alphabet, p):
        self.p = p
        self.alphabet = alphabet
        self.prim_key = self.chose_primary_key()
        self.sec_key = get_secondary_key(self.prim_key, self.p)

    def chose_primary_key(self):
        coprime = gen_all_possible_primary_keys(self.p)
        return random.choice(coprime)

    def gen_msg(self):
        return ord(random.choice(self.alphabet))

    def encrypt_primary(self, mu):
        return encrypt(mu=mu, key=self.prim_key, p=self.p)

    def encrypt_secondary(self, mu):
        return encrypt(mu=mu, key=self.sec_key, p=self.p)

    def __repr__(self):
        return "p={}, prim_key={}, sec_key={}".format(self.p, self.prim_key, self.sec_key)


class Hacker:

    def __init__(self, alphabet, p):
        self.alphabet = alphabet
        self.p = p
        self.possible_primary_keys = gen_all_possible_primary_keys(p)
        self.decode_table = self.fill_table()

    def fill_table(self):
        decode_table = dict()
        for mu in range(2, self.p-1):
            for alpha in self.possible_primary_keys:
                mu1 = encrypt(mu=mu, key=alpha, p=self.p)
                for beta in self.possible_primary_keys:
                    mu2 = encrypt(mu=mu1, key=beta, p=self.p)
                    if not decode_table.get(mu2):
                        decode_table[mu2] = {}
                    if not decode_table[mu2].get(beta):
                        decode_table[mu2][beta] = {}
                    decode_table[mu2][beta][alpha] = {}
                    decode_table[mu2][beta][alpha] = mu
        return decode_table

    def get_msg_keys(self, mu2):
        keys = []
        betas = self.decode_table.get(mu2)
        if betas:
            for beta in betas:
                alphas = self.decode_table[mu2].get(beta)
                for alpha in alphas:
                    mu = self.decode_table[mu2][beta][alpha]
                    a = get_secondary_key(prim_key=alpha, p=self.p)
                    b = get_secondary_key(prim_key=beta, p=self.p)
                    mu3 = encrypt(mu=mu2, key=a, p=self.p)
                    mu4 = encrypt(mu=mu3, key=b, p=self.p)
                    if mu == mu4:
                        keys.append((alpha, beta, a, b))
        return keys


if __name__ == "__main__":
    alphabet = list(string.ascii_lowercase)
    p = 257
    a = Abonent(alphabet=alphabet, p=p)
    b = Abonent(alphabet=alphabet, p=p)
    c = Hacker(alphabet=alphabet, p=p)
    keys = None
    for i in range(50):
        mu = a.gen_msg()
        mu1 = a.encrypt_primary(mu)
        mu2 = b.encrypt_primary(mu1)
        mu3 = a.encrypt_secondary(mu2)
        mu4 = b.encrypt_secondary(mu3)

        print(mu)
        print(mu4)
        keys = c.get_msg_keys(mu2=mu2)
        print("len = {}".format(len(keys)))
        if i > 0:
            keys = set(keys).intersection(old_keys)
        old_keys = copy.deepcopy(keys)

    print(keys)
    # for mu, alpha, beta, a, b in keys:
    #     if mu == mu4:
    #         print(mu, alpha, beta, a, b)
    # for mu, alpha, beta, a, b in keys:
    #     if not Fermats_theorem_check(alpha=alpha, beta=beta, a=a, b=b, p=257):
    #         print("not")



