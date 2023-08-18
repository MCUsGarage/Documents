[toc]

## 기초
브라우저 기본 동작
1. URL 분석
	- Scheme: 통신 프로토콜
	- Authority: Userinfo, Host, Port
	- Path
	- Query
	- Fragment
1. DNS(Domain Name Server) 요청
	- IP 수신
2. HTTP 요청
3. HTTP 응답 수신
4. 리소스 다운로드 및 웹 렌더링
	- 웹 렌더링은 브라우저별로 다른 엔진 사용(webkit, blink, gecko, etc..)


## Cookie & Session

HTTP 프로토콜 특징
- **Connectionless**: 하나의 요청에 하나의 응답을 한 후 연결을 종료함. 
- **Stateless**: 통신이 끝난 후 상태 정보를 저장하지 않음
-> 웹서버는 클라이언트를 기억할수 없음
### 쿠키 (Cookie)  

상태를 유지하기 위해 사용
- 서버에 요청을 보낼때마다 쿠키를 같이 전송함
- 쿠키를 확인해서 클라이언트 구분

쿠키 변조
- 쿠키를 통해 인증 정보를 식별하는 경우 쿠키를 변조해서 다른 사람인 것 처럼 사용해도 인증 통과 가능

### 세션 (Session)  

클라이언트가 인증 정보를 변조할 수 없게 하기위해 사용
- 인증 정보를 서버에 저장하고 해당 데이터에 접근할 수 있는 키(Session ID)를 만들어 클라이언트에 전달함. 브라우저는 해당 키를 쿠키에 저장하고 이후에 HTTP 요청을 보낼 때 사용함. 서버는 요청에 포함된 키에 해당하는 데이터를 가져와 인증 상태를 확인함.

-> 서버에 저장하는 값

### 세션 하이재킹 (Session Hijacking)

타 이용자의 쿠키를 훔쳐 인증 정보를 획득하는 공격
- 쿠키에 세션 정보(session id)가 저장되어 있고 서버는 이를 통해 이용자 식별하고 인증을 처리함.
- 다른 사람이 쿠키 변조를 통해 session id를 보내서 인증을 통과시키면 특정 사람인 것처럼 활동 가능

### Dreamhack - cookie
쿠키로 인증 상태를 관리하는 간단한 로그인 서비스입니다.  
admin 계정으로 로그인에 성공하면 플래그를 획득할 수 있습니다.

문제파일 - flask server

```python
#!/usr/bin/python3
from flask import Flask, request, render_template, make_response, redirect, url_for

app = Flask(__name__)

try:
    FLAG = open('./flag.txt', 'r').read()
except:
    FLAG = '[**FLAG**]'

users = {
    'guest': 'guest',
    'admin': FLAG
}

@app.route('/')
def index():
    username = request.cookies.get('username', None)
    if username:
        return render_template('index.html', text=f'Hello {username}, {"flag is " + FLAG if username == "admin" else "you are not admin"}')
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            pw = users[username]
        except:
            return '<script>alert("not found user");history.go(-1);</script>'
        if pw == password:
            resp = make_response(redirect(url_for('index')) )
            resp.set_cookie('username', username)
            return resp 
        return '<script>alert("wrong password");history.go(-1);</script>'

app.run(host='0.0.0.0', port=8000)

```

- 함수 index 에서 쿠키의 username을 가져와서 있으면 text를 렌더링함
	- admin으로 로그인하면 flag 를 출력함
- 함수 login 에서 username, password로 로그인 처리함
	- pw를 users 배열에서 확인하고 입력한 비밀번호랑 맞으면 쿠키를 설정함

 ![login_page][./images/20230818171908.png]
![guest_login](20230818172344.png)
![set_cookie_admin](Pasted%20image%2020230818172513.png)
- users에 guest/guest 가 있으니 이 계정으로 로그인해서 쿠키를 설정하고 값을 admin 으로 바꾸면 됨
- 쿠키에 username: admin으로 직접 설정해도 됨 

## XSS - Cross site scripting

## Cross Site Request Forgery

## SQL Injection

## Command Injection

## File Vulnerability

## SSRF - Server Side Request Forgery 

