import math

def create_ladner_fisher(n):
    """Utworzenie szablonu drzewa prefiksowego typu Ladnera-Fishera"""
    floors = math.ceil(math.log2(n))
    prefix_tree = []
    for i in range(floors):
        tmp_table = []
        tmp_counter = 0
        is_black = False
        for j in range(n):
            if tmp_counter == 2 ** i:
                tmp_counter = 0
                is_black = not is_black
            if is_black:
                tmp_table.append(1)
            else:
                tmp_table.append(0)
            tmp_counter += 1
        prefix_tree.append(tmp_table)
    return prefix_tree


def preprocessing(n, modulo, A, B):
    K = decimal_to_binary(2**n-modulo,n)

    A_prim = [0 for x in range(n)]
    B_prim = [0 for x in range(n + 1)]
    for i in range(len(K)):
        a = A[i]
        b = B[i]
        k = K[i]
        if k == 0:
            if a ^ b:  # A'[i]
                A_prim[i] = 1
            if a and b:  # B'[i]
                B_prim[i + 1] = 1
        else:
            if not (a ^ b):  # A'[i]
                A_prim[i] = 1
            if a or b:
                B_prim[i + 1] = 1  # B'[i]

    H = [0 for x in range(n)]
    P = [0 for x in range(n)]
    G = [0 for x in range(n)]
    H_prim = [0 for x in range(n)]
    P_prim = [0 for x in range(n)]
    G_prim = [0 for x in range(n)]
    for i in range(len(K)):
        a = A[i]
        b = B[i]
        a_prim = A_prim[i]
        b_prim = B_prim[i]
        if a ^ b:  # H[i]
            H[i] = 1
        if a or b:  # P[i]
            P[i] = 1
        if a and b:  # G[i]
            G[i] = 1
        if a_prim ^ b_prim:  # H'[i]
            H_prim[i] = 1
        if a_prim or b_prim:  # P'[i]
            P_prim[i] = 1
        if a_prim and b_prim:  # G'[i]
            G_prim[i] = 1

    # print(f"A = {A}\n"
    #       f"B = {B}\n"
    #       f"K = {K}\n\n"
    #       f"A'= {A_prim}\n"
    #       f"B'= {B_prim}\n\n"
    #       f"H = {H}\n"
    #       f"P = {P}\n"
    #       f"G = {G}\n\n"
    #       f"H'= {H_prim}\n"
    #       f"P'= {P_prim}\n"
    #       f"G'= {G_prim}\n\n")
    return multiplexing_and_sum_computing(H, H_prim, G, G_prim,
                                          P, P_prim, B_prim)

def parallel_prefix(G, P):
    n = len(G)

    ladner_fisher = create_ladner_fisher(n)

    # Stworzenie tablic dla sum prefiksowych
    prefix_g = G
    prefix_p = P

    for i in range(len(ladner_fisher)):
        counter = 0
        for j in range(n):
            if ladner_fisher[i][j] == 1:
                prefix_g[j] = prefix_g[j] or (prefix_g[2**(i)-1
                                        + counter*(2**(i+1))] and
                                              prefix_p[j])
                prefix_p[j] = prefix_p[j] and prefix_p[2**(i)-1
                                        + counter*(2**(i+1))]
            elif j!=0 and ladner_fisher[i][j-1] == 1:
                counter += 1

    return prefix_g

def multiplexing_and_sum_computing(H, H_prim, G, G_prim, P,
                                   P_prim, B_prim):
    n = len(H)
    C = parallel_prefix(G, P)
    C_prim = parallel_prefix(G_prim, P_prim)

    C_prim[n - 1] = C_prim[n - 1] or B_prim[n]

    S = [0 for i in range(n)]
    if C_prim[n - 1]:
        for i in range(n - 1):
            S[i + 1] = H_prim[i + 1] ^ C_prim[i]
        S[0] = H_prim[0]
    else:
        for i in range(n - 1):
            S[i + 1] = H[i + 1] ^ C[i]
        S[0] = H[0]
    return binary_to_decimal(S)


def binary_to_decimal(S):
    result = 0
    for i in range(len(S)):
        result += S[i] * 2 ** i
    return result


def decimal_to_binary(number, n):
    table = []
    while number > 0:
        table.append(number % 2)
        number //= 2

    # Uzupełnienie tablicy zerami do długości n
    while len(table) < n:
        table.append(0)

    return table

def check_if_modulo_is_valid(modulo):
    i = 0
    while modulo >= (2 ** i):
        i += 1
    if modulo < 5 or modulo == 2 ** (i - 1) or modulo == \
                    (2 ** i) - 1 or modulo == (2 ** i) - 2:
        return False
    return True

def calculate_bits(modulo):
    i = 3
    while modulo > (2 ** i) - 3:
        i += 1

    return i



print("---- SUMATOR MODULARNY 2^n - K ----")

#input
modulo = int(input(f"Podaj modulo: "))
while check_if_modulo_is_valid(modulo) is False:
   modulo = int(input(f"Podaj poprawne modulo: "))

n = calculate_bits(modulo)

#zapisanie liczb A i B jako tablice bitów
A_dec = int(input(f"Podaj liczbę A z przedziału "
                  f"[0,{modulo - 1}]: "))
while A_dec not in range(0,modulo):
    A_dec = int(input(f"Podaj liczbę A z przedziału "
                      f"[0,{modulo - 1}]: "))
B_dec = int(input(f"Podaj liczbę B z przedziału "
                  f"[0,{modulo - 1}]: "))
while B_dec not in range(0,modulo):
    B_dec = int(input(f"Podaj liczbę B z przedziału "
                      f"[0,{modulo - 1}]: "))

A = decimal_to_binary(A_dec, n)
B = decimal_to_binary(B_dec, n)

print(f"S = {preprocessing(n, modulo, A, B)}")



