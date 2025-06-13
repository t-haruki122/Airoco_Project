import requests
import datetime

res = requests.get('https://airoco.necolico.jp/data-api/latest?id=CgETViZ2&subscription-key=6b8aa7133ece423c836c38af01c59880')
# print(res.status_code)
# print(res.text)
for i in range(9):
    res_json = res.json()[i]
    # print(res_json)
    sensorNumber = res_json['sensorNumber']
    sensorName = res_json['sensorName']
    print(sensorNumber, sensorName)
    co2 = res_json['co2']
    if co2==None: continue # データ無ければ次
    temperature = res_json['temperature']
    relativeHumidity = res_json['relativeHumidity']
    timestamp = res_json['timestamp']
    dt = datetime.datetime.fromtimestamp(timestamp)
    print(f'CO2濃度={co2}[ppm], 気温={temperature}[deg], 相対湿度={relativeHumidity}[%], タイムスタンプ={dt}\n');
