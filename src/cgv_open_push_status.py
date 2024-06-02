import re
import requests
from flask import Flask, request
from datetime import datetime
from cgv_open_push_global_variable import private_ntfy_prometheus_address

def get_time_difference_from_log_file(log_file):
   try:
      with open(log_file, "r", encoding='utf-8') as f:
         lines = f.readlines()
         last_line = lines[-1]
      last_time_str = last_line.split(",")[0]
      last_time = datetime.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
      current_time = datetime.now()
      time_diff = (current_time - last_time).total_seconds()
   except Exception as e:
      return e
   return time_diff

def last_n_lines_from_log_file(log_file, n=50):
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

def check_user_is_mobile_or_not():
   user_agent = request.headers.get('User-Agent')
   if 'Android' in user_agent or 'iPhone' in user_agent or 'iPad' in user_agent:
      return True # 모바일
   else:
      return False # 컴퓨터

def get_metrics():
   result = []
   response = requests.get(private_ntfy_prometheus_address)
   if response.status_code == 200:
      match = re.search(r"ntfy_visitors_total\s+(\d+)", response.text)
      if match:
         result.append(int(match.group(1)))
      match = re.search(r"ntfy_subscribers_total\s+(\d+)", response.text)
      if match:
         result.append(int(match.group(1)))
   else:
      raise RuntimeError(f"RuntimeError : {response.status_code}")
   return result

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

   log = last_n_lines_from_log_file("cgv-open-push.log", 50)
   metrics = get_metrics()
   visitors_total = metrics[0]
   subscribers_total = metrics[1]

   pre_tag_font_size = ""
   padding_and_margin = ""
   num_item_font_size = ""
   if check_user_is_mobile_or_not():
      num_item_font_size = "4"
      pre_tag_font_size = "1"
      padding_and_margin = "2"
   else:
      num_item_font_size = "5"
      pre_tag_font_size = "1.5"
      padding_and_margin = "1"

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
      font-size: {pre_tag_font_size}em;
      white-space: pre-wrap; 
      background-color: #f5f5f5; 
      color: #444444;
      margin: 0 {padding_and_margin}vw; 
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
      font: 1.7em/1 'arial';
      color: gray;
      font-weight: 600;
      margin-top: 10px;
      margin-bottom: 0;
   }}
   .nums {{
      font: bold {num_item_font_size}em/1 'arial';
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
      max-height: 100vh;
      overflow-y: auto;
   }}
   #metrics {{
      background-color: #f5f5f5; 
      margin: {padding_and_margin}vw; 
      align-items: center;
      justify-content: center;
   }}
   """

   return f"""
   <!DOCTYPE html>
   <html lang="ko">
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
   </html>
   """

if __name__ == '__main__':  
   app.run('0.0.0.0',port=5000,debug=True)