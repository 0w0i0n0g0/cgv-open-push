import os
import sys
import time
import atexit
import threading
from cgv_open_push_function import *
from cgv_open_push_global_variable import *
from logging.handlers import RotatingFileHandler
from diff_match_patch import diff_match_patch

# 메인 로직
def main(url, cookies, headers, json_data, target_name):
    # 종료 시 ntfy로 서버 종료 알림 보내기
    atexit.register(send_ntfy_push_server, f"{target_name}\n서버가 종료되었습니다.", target_name)
    try:
        # 첫 응답 저장
        response1 = extract_playdays(send_curl_to_cgv_multiple(url, cookies, headers, json_data, target_name))
        response2 = ""
        while True:
            # 5초마다 새로고침
            time.sleep(5)
            # 2번에 새 응답 저장
            response2 = extract_playdays(send_curl_to_cgv_multiple(url, cookies, headers, json_data, target_name))
            # 새 응답과 저장된 이전 응답이 다르다면
            if response1 != response2:
                dmp = diff_match_patch()
                # diff에 응답끼리 다른 부분을 추출 {(-1, "삭제된 부분"), (1, "추가된 부분")}
                diff = dmp.diff_main(response1, response2)
                dmp.diff_cleanupSemantic(diff)
                added_result = ""
                deleted_result =""
                for d in diff:
                    ## d[0]가 1이면 추가된 요소
                    if d[0] == 1:
                        try:
                            added_result += extract_format_date(d[1])
                        except:
                            added_result += d[1]
                    ## d[0]가 -1이면 삭제된 요소
                    if d[0] == -1:
                        try:
                            deleted_result += extract_format_date(d[1])
                        except:
                            deleted_result += d[1]
                #추가된 요소가 있으면
                if added_result != "":
                    logging.info(f'{target_name} 서버에서 추가된 요소 : {added_result}')
                    # 추가된 변경사항 푸시알림 보내기
                    try:
                        send_ntfy_push(str(added_result), target_name)
                    except Exception as e:
                        send_ntfy_push_server(f"{target_name}\n서버에서 푸시 알림 전송 중 오류 발생🚨\n{e}", target_name)
                        send_ntfy_push_health_check(f"서버에서 푸시 알림 전송 중 오류 발생🚨\n{e}", target_name)
                        logging.error(f'{target_name} 서버에서 푸시 알림 전송 중 오류 발생 : {e}')
                        # 5초 대기 후 다시 알림 보내기 시도
                        time.sleep(5)
                        send_ntfy_push(str(added_result), target_name)
                #삭제된 요소가 있으면
                if deleted_result != "":
                    #로그만 남기기
                    logging.info(f'{target_name} 서버에서 삭제된 요소 : {deleted_result}')
                # response1 값은 변경된 값으로 초기화
                response1 = response2
    # 오류 발생 시
    except Exception as e:
        send_ntfy_push_server(f"{target_name}\n서버에서 오류 발생🚨\n{e}", target_name)
        send_ntfy_push_health_check(f"서버에서 오류 발생🚨\n{e}", target_name)
        logging.error(f'{target_name} 서버에서 오류 발생 : {e}')
        # 다시 실행
        os.execl(sys.executable, sys.executable, *sys.argv)

# 로그 저장 (최대 5MB씩 3개 백업본 저장)
handlers = [RotatingFileHandler('cgv-open-push.log', maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')]
logging.basicConfig(handlers=handlers, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# 코드 시작 시 개인 서버에 알림 보내기
send_ntfy_push_health_check("서버가 시작되었습니다.", "raspberrypi")

# 입력된 json_data에 대해 쓰레드로 모두 실행
for data in enumerate(json_data):
    t = threading.Thread(target=main, args=(url, cookies, headers, data[1], target_name[data[0]]))
    t.start()
    time.sleep(2)