from datetime import datetime, timezone
import json
import re
import requests
import xml.etree.ElementTree as ET
import logging
from cgv_open_push_global_variable import ntfy_token

# request의 응답 객체의 시간과 현재시간의 차이를 계산
def get_time_difference(response):
    # 응답 헤더에서 날짜를 추출
    response_time_str = response.headers['Date']
    # 추출한 날짜 문자열을 datetime 객체로 변환
    response_time = datetime.strptime(response_time_str, '%a, %d %b %Y %H:%M:%S GMT')
    # 현재 시간을 UTC로 가져오기
    current_time = datetime.now(timezone.utc).replace(tzinfo = None)
    # 응답 시간과 현재 시간을 비교
    time_difference = current_time - response_time
    # 시간 차이를 반환
    return time_difference

# cgv에서 영화 예매 정보 가져오기
def send_curl_to_cgv_multiple(url, cookies, headers, json_data, target_name):
    response = requests.post(
        url = url,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    # 응답 본문 추출
    response_body = response.content
    logging.debug(f'{target_name} 서버가 응답에 걸린 시간 : {get_time_difference(response)}')
    # UTF-8 디코딩
    response_text = response_body.decode('utf-8-sig')
    # JSON 데이터 파싱
    data = json.loads(response_text)
    # DATA 값 추출 및 디코딩
    data_value = data['d']['DATA']
    # 응답결과 리턴
    return data_value

# 변경사항 푸시알림 보내기
def send_ntfy_push(result, target_name):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        # ntfy 서버 토큰
        'Authorization': ntfy_token,
    }
    data = f'예매 오픈 알림!\n{result}\n{target_name}'.encode()
    response = requests.post(f'http://serverkorea.duckdns.org/{target_name}', headers=headers, data=data)
    logging.debug(f'{target_name} 서버의 send_ntfy_push : {response}')

# 정상작동 확인용 푸시알림 보내기
def send_ntfy_push_health_check(text, target_name):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        # ntfy 서버 토큰
        'Authorization': ntfy_token,
    }
    data = f'{target_name}\n{text}'.encode()
    response = requests.post(f'http://serverkorea.duckdns.org/SERVER', headers=headers, data=data)
    logging.debug(f'{target_name} 서버의 send_ntfy_push_health_check : {response}')

# 서버 정상작동 푸시알림 보내기
def send_ntfy_push_server(string, target_name):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'{string}'.encode()
    response = requests.post('http://ntfy.sh/CGVOPENPUSHSERVER', headers=headers, data=data)
    logging.debug(f'{target_name} 서버의 send_ntfy_push_server : {response}')

# XML 객체를 받아서 PlayDays 태그를 XML 객체로 반환
def extract_playdays(xml_string):
    # 문자열로 주어진 XML을 파싱
    root = ET.fromstring(xml_string)
    # 'PlayDays' 태그를 찾아서 해당 내용을 리턴
    playdays = root.find('.//PlayDays')
    return ET.tostring(playdays, encoding='unicode', method='xml') if playdays is not None else None

# 문자열을 받아서 FORMAT_DATE 태그 사이의 문자열을 모두 반환
def extract_format_date(xml_string):
    # 정규 표현식을 사용하여 <FORMAT_DATE>과 </FORMAT_DATE> 사이의 모든 문자열 찾기
    pattern = re.compile(r'<FORMAT_DATE>(.*?)</FORMAT_DATE>')
    # 찾은 문자열을 ', '로 구분하여 하나의 문자열로 연결하여 반환
    return ', '.join(pattern.findall(xml_string))

# 문자열과 태그를 받아서 해당 태그 사이의 문자열을 모두 반환
def extract_xml_content_by_tag(xml_string, tag):
    # 동적으로 정규 표현식 패턴 생성
    pattern = re.compile(r'<{}>(.*?)</{}>'.format(tag, tag))
    # 찾은 문자열을 ', '로 구분하여 하나의 문자열로 연결하여 반환
    return ', '.join(pattern.findall(xml_string))