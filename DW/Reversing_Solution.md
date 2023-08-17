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
