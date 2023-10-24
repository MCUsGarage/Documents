# gdb

명령어
- entry: 진입점에 중단점을 설정한 후 실행 
- break(b): 중단점 설정
- continue(c): 계속 실행
- disassemble: 디스어셈블 결과 출력
- u, nearpc, pd: 디스어셈블 결과 가독성 좋게 출력
- x: 메모리 조회
- run(r): 프로그램 처음부터 실행
- context: 레지스터, 코드, 스택, 백트레이스의 상태 출력
- nexti(ni): 명령어 실행, 함수 내부로는 들어가지 않음
- stepi(si): 명령어 실행, 함수 내부로 들어감
- telescope(tele): 메모리 조회, 메모리값이 포인터일 경우 재귀적으로 따라가며 모든 메모리값 출력
- vmmap: 메모리 레이아웃 출력