# 전체 topic에 공지사항 발송

from cgv_open_push_function import *
from cgv_open_push_global_variable import *

# 공지사항 내용
text = ""

send_open_push_announcement(text, "YONGSAN-IMAX")

for topic in enumerate(target_name):
    send_open_push_announcement(text, topic)