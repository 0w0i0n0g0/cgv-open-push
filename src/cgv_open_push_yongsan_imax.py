import os
import sys
import time
from cgv_open_push_function import *
from diff_match_patch import diff_match_patch

# 용산아이파크몰 IMAX관 업데이트 내역 확인 로직
def yongsan_imax_main():
    
    url = 'http://ticket.cgv.co.kr/CGV2011/RIA/CJ000.aspx/CJ_TICKET_SCHEDULE_TOTAL_PLAY_YMD'

    cookies = {
        '_INSIGHT_CK_1': 'f1d83d00493551cd7875517dd21cf81d|5e76eb13a569e162f1a8517dd21cf81d:1705916707000',
        'WMONID': 'zvGaitKgTbw',
        '_gid': 'GA1.3.1750462509.1711519151',
        'ASP.NET_SessionId': 'o0453f5oqurfws4f1abdzxij',
        '_gat_UA-47951671-5': '1',
        '_gat_UA-47951671-7': '1',
        '_gat_UA-47126437-1': '1',
        '_gat': '1',
        '_ga_559DE9WSKZ': 'GS1.1.1711547612.29.1.1711547816.58.0.0',
        '_ga': 'GA1.1.1033028224.1705195852',
        '_ga_SSGE1ZCJKG': 'GS1.3.1711547612.30.1.1711547816.59.0.0',
    }

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'http://ticket.cgv.co.kr',
        'Pragma': 'no-cache',
        'Referer': 'http://ticket.cgv.co.kr/Reservation/Reservation.aspx?MOVIE_CD=&MOVIE_CD_GROUP=&PLAY_YMD=&THEATER_CD=&PLAY_NUM=&PLAY_START_TM=&AREA_CD=&SCREEN_CD=&THIRD_ITEM=&SCREEN_RATING_CD=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
        'TheaterCd': 'LMP+XuzWskJLFG41YQ7HGA==',
        'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
        'MovieGroupCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'ScreenRatingCd': 'kXwoR3tnLM/+Tu0BILP3Qg==',
        'MovieTypeCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    }

    target_name = "YONGSAN-IMAX"
    
    try:
        # 첫 응답 저장
        response1 = get_request_to_cgv_api(url, cookies, headers, json_data, target_name)
        response2 = ""
        while True:
            # 5분마다 새로고침
            time.sleep(300)
            # 2번에 새 응답 저장
            response2 = get_request_to_cgv_api(url, cookies, headers, json_data, target_name)
            print(response2)
            # 새 응답과 저장된 이전 응답이 다르다면
            if response1 != response2:
                # 불필요한 부분 삭제
                response1 = yongsan_imax_remove_useless_tags(response1)
                response2 = yongsan_imax_remove_useless_tags(response2)
                # diff에 응답끼리 다른 부분을 추출 {(-1, "삭제된 부분"), (1, "추가된 부분")}
                dmp = diff_match_patch()
                diff = dmp.diff_main(response1, response2)
                dmp.diff_cleanupSemantic(diff)
                added_result = ""
                deleted_result =""
                for d in diff:
                    ## d[0]가 1이면 추가된 요소
                    if d[0] == 1:
                        try:
                            added_result += extract_all_text_from_xml(d[1])
                        except:
                            added_result += d[1]
                    ## d[0]가 -1이면 삭제된 요소
                    if d[0] == -1:
                        try:
                            deleted_result += extract_all_text_from_xml(d[1])
                        except:
                            deleted_result += d[1]
                #추가된 요소가 있으면
                if added_result != "":
                    logging.info(f'{target_name} added item : {deleted_result}')
                    # 추가된 변경사항 푸시알림 보내기
                    try:
                        send_open_push(str(added_result), target_name)
                    except Exception as e:
                        send_push_to_ntfy(f"{target_name}\n서버에서 푸시 알림 전송 중 오류 발생🚨\n{e}", target_name)
                        send_push_to_private_ntfy(f"{target_name}\n서버에서 푸시 알림 전송 중 오류 발생🚨\n{e}", target_name)
                        logging.error(f'{target_name} error when sending open push : {e}')
                        # 5초 대기 후 다시 알림 보내기 시도
                        time.sleep(5)
                        send_open_push(str(added_result), target_name)
                #삭제된 요소가 있으면
                if deleted_result != "":
                    #로그만 남기기
                    logging.info(f'{target_name} deleted item : {deleted_result}')
                # response1 값은 변경된 값으로 초기화
                response1 = response2
    # 오류 발생 시
    except Exception as e:
        send_push_to_ntfy(f"{target_name}\n서버에서 오류 발생🚨\n{e}", target_name)
        send_push_to_private_ntfy(f"{target_name}\n서버에서 오류 발생🚨\n{e}", target_name)
        logging.error(f'{target_name} error : {e}')
        # 다시 실행
        os.execl(sys.executable, sys.executable, *sys.argv)