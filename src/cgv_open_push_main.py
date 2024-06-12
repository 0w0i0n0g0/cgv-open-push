import time
import atexit
import threading
from cgv_open_push_function import *
from cgv_open_push_global_variable import *
from cgv_open_push_movie import movie_main
from cgv_open_push_screen import screen_main
from logging.handlers import RotatingFileHandler

# 로그 저장 (최대 5MB씩 3개 백업본 저장)
handlers = [RotatingFileHandler('cgv-open-push.log', maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')]
logging.basicConfig(handlers=handlers, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# cgv_open_push_status.py 실행
threading.Thread(target=run_cgv_open_push_status).start()
time.sleep(1)

# 영화 Thread 실행
for data in enumerate(movie_json_data):
    t = threading.Thread(target=movie_main, args=(movie_url, movie_cookies, movie_headers, data[1], movie_target_name[data[0]]))
    t.start()
    time.sleep(1)

# 특별관 Thread 실행
for data in enumerate(screen_json_data):
    t = threading.Thread(target=screen_main, args=(screen_url, screen_cookies, screen_headers, data[1], screen_target_name[data[0]]))
    t.start()
    time.sleep(1)

# 서버 시작 알림 보내기
send_push_to_ntfy("cgv-open-push\n서버가 시작되었습니다.", "cgv-open-push")
send_push_to_private_ntfy("cgv-open-push\n서버가 시작되었습니다.", "cgv-open-push")

# 종료 시 서버 종료 알림 보내기
atexit.register(send_push_to_ntfy, "cgv-open-push\n서버가 종료되었습니다.", "cgv-open-push")
atexit.register(send_push_to_private_ntfy, "cgv-open-push\n서버가 종료되었습니다.", "cgv-open-push")