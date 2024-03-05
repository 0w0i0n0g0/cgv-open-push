from datetime import datetime
import json
import re
import charset_normalizer
import requests
import xml.etree.ElementTree as ET
import logging

def get_time_difference(response):
    # 응답 헤더에서 날짜를 추출합니다.
    response_time_str = response.headers['Date']
    # 추출한 날짜 문자열을 datetime 객체로 변환합니다.
    response_time = datetime.strptime(response_time_str, '%a, %d %b %Y %H:%M:%S GMT')
    # 현재 시간을 UTC로 가져옵니다.
    current_time = datetime.utcnow()
    # 응답 시간과 현재 시간을 비교합니다.
    time_difference = current_time - response_time
    # 시간 차이를 반환합니다.
    return time_difference

def send_curl_to_cgv_multiple(url, cookies, headers, json_data, target):
    response = requests.post(
        url = url,
        cookies=cookies,
        headers=headers,
        json=json_data,
        verify=False,
    )
    # 응답 본문 추출
    response_body = response.content
    logging.debug(f'{target} 응답에 걸린 시간 : {get_time_difference(response)}')
    # 자동 인식 실패 시, 인코딩 정보 추출 시도
    if not response.encoding:
        encoding = charset_normalizer.detect(response_body)['encoding'] or 'utf-8'
        response_body = response_body.decode(encoding)
    # UTF-8 디코딩
    response_text = response_body.decode('utf-8')
    # JSON 데이터 파싱
    data = json.loads(response_text)
    # DATA 값 추출 및 디코딩
    data_value = data['d']['DATA']
    # 응답결과 리턴
    return data_value

def send_ntfy_push(result):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'변경사항 확인!\n{result}'.encode()
    response = requests.post('http://ntfy.sh/CGVIMAXYONGSANOPEN', headers=headers, data=data)
    logging.debug(f'send_ntfy_push : {response}')

def send_ntfy_push_server(string):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = f'CGVIMAXYONGSANOPEN\n{string}'.encode()
    response = requests.post('http://ntfy.sh/CGVIMAXYONGSANOPENSERVER', headers=headers, data=data)
    logging.debug(f'send_ntfy_push_server : {response}')

def save_to_text_file(text, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)

def load_text_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def extract_playdays(xml_string):
    # 문자열로 주어진 XML을 파싱
    root = ET.fromstring(xml_string)
    # 'PlayDays' 태그를 찾아서 해당 내용을 리턴
    playdays = root.find('.//PlayDays')
    return ET.tostring(playdays, encoding='unicode', method='xml') if playdays is not None else None

def extract_format_date(xml_string):
    # 정규 표현식을 사용하여 <FORMAT_DATE>과 </FORMAT_DATE> 사이의 모든 문자열 찾기
    pattern = re.compile(r'<FORMAT_DATE>(.*?)</FORMAT_DATE>')
    # 찾은 문자열을 ','로 구분하여 하나의 문자열로 연결하여 반환
    return ', '.join(pattern.findall(xml_string))