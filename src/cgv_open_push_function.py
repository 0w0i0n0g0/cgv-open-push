import json
import re
import subprocess
import time
import requests
import logging
import datetime
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

def run_cgv_open_push_status():
    while True:
        save_log_info("cgv_open_push_status.py restarted.")
        process = subprocess.Popen(['python', 'cgv_open_push_status.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(3600)
        process.kill()

# 로그 저장
def save_log_info(log, is_log_file=False):
    if is_log_file:
        logging.info(log)
    print(f"[{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}] {log}", flush=True)

def save_log_error(log, is_log_file=True):
    if is_log_file:
        logging.error(log)
    print(f"[{datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')}] {log}", flush=True)

# request의 응답 객체를 받아 현재시간의 차이를 계산
def calculate_response_delay(response):
    # 응답 헤더에서 날짜를 추출
    response_time_str = response.headers['Date']
    # 추출한 날짜 문자열을 datetime 객체로 변환
    response_time = datetime.strptime(response_time_str, '%a, %d %b %Y %H:%M:%S GMT')
    # 현재 시간을 UTC로 가져오기
    current_time = datetime.now(timezone.utc).replace(tzinfo = None)
    # 응답 시간과 현재 시간을 비교
    time_difference = abs(current_time - response_time)
    # 시간 차이를 반환
    return time_difference

# 받은 정보들로 get 요청을 보내고 json을 응답받는다. json 데이터 값인 xml을 추출하여 문자열로 리턴한다.
def get_request_to_cgv_api(url, cookies, headers, json_data, target_name):
    response = requests.post(
        url = url,
        cookies = cookies,
        headers = headers,
        json = json_data,
        verify = False,
    )
    # 응답 본문 추출
    response_body = response.content
    save_log_info(f'{target_name} response delay : {calculate_response_delay(response)}', True)
    # UTF-8 디코딩
    response_text = response_body.decode('utf-8-sig')
    # JSON 데이터 파싱
    data = json.loads(response_text)
    # DATA 값 추출 및 디코딩
    xml_string = data['d']['DATA']
    # 응답결과 리턴
    return xml_string

# XML 문자열을 받아서 PlayDays 태그를 XML 문자열로 반환
def extract_playdays(xml_string):
    try:
        # 문자열로 주어진 XML을 파싱
        xml = ET.fromstring(xml_string)
        # 'PlayDays' 태그를 찾아서 해당 내용을 리턴
        playdays = xml.find('.//PlayDays')
        return ET.tostring(playdays, encoding='unicode', method='xml') if playdays is not None else None
    except:
        return ""

# XML 문자열과 태그를 받아서 해당 태그를 모두 XML 문자열로 반환
def extract_xml_object_by_tag(xml_string, tag):
    try:
        # 문자열로 주어진 XML을 파싱
        xml = ET.fromstring(xml_string)
        # 태그를 모두 찾아서 리스트로 변환
        data = xml.findall(f'.//{tag}')
        return ''.join([ET.tostring(item, encoding='unicode', method='xml') for item in data] if data is not None else [])
    except:
        return ""

# 문자열과 태그를 받아서 해당 태그 사이의 문자열을 모두 반환
def extract_text_between_tag(xml_string, tag):
    # 동적으로 정규 표현식 패턴 생성
    pattern = re.compile(r'<{}>(.*?)</{}>'.format(re.escape(tag), re.escape(tag)))
    # 찾은 문자열을 ', '로 구분하여 하나의 문자열로 연결하여 반환
    return ', '.join(pattern.findall(xml_string))

# XML 문자열을 받아 태그 사이의 값을 모두 추출하여 ", "으로 구분된 문자열로 리턴
def extract_all_text_from_xml(xml_string):
    # 동적으로 정규 표현식 패턴 생성
    pattern = re.compile(r'<.*?>(.*?)</.*?>')
    # 찾은 문자열을 ', '로 구분하여 하나의 문자열로 연결하여 반환
    return ', '.join(pattern.findall(xml_string))

# 문자열과 태그를 받아서 해당 태그와 내용을 모두 삭제된 문자열을 반환
def remove_text_between_tag(xml_string, tag):
    # 동적으로 정규 표현식 패턴 생성
    pattern = re.compile(r'<{}>(.*?)</{}>'.format(re.escape(tag), re.escape(tag)))
    # 모든 태그와 내용을 찾아 제거
    return pattern.sub('', xml_string)

# 특별관 예매 오픈 알림에 필요 없는 태그 제거하기
def screen_remove_useless_tags(xml_string):
    useless_tags = {"PLAY_YMD", "GROUP_CD", "MOVIE_CD", "RATING_CD", "PLATFORM_CD", "TRANS_CD", "PLATFORM_ATTR_CD", "MOVIE_COLLAGE_YN", "TICKET_RATE", "STAR_POINT", "SOUNDX_YN", "THIRD_ATTR_CD", "MOVIE_ATTR_CD", "MOVIE_PKG_YN", "MOVIE_NOSHOW_YN", "POSTER", "MOVIE_IDX", "THIRD_ATTR_NM", }
    for tag in useless_tags:
        xml_string = remove_text_between_tag(xml_string, tag)
    return xml_string