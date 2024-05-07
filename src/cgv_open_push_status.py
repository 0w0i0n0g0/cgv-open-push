import re
from flask import Flask, request
from datetime import datetime

def get_time_difference_from_log_file(log_file):
   try:
      with open(log_file, "r", encoding='utf-8') as f:
         lines = f.readlines()
         last_line = lines[-1]
      last_time_str = last_line.split(",")[0]
      print(last_time_str)
      last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
      current_time = datetime.now()
      time_diff = (current_time - last_time).total_seconds()
   except Exception as e:
      return e
   return time_diff

def last_n_lines_from_log_file(log_file, n=5):
    log = ''
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            last_n_lines = lines[-n:]
            for line in last_n_lines:
            # INFO 문자열 앞에 \n 추가
                if 'INFO' in line:
                    line = line.replace(':INFO:', '\n')
                log = line.strip() + '\n\n' + log
    except Exception as e:
        return e
    finally:
        return log

def extract_platform(user_agent_string):
   # 첫 번째 괄호 안의 내용을 추출하는 정규 표현식
   pattern = r"\((.*?)\;"
   # 정규 표현식을 사용하여 문자열 일치 부분을 추출합니다.
   match = re.search(pattern, user_agent_string)
   # 일치하는 부분이 없으면 빈 문자열을 반환합니다.
   if match is None:
      return ""
   # 추출된 문자열을 반환합니다.
   return match.group(1)

def check_user_platform():
   platform = extract_platform(request.user_agent.string)
   return platform

import requests

def get_subscribers_total():
  response = requests.get("http://192.168.0.17:9090")
  if response.status_code == 200:
    match = re.search(r"ntfy_subscribers_total\s+(\d+)", response.text)
    if match:
      return int(match.group(1))
  else:
    raise RuntimeError(f"RuntimeError : {response.status_code}")
  
def get_visitors_total():
  response = requests.get("http://192.168.0.17:9090")
  if response.status_code == 200:
    match = re.search(r"ntfy_visitors_total\s+(\d+)", response.text)
    if match:
      return int(match.group(1))
  else:
    raise RuntimeError(f"RuntimeError : {response.status_code}")

app = Flask(__name__)

@app.route('/')
def home():
   time_diff = get_time_difference_from_log_file("cgv-open-push.log")
   health_color = ""
   if isinstance(time_diff, float):
      if time_diff >= 300:
         health_color = "#e06666"
      else:
         health_color ="#1D976C"
   else:
      health_color = "#ff0000"
   log = last_n_lines_from_log_file("cgv-open-push.log", 10)
   user_platform = check_user_platform()

   subscribers_total = get_subscribers_total()
   visitors_total = get_visitors_total()

   font_size = ""
   padding_and_margin = ""
   if "Windows" in user_platform:
      font_size = "font-size: 1.5em;"
      padding_and_margin = 1
   else:
      font_size = "font-size: 1em;"
      padding_and_margin = 2

   css = f"""
   html, body {{ 
      width: 100%;
      height: 100%;
      overflow: hidden;
      margin:0 auto;
      touch-action: none;    
   }}
   progress {{ 
      appearance: none;
      width: 97%;
      height: 2vh;
   }} 
   progress::-webkit-progress-bar {{ 
      background: #ffffff; 
      border-radius: 1vh; 
      overflow: hidden;
   }} 
   progress::-webkit-progress-value {{ 
      border-radius: 1vh; 
      background: {health_color}; 
      background: -webkit-linear-gradient(to right, #ffffff, {health_color}); 
      background: linear-gradient(to right, #ffffff, {health_color}); 
   }}
   h1 {{
      color: #333; 
      margin: {padding_and_margin}vw;
      font-family: arial;
   }}
   h2 {{
      color: #333; 
      margin: {padding_and_margin}vw;
      font-family: arial;
   }}
   pre {{
      {font_size} 
      white-space: pre-wrap; 
      background-color: #f5f5f5; 
      color: #444444;
      margin: {padding_and_margin}vw; 
      padding: {padding_and_margin}vw; 
      font-family: "Nanum Gothic Coding", monospace;
   }}
   .num-container {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-evenly;
      align-items: center;
      }}
   .num-item {{
      text-align: center;
      padding-right: 10%;
      padding-left: 10%;
      padding-top: 10px;
      padding-bottom: 10px;
   }}
   .in-title {{
      font: 30px/1 'arial';
      color: gray;
      font-weight: 600;
      margin-top: 10px;
      margin-bottom: 0;
   }}
   .nums {{
      font: bold 80px/1 'arial';
      color: #444444;
   }}
      #health-check {{
      text-align: center;
      background-color: #f5f5f5; 
      margin: {padding_and_margin}vw; 
      padding: {padding_and_margin}vw; 
   }}
   #log {{
      margin:0 auto; 
   }}
   #metrics {{
      background-color: #f5f5f5; 
      margin: {padding_and_margin}vw; 
      align-items: center;
      justify-content: center;
   }}
   """

   return f"""
   <head>
      <title>CGV 예매 오픈 알리미</title>
      <link rel="shortcut icon" href="https://raw.githubusercontent.com/0w0i0n0g0/cgv-open-push/main/img/logo.png">
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic+Coding&family=Orbit&display=swap" rel="stylesheet">
      <style>{css}</style>
      <meta http-equiv='refresh' content='10'/>
      <meta name="viewport" content="initial-scale=1.0; maximum-scale=1.0; minimum-scale=1.0; user-scalable=no;"> 
   </head>
   <body>
      <h1>CGV 예매 오픈 알리미</h1>
      <h2>Metrics</h2>
      <div id="metrics">
         <div class="num-container" id="num-container">
            <div class="num-item">
               <h4 class="in-title">Daily Active Users</h4>
               <span class="nums" data-count="{visitors_total}">0</span><span id="num-unit"></span><br>
            </div>
            <div class="num-item">
               <h4 class="in-title">Online Subscribers</h4>
               <span class="nums" data-count="{subscribers_total}">0</span><span id="num-unit"></span><br>
            </div>
         </div>
      </div>
      <h2>Server Health Check</h2>
      <div id="health-check">
         <progress value='200' max='{time_diff}'></progress>
      </div>
      <h2>Server Log</h2>
      <div id="log">
         <pre>{log}</pre>
      </div>
         <script src="https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.6.0.min.js"></script>
      <script>
         //숫자 카운트 애니메이션
         $('.nums').each(function () {{
               const $this = $(this),
                  countTo = $this.attr('data-count');

               $({{
                  countNum: $this.text()
               }}).animate({{
                  countNum: countTo
               }}, {{
                  duration: 2000,
                  easing: 'swing',
                  step: function () {{
                     $this.text(Math.floor(this.countNum));
                  }},
                  complete: function () {{
                     $this.text(this.countNum.toString().replace(/\B(?=(\d{{3}})+(?!\d))/g, ','));
                  }}
               }});
         }});
      </script>
   </body>
   """

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)