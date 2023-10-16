# 1. Computer Architecture

## 컴퓨터 구조(Computer Architecture)

### 컴퓨터 기능 구조(Architecture)
- 컴퓨터의 효율적인 연산을 위한 기능 설계

종류
1. 폰 노이만 아키텍처
	- CPU + 기억장치 + BUS 
	- 프로그램 내장 방식: 메모리 안에 실행 코드와 데이터가 구분되지 않음
	- 장점: 범용성
	- 단점: 병목현상(명령어와 데이터에 동시 접근 불가능)
2. 하버드 아키텍처
	- 프로그램, 데이터 버스 분리
	- 장점: 폰노이만 대비 빠른 속도(병목현상 완화)
	- 단점: 회로 증가
	- ![pure-harvard](images/Pasted%20image%2020231015115819.png)
1. 수정된 하버드 아키텍처
	- 캐시 메모리도 분리함
	- 한 사이클에 load, store 동시 수행 가능
	- ![](images/Pasted%20image%2020231015115916.png)

### 명령어 집합 구조 (Instruction Set Architecture, ISA)
- CPU가 처리해야하는 명령어 설계

종류 (RISC/ CISC)
- ARM
- MIPS
- RISC-V
- x86, x86-64
- etc...

### 마이크로 아키텍처
- 정의된 명령어 집합을 효율적으로 처리하도록 CPU 회로 설계

종륲
- 캐시 설계
- 파이프라이닝
- 슈퍼 스칼라
- 분기 예측
- 비순차적 명령어 처리
- etc...

### 하드웨어 및 컴퓨팅 방법에 대한 설계
- DMA(Direct Memory Access) 
- etc...



## x86-64 아키텍처

### 레지스터 종류

범용 레지스터(General Register) 

0. RAX (Accumulator register). 산술 연산에 사용.
1. RCX (Counter register). 시프트/회전 연산과 루프에서 사용.
2. RDX (Data register). 산술 연산과 I/O 명령에서 사용.
3. RBX (Base register). 데이터의 주소를 가리키는 포인터로 사용. (세그멘티드 모드에서는 세그멘트 레지스터 DS로 존재)
4. RSP (Stack Pointer register). 스택의 최상단을 가리키는 포인터로 사용.
5. RBP (Stack Base Pointer register). 스택의 베이스를 가리키는 포인터로 사용.
6. RSI (Source Index register). 스트림 명령에서 소스를 가리키는 포인터로 사용.
7. RDI (Destination Index register). 스트림 명령에서 도착점을 가리키는 포인터로 사용.
8. R8~R15
9. 

세그먼트 레지스터(Segment Register)  - 16 bit
1. Stack Segment (SS). 스택을 가리킨다.
2. Code Segment (CS). 코드를 가리킨다.
3. Data Segment (DS). 데이터를 가리킨다.
4. Extra Segment (ES). 추가적인 데이터를 가리킨다 ('Extra'의 첫 글자 'E').
5. F Segment (FS). 많은 추가적인 데이터를 가리킨다 ('E' 다음은 'F').
6. G Segment (GS). 더 많은 추가적인 데이터를 가리킨다 ('F' 다음은 'G').

플래그 레지스터(Flag Register, RFLAGS)  - 64 bit
- 프로세서의 작동 결과와 상태를 저장하기 위한 부울 값들의 모음
- CF(Carry Flag) 부호 없는 수의 연산 결과가 비트의 범위를 넘는 경우
- ZF(Zero Flag) 연산의 결과가 0일 경우
- SF(Sign Flag) 연산의 결과가 음수일 경우.
- OF(Overflow Flag) 부호 있는 수의 연산 결과가 비트 범위를 넘을 경우
![flag-register](images/Pasted%20image%2020231015124234.png)


명령어 포인터 레지스터(Instruction Pointer Register, RIP) - 64 bit
- 다음에 실행되어야 할 명령어의 주소

# Linux Memory Layout

리눅스 메모리 구조

## 세그먼트

용도 별로 나눈 메모리 단위
- 각 용도에 맞게 적절한 권한(읽기, 쓰기, 실행)을 부여할 수 있음
- CPU는 메모리에 대해 권한이 부여된 행위만 할 수 있음

종류

1. 코드 세그먼트(.text)
	- 실행 가능한 기계 코드가 위치하는 영역. 함수 등
	- 주로 읽기, 실행 권한만 부여됨
2. 데이터 세그먼트
	- 컴파일 시점에 값이 정해진 전역 변수, 전역 상수 위치하는 영역
	- 읽기 권한이 부여됨.
	- data:  쓰기 가능한 세그먼트(전역 변수)
	- rodata:  쓰기 불가능한 세그먼트 (상수)
3. BSS 세그먼트(.bss)
	- Block Started By Symbol Segment
	- 컴파일 시점에 값이 정해지지 않은 전역 변수가 위치하는 영역
	- 읽기, 쓰기 권한 부여됨.
4. 스택 세그먼트
	- 프로세스의 스택이 위치하는 영역. 함수의 인자나 지역 변수 같은 임시 변수 등이 저장됨.
	- 읽기, 쓰기 권한 부여됨
5. 힙 세그먼트
	- 힙 데이터가 위치하는 세그먼트. malloc, calloc 등 동적 할당시 사용되는 메모리
	- 읽기, 쓰기 권한 부여됨.


# x86 Assembly

Operation Code (Opcode)

|명령 코드 분류|명령어 종류 |
|---|---|
|데이터 이동(Data Transfer)|`mov`, `lea`|
|산술 연산(Arithmetic)|`inc`, `dec`, `add`, `sub`|
|논리 연산(Logical)|`and`, `or`, `xor`, `not`|
|비교(Comparison)|`cmp`, `test`|
|분기(Branch)|`jmp`, `je`, `jg`|
|스택(Stack)|`push`, `pop`|
|프로시져(Procedure)|`call`, `ret`, `leave`|
|시스템 콜(System call)|`syscall`|
- 이외에도 다른 명령 코드가 있음

Operand 

- 상수(Immediate Value)
- 레지스터(Register)
- 메모리(Memory)



Question 1
 end로 점프하면 프로그램이 종료된다고 가정하자. 프로그램이 종료됐을 때, 0x400000 부터 0x400019까지의 데이터를 대응되는 아스키 문자로 변환하면 어느 문자열이 나오는가?

```
[Register]
rcx = 0
rdx = 0
rsi = 0x400000
=======================
[Memory]
0x400000 | 0x67 0x55 0x5c 0x53 0x5f 0x5d 0x55 0x10
0x400008 | 0x44 0x5f 0x10 0x51 0x43 0x43 0x55 0x5d
0x400010 | 0x52 0x5c 0x49 0x10 0x47 0x5f 0x42 0x5c
0x400018 | 0x54 0x11 0x00 0x00 0x00 0x00 0x00 0x00
=======================
[code]
1: mov dl, BYTE PTR[rsi+rcx]
2: xor dl, 0x30
3: mov BYTE PTR[rsi+rcx], dl
4: inc rcx
5: cmp rcx, 0x19
6: jg end
7: jmp 1

```
- code를 보면 한 바이트씩 읽어서 0x30 값과 xor  시키는데 총 19번 반복 시키는 걸 알 수 있다.
- 이를 파이썬으로 작성하면 다음과 같다.

```python
def main():
	arr = [
		0x67, 0x55, 0x5c, 0x53, 0x5f, 0x5d, 0x55, 0x10,
		0x44, 0x5f, 0x10, 0x51, 0x43, 0x43, 0x55, 0x5d,
		0x52, 0x5c, 0x49, 0x10, 0x47, 0x5f, 0x42, 0x5c,
		0x54, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
	

    for i in range(19):
        arr[i] ^= 0x30
        print(chr(arr[i]), end='')
    print()
  
 
if __name__ == "__main__":
	main()
```
- Welcome to assembly