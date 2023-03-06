# lambda-to-ski
Lambda to SKI translator

## 사용법
* Python Interpreter에서 다음처럼 lambda_expr.py의 모든 요소를 import해서 사용한다.
```
from lambda_expr import *
```
* Python으로 lambda_expr.py를 직접 실행하면 예제 테스트를 행한다.

## Lambda expression을 위한 추상 문법
* Lambda expression을 위한 문법 : Lam(variable list, lambda term)
* Application을 위한 문법 : App(lambda terms)
* variable은 string으로 나타낸다.
* 예시
```
add = Lam(['m', 'n', 'f', 'x'], App('m', 'f', App('n', 'f', 'x')))
one = Lam(['f', 'x'], App('f', 'x'))
```

## 정의한 함수 설명
* Lam(v, e) -- variable list(v)와 lambda term(e)를 받아 해당하는 Abstraction의 내부 표현을 리턴한다.
* App(*e_tuple) -- 복수의 lambda term(e_tuple)을 받아 그것들에 Application을 취한 내부 표현을 리턴한다.
* free_vars(term) -- term의 free variable들을 set의 형태로 리턴한다.
* translate(term) -- 임의의 Lambda expression을 S, K, I combinator로 구성된 expression으로 번역한다.
* print_lam_expr(expr) -- 내부 표현으로 구성된 Lambda expression을 읽기 쉽게 출력한다.
* print_ski_expr(expr) -- 내부 표현으로 구성된 S, K, I combinator expression을 읽기 쉽게 출력한다.
