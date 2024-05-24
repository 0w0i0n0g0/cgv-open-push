import unittest
from cgv_open_push_function import *
from cgv_open_push_global_variable import *

class CgvOpenPushTest(unittest.TestCase):

    # 테스트 시작
    def setUp(self):
        print('\n')

    # send_curl_to_cgv_multiple 테스트
    def test_send_curl_to_cgv_multiple(self):
        for data in enumerate(movie_json_data):
            print(f"test_send_curl_to_cgv_multiple to {movie_target_name[data[0]]}\n")
            response = get_request_to_cgv_api(movie_url, movie_cookies, movie_headers, data[1], movie_target_name[data[0]])
            위치 = extract_text_between_tag(response, "THEATER_NM")
            print(f"위치 : {위치}")
            유형 = extract_text_between_tag(response, "RATING_NM")
            print(f"유형 : {유형}")
            영화 = extract_text_between_tag(response, "MOVIE_GROUP_NM")
            print(f"영화 : {영화}")
            print('\n')

        for data in enumerate(screen_json_data):
            print(f"test_send_curl_to_cgv_multiple to {screen_target_name[data[0]]}\n")
            response = get_request_to_cgv_api(screen_url, screen_cookies, screen_headers, data[1], screen_target_name[data[0]])
            위치 = extract_text_between_tag(response, "THEATER_NM")
            print(f"위치 : {위치}")
            유형 = extract_text_between_tag(response, "RATING_NM")
            print(f"유형 : {유형}")
            print('\n')

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