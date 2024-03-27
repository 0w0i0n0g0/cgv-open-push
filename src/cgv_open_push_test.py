import unittest
from cgv_open_push_function import *
from cgv_open_push_global_variable import *

class CgvOpenPushTest(unittest.TestCase):

    # send_curl_to_cgv_multiple 테스트
    def test_send_curl_to_cgv_multiple(self):
        for data in enumerate(json_data):
            response = send_curl_to_cgv_multiple(url, cookies, headers, data[1], target_name[data[0]])
            print(extract_xml_content_by_tag(response, "THEATER_NM"))
            print(extract_xml_content_by_tag(response, "RATING_NM"))
            print(extract_xml_content_by_tag(response, "MOVIE_GROUP_NM"))

    # send_ntfy_push_health_check 테스트
    def test_send_ntfy_push_health_check(self):
        send_ntfy_push_health_check("test", "test")

if __name__ == '__main__':
    unittest.main()