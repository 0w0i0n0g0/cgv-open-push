import unittest
from cgv_open_push_function import *
from cgv_open_push_global_variable import *

class CgvOpenPushTest(unittest.TestCase):

    # 테스트 시작
    def setUp(self):
        print('\n')

    # send_curl_to_cgv_multiple 테스트
    def test_send_curl_to_cgv_multiple(self):
        for data in enumerate(json_data):
            print(f"test_send_curl_to_cgv_multiple to {target_name[data[0]]}\n")
            response = get_request_to_cgv_api(url, cookies, headers, data[1], target_name[data[0]])
            위치 = extract_text_between_tag(response, "THEATER_NM")
            print(f"위치 : {위치}")
            유형 = extract_text_between_tag(response, "RATING_NM")
            print(f"유형 : {유형}")
            영화 = extract_text_between_tag(response, "MOVIE_GROUP_NM")
            print(f"영화 : {영화}")

    # send_push_to_private_ntfy 테스트
    def test_send_push_to_private_ntfy(self):
        res = send_push_to_private_ntfy(f"test_send_push_to_private_ntfy\n푸시 알림 테스트입니다.", "test_send_push_to_private_ntfy")
        print(f"test_send_push_to_private_ntfy : {res}")

    # send_push_to_ntfy 테스트
    def test_send_push_to_ntfy(self):
        res = send_push_to_ntfy(f"test_send_push_to_ntfy\n푸시 알림 테스트입니다.", "test_send_push_to_ntfy")
        print(f"test_send_push_to_ntfy : {res}")

if __name__ == '__main__':
    unittest.main()