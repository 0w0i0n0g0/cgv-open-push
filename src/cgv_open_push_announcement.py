from cgv_open_push_function import *

# 공지사항 내용
text = ""

# # 종료된 구독
# previous_topics = [
#     "DUNE-PART2-YONGSAN-IMAX",
#     "GODZILLA-KONG",
#     ]
# for topic in previous_topics:
#     send_open_push_announcement(text, topic)

# 현재 구독
# current_topics = [
#     "YONGSAN-IMAX",
#     "YONGSAN-4DX",
#     "HAIKU-YONGSAN-IMAX",
#     "APES-YONGSAN-IMAX",
#     "FURIOSA-YONGSAN-IMAX",
#     ]
# for topic in current_topics:
#     send_open_push_announcement(text, topic)

# 특정 구독
specific_topics = [
    ]
for topic in specific_topics:
    send_open_push_announcement(text, topic)