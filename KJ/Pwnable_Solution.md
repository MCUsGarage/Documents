
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