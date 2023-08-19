# 1 Reversing Basic Challenge #0

https://dreamhack.io/wargame/challenges/14

이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.

해당 바이너리를 분석하여 correct를 출력하는 입력값을 찾으세요!

획득한 입력값은 DH{} 포맷에 넣어서 인증해주세요.

예시) 입력 값이 Apple_Banana일 경우 flag는 DH{Apple_Banana}

## Solution

해당 exe file을 다운로드 받은 다음에 Text editor로 문서를 연다.

![exefile](./img/Screenshot%202023-08-17%20at%2010.35.14%20PM.png)

상기 이미지 내 값을 ASCII로 읽으면

43 6F 6D 70 61 72 33 5F 74 68 65 5F 73 74 72 31 6E 67
Compar3_the_str1ng

라는 값을 읽을 수 있으며 해당 값이 flag이다.

</br>
</br>

# 2 Reversing Basic Challenge #1


https://dreamhack.io/wargame/challenges/15

이 문제는 사용자에게 문자열 입력을 받아 정해진 방법으로 입력값을 검증하여 correct 또는 wrong을 출력하는 프로그램이 주어집니다.

해당 바이너리를 분석하여 correct를 출력하는 입력값을 알아내세요.

획득한 입력값은 DH{} 포맷에 넣어서 인증해주세요.

예시) 입력 값이 Apple_Banana일 경우 flag는 DH{Apple_Banana}

## Solution

이 문제도 text editor로 찾을 수 도 있지만, 이번에는 x64 dbg로 정답을 찾아보도록 하자.

![sol2_1](./img/sol2_1.png)

x64 dbg에 exe file을 넣고 ASICC 검색 기능을 사용하면, 이렇게 해당 프로그램에 단서를 찾을 수 있다.

INPUT 쪽을 클릭해서 해당 주소로 이동해보자.

![sol2_2](./img/sol2_2.png)

해당 코드를 읽어보면, Input으로 256 byte string 입력값을 받고, 위의 이미지 내에 Call chall1.7FF7B59A10000 주소 내에 함수에서 해당 Input을 비교하는 함수가 있다는 것을 알 수 있다. 

![sol2_3](./img/sol2_3.png)

해당 주소를 점프하면 비교 할 String 값이 보인다. {Compa~로 시작하는 문장 }