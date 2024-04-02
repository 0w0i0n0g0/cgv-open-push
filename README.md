<div align="center">

# CGV 예매 오픈 알리미

<p align="center">
  <img src="./img/logo.png" width="160"/>
</p>

By_0w0i0n0g0

<br>
<br>

## [서버가 작동 중인지 여기서 확인하세요!](http://serverkorea.duckdns.org:5000)

###  http://serverkorea.duckdns.org:5000

<br>
<br>

## 목차

[알림 받기](#알림-받기)

[Description](#description)

[Features](#features)

[Stack](#stack)

[License](#license)

</div>

<br>
<br>

## 🔎 현재 예매 오픈 알리미가 지켜보고 있는 영화는? (2024/04/03 기준)

- 듄-파트2 / 용산아이파크몰 / IMAX관
- 고질라 X 콩: 뉴 엠파이어 / 용산아이파크몰 / IMAX관

<br>

### 추가 건의나 문의사항은 [issues](https://github.com/0w0i0n0g0/cgv-open-push/issues)에 남겨주세요!

https://github.com/0w0i0n0g0/cgv-open-push/issues

<br>
<br>

## 🔔 알림 받는 방법!

### 먼저 ntfy 앱을 다운받으세요.

- [구글 플레이스토어](https://play.google.com/store/apps/details?id=io.heckel.ntfy)

- [애플 앱스토어](https://apps.apple.com/us/app/ntfy/id1625396347)

> 예매 오픈 알림을 받으려면 설정에서 앱 알림을 허용해주세요.

<br>

### 구독을 추가하세요.

알림을 받기 위해 ```Add subscription```을 눌러 구독을 추가해야 해요.

먼저 밑의 예시와 같이 ```Topic name```에 밑의 리스트 중에서 알림받고 싶은 것을 골라 입력해주세요. 

> 정확히 입력해야 합니다.

<p align="center">
  <img src="./img/topic-name.png" width="300"/>
</p>

<br>

---

#### 듄-파트2 / 용산아이파크몰 / IMAX관

```
DUNE-PART2-YONGSAN-IMAX
```

> 복사 붙여넣기 해주세요.

<br>

#### 고질라 X 콩: 뉴 엠파이어 / 용산아이파크몰 / IMAX관

```
GODZILLA-KONG
```

> 복사 붙여넣기 해주세요.

---

<br>


그리고 다음과 같이 ```Use another server```를 활성화 후, ```Service URL```에

```
http://serverkorea.duckdns.org
```

> 복사 붙여넣기 해주세요.

를 입력해주세요.

<p align="center">
  <img src="./img/use-another-server.png" width="300"/>
</p>

> 만약 오류메세지가 뜨면서 실패하게 된다면 조금 기다린 후 다시 시도해주세요. 개인 서버로 운영 중이여서 24시간 정상작동을 보장할 수 없습니다.

<br>
<br>

## 🎉 이제 다 끝났어요!

__도움이 되었다면 Star⭐를 눌러주세요. 큰 도움이 됩니다!__

<br>

### 알람은 이렇게 와요.


<p align="center">
  <img src="./img/example.png" width="300"/>
</p>

> 실제 가동중인 서버에서 CGV 용산아이파크몰 IMAX관 듄 파트2 4주차 (2024/03/23 ~ 2024/03/29) 예매 오픈 당시 실시간으로 울린 알림이에요.

<br>
<br>

> 이전 알림 더보기
>> [CGV 용산아이파크몰 IMAX관 듄 파트2 (3)](https://github.com/0w0i0n0g0/cgv-open-push/blob/main/img/previous-push-notifications/dune-part2-3.png)
>>
>> [CGV 용산아이파크몰 IMAX관 듄 파트2 (4)](https://github.com/0w0i0n0g0/cgv-open-push/blob/main/img/previous-push-notifications/dune-part2-4.png)
>>
>> [CGV 용산아이파크몰 IMAX관 듄 파트2 (5)](https://github.com/0w0i0n0g0/cgv-open-push/blob/main/img/previous-push-notifications/dune-part2-5.png)
>>
>> [CGV 용산아이파크몰 IMAX관 고질라 X 콩: 뉴 엠파이어 (1)](https://github.com/0w0i0n0g0/cgv-open-push/blob/main/img/previous-push-notifications/godzilla-kong-1.png)

<br>
<br>

## Description

- 

<br>
<br>

## Features

- Send Push Notification
  - http://serverkorea.duckdns.org/{target_name}
    - Push notification when new date detected from *target_name*.

- Health Check
  - http://serverkorea.duckdns.org:5000
    - Server status
  - http://ntfy.sh/CGVOPENPUSHSERVER
  - http://serverkorea.duckdns.org/SERVER
    - Push notification when server start, end and error.

- Server Port
  - Internal
    - http://192.168.0.17 : nginx
    - http://192.168.0.17/monitoring : eZ Server monitor
    - http://192.168.0.17:9999 : private ntfy server
    - http://192.168.0.17:9090 : matrix
    - http://192.168.0.17:3000 : Grafana
    - http://192.168.0.17:9010 : Prometheus
    - http://192.168.0.17:5000: Server status
  - External
    - http://serverkorea.duckdns.org : private ntfy server
    - http://serverkorea.duckdns.org:5000 : Server status

- Logging
  - cgv-open-push.log
    - maxBytes=5\*1024\*1024, backupCount=3, encoding='utf-8'

- Testing
  - cgv_open_push_test.py
    - test_send_curl_to_cgv_multiple
    - test_send_ntfy_push_health_check

- Autostart after Boot
  - sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
    - @bash /home/pi/afterstart.sh
  - afterstart.sh

```bash
#!/bin/bash
python cgv_open_push_main.py &
python cgv_open_push_status.py &
echo 'raspberry' | sudo -S ntfy serve
cd prometheus
./prometheus --web.listen-address=:9010
```

<br>
<br>

## Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Debian](https://img.shields.io/badge/Debian-D70A53?style=for-the-badge&logo=debian&logoColor=white)

<br>
<br>

## License

**AGPL-3.0 license**

Read full license [here](https://github.com/0w0i0n0g0/cgv-open-push/blob/main/LICENSE).

logo image - 
<a href="https://kr.freepik.com/free-photo/3d-render-notification-bell-icon-new-email-message_34503708.htm#query=%EC%95%8C%EB%A6%BC%20%EC%95%84%EC%9D%B4%EC%BD%98&position=0&from_view=keyword&track=ais&uuid=0303dc60-e421-4177-8ab2-29b1326ae712">작가 upklyak</a> 출처 Freepik