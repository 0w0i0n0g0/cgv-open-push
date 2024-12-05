import os
import sys
import time
import queue
from cgv_open_push_function import *
from diff_match_patch import diff_match_patch

# 영화 업데이트 내역 확인 로직
def movie_main(url, cookies, headers, json_data, target_name, message_queue):
    try:
        # 첫 응답 저장
        response1 = extract_playdays(get_request_to_cgv_api(url, cookies, headers, json_data, target_name))
        response2 = ""
        while True:
            time.sleep(5)
            # 2번에 새 응답 저장
            response = get_request_to_cgv_api(url, cookies, headers, json_data, target_name)
            위치 = extract_text_between_tag(response, "THEATER_NM")
            유형 = extract_text_between_tag(response, "RATING_NM")
            영화 = extract_text_between_tag(response, "MOVIE_GROUP_NM")
            save_log_info(f"{target_name} response : 위치 : {위치}, 유형 : {유형}, 영화 : {영화}")
            response2 = extract_playdays(response)
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
                            added_result += extract_text_between_tag(d[1], "FORMAT_DATE")
                        except:
                            added_result += d[1] + ", "
                    ## d[0]가 -1이면 삭제된 요소
                    elif d[0] == -1:
                        try:
                            deleted_result += extract_text_between_tag(d[1], "FORMAT_DATE")
                        except:
                            deleted_result += d[1] + ", "
                #추가된 요소가 있으면
                if added_result != "":
                    save_log_info(f'{target_name} added item : {added_result.encode()}')
                    # 추가된 변경사항 푸시알림 보내기
                    try:
                        message_queue.put([target_name, "**예매 오픈 알림** : " + str(added_result)])
                    except Exception as e:
                        save_log_error(f'{target_name} error when sending open push : {e}')
                        # 5초 대기 후 다시 알림 보내기 시도
                        time.sleep(5)
                        message_queue.put([target_name, "**예매 오픈 알림** : " + str(added_result)])
                #삭제된 요소가 있으면
                if deleted_result != "":
                    #로그만 남기기
                    save_log_info(f'{target_name} deleted item : {deleted_result.encode()}')
                # response1 값은 변경된 값으로 초기화
                response1 = response2
            # 5분마다 새로고침
            time.sleep(295)
    # 오류 발생 시
    except Exception as e:
        save_log_error(f'{target_name} error : {e}')
        # 다시 실행
        os.execl(sys.executable, sys.executable, *sys.argv)