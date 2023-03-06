# 20191396 장기훈

LAM_SIGN = '_lam'
APP_SIGN = '_app'
S_SIGN = '_s'
K_SIGN = '_k'
I_SIGN = '_i'


def Lam(v, e):
    """ variable list(v)와 lambda term(e)를 받아
        해당하는 abstraction의 내부 표현을 리턴
    """
    # v가 list일 경우 원소를 하나씩 꺼내서,
    # abstraction이 파라미터를 하나씩 가지도록 내부 표현을 구성 (recursive하게 구현)
    if isinstance(v, list):
        if len(v) == 1:
            return Lam(v[0], e)
        return Lam(v[0], Lam(v[1:], e))

    return (LAM_SIGN, v, e)


def App(*e_tuple):
    """ 복수의 lambda term(e_tuple)을 받아
        application을 취한 내부 표현을 리턴
    """
    if(len(e_tuple) < 2):
        print("error in App")
        return (APP_SIGN, e_tuple[0])

    res = (APP_SIGN, e_tuple[0], e_tuple[1])
    
    # e_tuple의 원소가 3개 이상일 경우 3번째 원소부터 다시 application 취하도록 함
    for i in range(2, len(e_tuple)):
        res = (APP_SIGN, res, e_tuple[i])

    return res


def free_vars(term):
    """ term의 free variable들을 set의 형태로 리턴
    """
    if not isinstance(term, tuple):
        return set([term])
    if term[0] == LAM_SIGN:    # term이 abstraction인 경우
        frees = free_vars(term[2])
        if term[1] in frees:
            frees.remove(term[1])
        return frees
    if term[0] == APP_SIGN:    # term이 application인 경우
        frees = free_vars(term[1])
        frees.update(free_vars(term[2]))
        return frees

    print('error in free_vars. term: ')


def translate(term):
    """ 임의의 Lambda expression을 S,K,I combinator로 구성된 expression으로 번역
    """
    if not isinstance(term, tuple):  # Rule 1
        return term
    if term[0] == APP_SIGN:  # Rule 2
        return App(translate(term[1]), translate(term[2]))
    if term[0] == LAM_SIGN:
        if term[1] not in free_vars(term[2]):  # Rule 3
            return App(K_SIGN, translate(term[2]))
        if term[1] == term[2]:  # Rule 4
            return I_SIGN
        if isinstance(term[2], tuple):
            if term[2][0] == LAM_SIGN and (term[1] in free_vars(term[2][2])):  # Rule 5
                return translate(Lam(term[1], translate(Lam(term[2][1], term[2][2]))))
            if term[2][0] == APP_SIGN and ((term[1] in free_vars(term[2][1])) or (term[1] in free_vars(term[2][2]))):  # Rule 6
                return App(S_SIGN, translate(Lam(term[1], term[2][1])), translate(Lam(term[1], term[2][2])))
    
    print("error in translate. term:", term)


def print_lam_expr(expr, new_line = True):
    """ 내부 표현으로 구성된 Lambda expression을 읽기 쉽게 출력
        new_line이 True이면 출력 후 개행하고 False이면 개행하지 않음
    """
    if not isinstance(expr, tuple):    # epxr이 tuple이 아닐 경우
        print(expr, end=' ')
    if expr[0] == LAM_SIGN:    # expr이 abstraction일 경우
        print('\\', end='')
        print_lam_expr(expr[1], new_line=False)
        print('->', end=' ')
        print_lam_expr(expr[2], new_line=False)
    if expr[0] == APP_SIGN:    # expr이 application일 경우
        if isinstance(expr[1], tuple):
            if expr[1][0] == LAM_SIGN:    # application의 첫번째 인자가 abstraction인 경우
                print('(', end=' ')
                print_lam_expr(expr[1], new_line=False)
                print(')', end=' ')
            else:
                print_lam_expr(expr[1], new_line=False)
        else:
            print_lam_expr(expr[1], new_line=False)
        if isinstance(expr[2], tuple):
            print('(', end=' ')
            print_lam_expr(expr[2], new_line=False)
            print(')', end=' ')
        else:
            print_lam_expr(expr[2], new_line=False)
            
    if new_line:
        print()


def print_ski_expr(expr, new_line = True):
    """ 내부 표현으로 구성된 S, K, I combinator expression을 읽기 쉽게 출력
        new_line이 True이면 출력 후 개행하고 False이면 개행하지 않음
    """
    # expr이 application이 아닐 경우
    if not isinstance(expr, tuple):
        if expr == S_SIGN:
            print('S', end='')
        elif expr == K_SIGN:
            print('K', end='')
        elif expr == I_SIGN:
            print('I', end='')
        else:
            print('\nerror in print_ski_expr. expr:', expr)
        return

    # expr이 application일 경우
    print_ski_expr(expr[1], new_line = False)
    if isinstance(expr[2], tuple):
        print('(', end='')
    print_ski_expr(expr[2], new_line = False)
    if isinstance(expr[2], tuple):
        print(')', end='')
    
    if new_line:
        print()


if __name__ == "__main__":
    print('- lambda-to-ski')
    print('- 20191396 장기훈')
    print('- 예제 테스트')

    one = Lam(['f', 'x'], App('f', 'x'))
    two = Lam(['f', 'x'], App('f', App('f', 'x')))
    four = Lam(['f', 'x'], App('f', App('f', App('f', App('f', 'x')))))
    add = Lam(['m', 'n', 'f', 'x'], App('m', 'f', App('n', 'f', 'x')))
    mult = Lam(['m', 'n', 'f'], App('m', App('n', 'f')))

    print('\n1 :', end=' ')
    print_lam_expr(one)
    print('2 :', end=' ')
    print_lam_expr(two)
    print('4 :', end=' ')
    print_lam_expr(four)
    print('add :', end=' ')
    print_lam_expr(add)
    print('mult :', end=' ')
    print_lam_expr(mult)

    print('\ntranslate(add 1 1) :', end=' ')
    print_ski_expr(translate(App(add, one, one)))
    print('\ntranslate(add 2 1) :', end=' ')
    print_ski_expr(translate(App(add, two, one)))
    print('\ntranslate(mult 4 2) :', end=' ')
    print_ski_expr(translate(App(mult, four, two)))
    