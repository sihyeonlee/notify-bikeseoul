import requests
from win10toast import ToastNotifier
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler()
scheduler.start()


def parsing_data(data):
    parking_bike = (data['rentBikeStatus']['row'][0]['parkingBikeTotCnt'])

    return int(parking_bike)


def get_realtime_data(key):
    url = "http://openapi.seoul.go.kr:8088/" + key + "/json/bikeList/1262/1262/"                                        # 아직까지 매트릭스 형태의 정류장 정보를 못 구해서 우선 노가다로 과학전시관 찾아냄

    get_url = requests.get(url)

    if get_url.status_code != 200:
        print("Fail to get data")

        return -1

    else:
        result_json_data = get_url.json()

    return result_json_data


def get_auth_key():
    file = open('auth-key.txt', 'r')
    key = file.readline()

    return key


def loop_task(threshold):
    toaster = ToastNotifier()

    auth_key = get_auth_key()
    json_result = get_realtime_data(auth_key)
    bike_cnt = parsing_data(json_result)

    if bike_cnt < threshold:
        toaster.show_toast("현재 따릉이 " + str(bike_cnt) + "개 남았습니다.", "바로 대여하세요.")


bike_low_cnt = int(input("몇 대 이하인 경우 알람을 울릴까요?"))
set_hour = input("어느 시간 대에 알람을 활성화 할까요? ex) 0-23")
set_second = "*/" + str(input("몇 초 주기로 알려드릴까요?"))

scheduler.add_job(loop_task, 'cron', hour=set_hour, second=set_second, id="bike_toaster", args=[bike_low_cnt])

while True:
    pass