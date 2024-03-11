import time
import atexit
import threading
from cgv_open_push_function import *
from logging.handlers import RotatingFileHandler
from diff_match_patch import diff_match_patch

url = 'http://ticket.cgv.co.kr/CGV2011/RIA/CJ000.aspx/CJ_TICKET_SCHEDULE_TOTAL_PLAY_YMD'

cookies = {
    '_INSIGHT_CK_1': 'f1d83d00493551cd7875517dd21cf81d|5e76eb13a569e162f1a8517dd21cf81d:1705916707000',
    'WMONID': 'zvGaitKgTbw',
    '_gid': 'GA1.3.895218779.1709345361',
    'CgvPopAd-ticket': '^%^uA257^%^uA24D^%^uA248^%^uA251^%^uA24C^%^uA25C',
    '_gat_UA-47951671-5': '1',
    '_gat_UA-47951671-7': '1',
    '_gat_UA-47126437-1': '1',
    '_gat': '1',
    'ASP.NET_SessionId': '3qi04s2s5lgd33kmszdarrvp',
    '_ga_559DE9WSKZ': 'GS1.1.1709348096.22.1.1709348100.56.0.0',
    '_ga': 'GA1.1.1033028224.1705195852',
    '_ga_SSGE1ZCJKG': 'GS1.3.1709348096.23.1.1709348100.56.0.0',
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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

# 변경사항을 확인할 타겟의 json_data
json_data = [
    # 듄-파트2 용산아이파크몰 IMAX관
    {
        "REQSITE": "x02PG4EcdFrHKluSEQQh4A==",
        "TheaterCd": "LMP+XuzWskJLFG41YQ7HGA==",
        "ISNormal": "3y+GIXzg3xKpOjlKjH8+Fg==",
        "MovieGroupCd": "bNQovwyoamC5EsbGvSDIqw==",
        "ScreenRatingCd": "nG6tVgEQPGU2GvOIdnwTjg==",
        "MovieTypeCd": "/Saxvehmz4RPKZDKNMvSKQ==",
        "Subtitle_CD": "nG6tVgEQPGU2GvOIdnwTjg==",
        "SOUNDX_YN": "nG6tVgEQPGU2GvOIdnwTjg==",
        "Third_Attr_CD": "nG6tVgEQPGU2GvOIdnwTjg==",
        "Language": "zqWM417GS6dxQ7CIf65+iA==",
    },
]

# 변경사항을 확인할 타겟 이름 json_data 순서대로
target_name = [
    "DUNE-PART2-YONGSAN-IMAX",
]

# 메인 함수
def main(url, cookies, headers, json_data, target_name):
    atexit.register(send_ntfy_push_server, f"{target_name}\n서버가 종료되었습니다.", target_name)
    try:
        # 첫 응답 저장
        send_ntfy_push_server(f"{target_name}\n서버가 시작되었습니다.", target_name)
        response1 = extract_playdays(send_curl_to_cgv_multiple(url, cookies, headers, json_data, target_name))
        response2 = ""
        counter = 0
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
                    logging.debug(f'추가된 요소 : {added_result}')
                    # 추가된 변경사항 푸시알림 보내기
                    send_ntfy_push(str(added_result), target_name)
                #삭제된 요소가 있으면
                if deleted_result != "":
                    #로그만 남기기
                    logging.debug(f'삭제된 요소 : {deleted_result}')
                # response1 값은 변경된 값으로 초기화
                response1 = response2
            # 카운터 증가
            counter += 1
            # (약 1시간)
            if counter >= 720:
                # 서버 실행중 푸시알림 보내기
                send_ntfy_push_server(f"{target_name}\n서버가 실행중입니다.", target_name)
                # 카운터 초기화
                counter = 0
    except Exception as e:
        send_ntfy_push_server(f"{target_name}\n서버가 예외발생으로 종료되었습니다.", target_name)
        logging.debug(f'{target_name}서버에서 예외발생 : {e}')

# 로그 저장 (최대 10MB씩 3개 백업본 저장)
handlers = [RotatingFileHandler('cgv-open-push.log', maxBytes=10*1024*1024, backupCount=3, encoding='utf-8')]
logging.basicConfig(handlers=handlers, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

# 입력된 json_data에 대해 쓰레드로 모두 실행
for data in enumerate(json_data):
    t = threading.Thread(target=main, args=(url, cookies, headers, data[1], target_name[data[0]]))
    t.start()