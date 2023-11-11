# Search The Flag

Session hijacking? SSRF?

1. 일반 유저로 로그인
2. report 페이지에서 http 리퀘스트 송신
```python
@app.route("/report", methods=["GET", "POST"])
def report():
	if not session:
		return redirect("/login")
	  
	if request.method == "POST":
		path = request.form.get("path")
		if not path:
			return render_template("report.html", msg="fail")
		  
		if path and path[0] == "/":
			path = path[1:]
		  
		url = f"http://127.0.0.1:8000/{path}"
		if check_url(url):
			return render_template("report.html", msg="success")
		else:
			return render_template("report.html", msg="fail")
	  
	elif request.method == "GET":
		return render_template("report.html")
```
3. 리퀘스트 받으면 서버 내부에서 check_url실행. admin 계정으로 로그인후 url 실행
```python
def check_url(url):
	try:
	service = Service(executable_path="/chromedriver")
	options = webdriver.ChromeOptions()
	for _ in [
		"headless",
		"window-size=1920x1080",
		"disable-gpu",
		"no-sandbox",
		"disable-dev-shm-usage",
	]:
		options.add_argument(_)
	driver = webdriver.Chrome(service=service, options=options)
	driver.implicitly_wait(3)
	driver.set_page_load_timeout(3)
	  
	driver_promise = Promise(driver.get("http://127.0.0.1:8000/login"))
	driver_promise.then(driver.find_element(By.NAME, "username").send_keys("admin"))
	driver_promise.then(
	driver.find_element(By.NAME, "password").send_keys("REDACTED!!!")
	)
	driver_promise = Promise(driver.find_element(By.ID, "submit").click())
	driver_promise.then(driver.get(url))
	driver_promise.then(sleep(0.5))
	  
	except Exception as e:
		driver.quit()
		return False
	finally:
		driver.quit()
	return True
```
4. url을 `/search?keyword=`에 한글자씩 넣어서 비밀키 확인

이 방식으로 진행해야할 것 같은데 4번에서 비밀키를 확인할 방법이 없다. report에서 url 뭐가 들어가든 success 가 뜬다.
- 잘못된 URL (404 page)가 뜨면 fail 뜰줄 알았는데 안된다.

직접 페이지에 들어가서 /search?keyword= 를 사용하면 init.sql 에 있는 값에서 검색한다.
```sql
INSERT INTO sentences (sentence, secret) VALUES
('The harder the battle, the sweeter the victory.', 0),
('In football, the worst blindness is only seeing the ball.', 0),
("Success is no accident. It is hard work, perseverance, learning, studying, sacrifice, and most of all, love of what you are doing.", 0),
("If you're not making mistakes, then you're not doing anything. I'm positive that a doer makes mistakes.", 0),
("I don't have time for fear. I'm too busy working on my dreams.", 0),
('The only way to do great work is to love what you do.', 0),
('The best way to predict the future is to create it.', 0),
("Your time is limited, don't waste it living someone else's life.", 0),
("The only limit to our realization of tomorrow will be our doubts of today.", 0),
("DH{**fake_flag**}", 1);
```
- admin 세션을 활용해야한다. admin 비밀번호 필요하거나 서버측에서 직접 수행하게 해야함.

search 에선 admin 세션이 필요하다.
```python
@app.route("/search", methods=["GET"])
def search():
	if not session:
		return redirect("/login")
	  
	if request.method == "GET":
		keyword = request.args.get("keyword")
		  
		if keyword == None:
			return render_template("search.html")
		  
		if keyword == "":
			return render_template("search.html", msg="Enter the the keyword")
		  
		if "}" in keyword:
			return render_template("search.html", msg="Not allowed string")
		  
		sentence_list = []
		sentences = search_sentences(keyword)
		  
		if sentences == None:
			abort(404, {"keyword": keyword})
		  
		for sentence in sentences:
			if (session["isAdmin"] == False) and (sentence[2] == 1):
				continue
			else:
				sentence_list.append(sentence[1])
		  
		if len(sentence_list) == 0:
			abort(404, {"keyword": keyword})
		  
		return render_template("search.html", sentence_list=sentence_list)
	  
	else:
		abort(500)
```
- `session["isAdmin"]` 이 조건이 있어서 돌아가든 세션을 얻든 해야한다.