from logging.handlers import RotatingFileHandler
import time
import atexit
import threading
from cgv_open_push_function import *
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

json_data = [
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
        "Language": "zqWM417GS6dxQ7CIf65+iA=="
    },
    {
    "REQSITE": "x02PG4EcdFrHKluSEQQh4A==",
    "TheaterCd": "LMP+XuzWskJLFG41YQ7HGA==",
    "ISNormal": "3y+GIXzg3xKpOjlKjH8+Fg==",
    "MovieGroupCd": "nG6tVgEQPGU2GvOIdnwTjg==",
    "ScreenRatingCd": "nG6tVgEQPGU2GvOIdnwTjg==",
    "MovieTypeCd": "nG6tVgEQPGU2GvOIdnwTjg==",
    "Subtitle_CD": "nG6tVgEQPGU2GvOIdnwTjg==",
    "SOUNDX_YN": "nG6tVgEQPGU2GvOIdnwTjg==",
    "Third_Attr_CD": "nG6tVgEQPGU2GvOIdnwTjg==",
    "Language": "zqWM417GS6dxQ7CIf65+iA=="
    }
]

target = [
    "듄-파트2 용아맥 오픈 알림 서버가",
    "용산아이파크몰 오픈 알림 서버가"
]

def main(cookies, headers, json_data, target):
    atexit.register(send_ntfy_push_server, f"{target} 종료되었습니다.")
    try:
        # 첫 응답 저장
        send_ntfy_push_server(f"{target} 시작되었습니다.")
        response1 = extract_playdays(send_curl_to_cgv_multiple(url, cookies, headers, json_data, target))
        response2 = ""
        counter = 0
        while True:
            time.sleep(2)
            # 2번에 새 응답 저장
            response2 = extract_playdays(send_curl_to_cgv_multiple(url, cookies, headers, json_data, target))
            # 비교
            if response1 != response2:
                dmp = diff_match_patch()
                diff = dmp.diff_main(response1, response2)
                dmp.diff_cleanupSemantic(diff)
                added_result = ""
                deleted_result =""
                for d in diff:
                    if d[0] == 1:
                        try:
                            added_result += extract_format_date(d[1])
                        except:
                            added_result += d[1]
                        finally:
                            logging.debug(f'추가된 요소 : {d}')
                    if d[0] == -1:
                        try:
                            deleted_result += extract_format_date(d[1])
                        except:
                            deleted_result += d[1]
                        finally:
                            logging.debug(f'삭제된 요소 : {d}')
                if added_result != "":
                    send_ntfy_push('추가된 요소 : ' + str(added_result))
                if deleted_result != "":
                    send_ntfy_push('삭제된 요소 : ' + str(deleted_result))
                # response1 값은 변경된 값으로 초기화
                response1 = response2
            # 카운터 증가
            counter += 1
            if counter >= 1800:
                send_ntfy_push_server(f"{target} 실행중입니다.")
                counter = 0
    except Exception as e:
        send_ntfy_push_server(f"{target} 예외발생으로 종료되었습니다.")
        logging.debug(f'예외발생 : {e}')

handlers = [RotatingFileHandler('cgv-open-push.log', maxBytes=10*1024*1024, backupCount=3, encoding='utf-8')]
logging.basicConfig(handlers=handlers, level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

for data in enumerate(json_data):
    t = threading.Thread(target=main, args=(cookies, headers, data[1], target[data[0]]))
    t.start()