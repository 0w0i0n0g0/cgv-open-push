import os

##################################################
# ENV
ntfy_token = os.environ["NTFY_TOKEN"]
private_ntfy_server_address = os.environ["PRIVATE_NTFY_SERVER_ADDRESS"]
private_ntfy_prometheus_address = os.environ["PRIVATE_NTFY_PROMETHEUS_ADDRESS"]



##################################################
# cgv_open_push_movie.py

movie_url = 'http://ticket.cgv.co.kr/CGV2011/RIA/CJ000.aspx/CJ_TICKET_SCHEDULE_TOTAL_PLAY_YMD'

movie_cookies = {
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

movie_headers = {
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
movie_json_data = [
    # # 듄-파트2 용산아이파크몰 IMAX관
    # {
    #     "REQSITE": "x02PG4EcdFrHKluSEQQh4A==",
    #     "TheaterCd": "LMP+XuzWskJLFG41YQ7HGA==",
    #     "ISNormal": "3y+GIXzg3xKpOjlKjH8+Fg==",
    #     "MovieGroupCd": "bNQovwyoamC5EsbGvSDIqw==",
    #     "ScreenRatingCd": "nG6tVgEQPGU2GvOIdnwTjg==",
    #     "MovieTypeCd": "/Saxvehmz4RPKZDKNMvSKQ==",
    #     "Subtitle_CD": "nG6tVgEQPGU2GvOIdnwTjg==",
    #     "SOUNDX_YN": "nG6tVgEQPGU2GvOIdnwTjg==",
    #     "Third_Attr_CD": "nG6tVgEQPGU2GvOIdnwTjg==",
    #     "Language": "zqWM417GS6dxQ7CIf65+iA==",
    # },
    # # 고질라 X 콩-뉴 엠파이어 용산아이파크몰 IMAX관
    # {
    #     'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
    #     'TheaterCd': 'LMP+XuzWskJLFG41YQ7HGA==',
    #     'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
    #     'MovieGroupCd': 'rOV6MXDmdX4t5y4MUwm1SQ==',
    #     'ScreenRatingCd': 'kXwoR3tnLM/+Tu0BILP3Qg==',
    #     'MovieTypeCd': '/Saxvehmz4RPKZDKNMvSKQ==',
    #     'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    # },
    # # 극장판하이큐!!쓰레기장의결전 용산아이파크몰 IMAX관
    # {
    #     'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
    #     'TheaterCd': 'LMP+XuzWskJLFG41YQ7HGA==',
    #     'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
    #     'MovieGroupCd': 'rScFvvwEyPojN0wB3iaAJg==',
    #     'ScreenRatingCd': 'kXwoR3tnLM/+Tu0BILP3Qg==',
    #     'MovieTypeCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    # },
    # # 혹성탈출-새로운시대 용산아이파크몰 IMAX관
    # {
    #     'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
    #     'TheaterCd': 'LMP+XuzWskJLFG41YQ7HGA==',
    #     'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
    #     'MovieGroupCd': 'kWm88LTxi790bmsk4bHiOg==',
    #     'ScreenRatingCd': 'kXwoR3tnLM/+Tu0BILP3Qg==',
    #     'MovieTypeCd': '/Saxvehmz4RPKZDKNMvSKQ==',
    #     'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    # },
    # #퓨리오사-매드맥스사가 용산아이파크몰 IMAX관
    # {
    #     'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
    #     'TheaterCd': 'LMP+XuzWskJLFG41YQ7HGA==',
    #     'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
    #     'MovieGroupCd': 'Eclx6HdxURDc7ZSCEC1oVg==',
    #     'ScreenRatingCd': 'kXwoR3tnLM/+Tu0BILP3Qg==',
    #     'MovieTypeCd': '/Saxvehmz4RPKZDKNMvSKQ==',
    #     'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    # },
    # # 나쁜녀석들-라이드오어다이 용산아이파크몰 IMAX관
    # {
    # 'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
    # 'TheaterCd': 'LMP+XuzWskJLFG41YQ7HGA==',
    # 'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
    # 'MovieGroupCd': 'mgqEaWmqb6vUNc0jFeR+oQ==',
    # 'ScreenRatingCd': 'kXwoR3tnLM/+Tu0BILP3Qg==',
    # 'MovieTypeCd': '/Saxvehmz4RPKZDKNMvSKQ==',
    # 'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    # 'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
    # 'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    # 'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    # },
    # 명탐정코난-100만달러의펜타그램 용산아이파크몰 IMAX관
    # {
    #     'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
    #     'TheaterCd': 'LMP+XuzWskJLFG41YQ7HGA==',
    #     'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
    #     'MovieGroupCd': 'sotE7BPGwguNFSYUhbmAmg==',
    #     'ScreenRatingCd': 'kXwoR3tnLM/+Tu0BILP3Qg==',
    #     'MovieTypeCd': '/Saxvehmz4RPKZDKNMvSKQ==',
    #     'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
    #     'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    # },
]

# 변경사항을 확인할 타겟 이름 (json_data 순서대로)
movie_target_name = [
    # "DUNE-PART2-YONGSAN-IMAX",
    # "GODZILLA-KONG",
    # "HAIKU-YONGSAN-IMAX",
    # "APES-YONGSAN-IMAX",
    # "FURIOSA-YONGSAN-IMAX",
    # "BADBOYS-YONGSAN-IMAX",
    # "CONAN-YONGSAN-IMAX",
]



##################################################
# cgv_open_push_screen.py

screen_url = 'http://ticket.cgv.co.kr/CGV2011/RIA/CJ000.aspx/CJ_TICKET_SCHEDULE_TOTAL_PLAY_YMD'

screen_cookies = {
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

screen_headers = {
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

screen_json_data = [
    # 용산아이파크몰 IMAX관
    {
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
    },
    # 용산아이파크몰 4DX관
    {
        'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
        'TheaterCd': 'LMP+XuzWskJLFG41YQ7HGA==',
        'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
        'MovieGroupCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'ScreenRatingCd': '9sxNW0kL/ZE3ioyEu1Em8w==',
        'MovieTypeCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    },
    # 서면 IMAX관
    {
        'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
        'TheaterCd': 'VCtDd13tWp85DXhl1ss+bw==',
        'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
        'MovieGroupCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'ScreenRatingCd': 'kXwoR3tnLM/+Tu0BILP3Qg==',
        'MovieTypeCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    },
    # 영등포 IMAX관
    {
        'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
        'TheaterCd': 'Y5qC4mHnqFvPnE5/3487AQ==',
        'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
        'MovieGroupCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'ScreenRatingCd': 'kXwoR3tnLM/+Tu0BILP3Qg==',
        'MovieTypeCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    },
    # 영등포 SCREENX관
    {
        'REQSITE': 'x02PG4EcdFrHKluSEQQh4A==',
        'TheaterCd': 'Y5qC4mHnqFvPnE5/3487AQ==',
        'ISNormal': 'ECFppiyFz/nvSGsg7VwPQw==',
        'MovieGroupCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'ScreenRatingCd': '1WlMxB/T2xWstAhFsiNSfQ==',
        'MovieTypeCd': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Subtitle_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'SOUNDX_YN': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Third_Attr_CD': 'nG6tVgEQPGU2GvOIdnwTjg==',
        'Language': 'zqWM417GS6dxQ7CIf65+iA==',
    },
]

screen_target_name = [
    "YONGSAN-IMAX",
    "YONGSAN-4DX",
    "SEOMYEON-IMAX",
    "YEONGDEUNGPO-IMAX",
    "YEONGDEUNGPO-SCREENX",
]