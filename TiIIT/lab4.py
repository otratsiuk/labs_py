from random import randint


def prime_number(num):
    prime_num = num
    for a in range(2, num):
        if a ** prime_num % prime_num != a % prime_num:
            prime_num += 1
            a = 2
    return prime_num


def greatest_common_division(num1, num2):
    while num1 != 0 and num2 != 0:
        if num1 > num2:
            num1 %= num2
        else:
            num2 %= num1
    gcd = num1 + num2
    return gcd


def mutually_prime_number(num):
    mpn = randint(1, 100)
    while greatest_common_division(num, mpn) != 1:
        mpn = randint(1, 100)
    return (mpn)


def make_E(D, L, Q):
    E = randint(1, 100)
    while E * D % L != 1:
        E = randint(1, 100)
    return E


code = []
decode = []
more = 1
while more:
    name = input('enter name: ')
    surname = input('enter surname: ')
    name_length = len(name)
    surname_length = len(surname)
    P = prime_number(name_length)
    Q = prime_number(surname_length)
    if Q == P:
        Q = prime_number(P + 1)
    print('P = ' + str(P))
    print('Q = ' + str(Q))
    N = (P * Q)
    L = (P - 1) * (Q - 1)
    print('L = ' + str(L))
    D = mutually_prime_number(L)
    E = make_E(D, L, Q)
    print('secret key(E, N): ' + '(' + str(E) + ', ' + str(N) + ')')
    print('public key(D, N): ' + '(' + str(D) + ', ' + str(N) + ')')
    print('name code: ', end=' ')
    for i in range(name_length):
        M = ord(name[i])
        M = M - 96      # to numerate capital latin letters from 1 to 26
        code.insert(i, M ** E % N)
        print(code[i], end=' ')
    print('\nname decode: ', end=' ')
    for i in range(name_length):
        decode.insert(i, code[i] ** D % N + 96)
        print(decode[i], end=' ')
    print('\nname was:', end=' ')
    for i in range(name_length):
        print(chr(decode[i]), end='')
    state = input('\nwant to continue?(y/n)')
    if state == 'n':
        more = 0
    else:
        more = 1
        print('\n')
