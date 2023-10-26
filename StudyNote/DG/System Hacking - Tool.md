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


# pwntools

## Download for M1 mac
```bash
$ brew install cmake
$ pip install unicorn
$ pip install pwntools
```

## Manual

https://docs.pwntools.com/en/latest/

자주 쓰이는 명령어

1. process:  로컬 바이너리 대상 익스플로잇 
2. remote: 원격 서버 대상 익스플로잇
3. send: 프로세스에 데이터를 전송
4. recv: 프로세스에서 데이터를 수신 (cf. recvn)
5. packing: 리틀 엔디언 값을 바이트로 변환
6. unpacking: 바이트를 리틀엔디언 값으로 변환
7. interactive: 셸을 획득했거나 익스플로잇의 특정 상황에 직접 입력을 주면서 출력을 확인함
8. elf: elf 헤더 정보 참조
9. context.log: 익스플로잇 디버깅용 로그
10. context.arch: 아키텍처 정보 지정
11. shellcraft: 아키텍처에 맞는 셸 코드 제공/ 실행 등
12. asm: 아키텍처에 맞는 어셈블 명령어 사용

