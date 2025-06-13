# 内部ライブラリ
import time
import csv
import datetime

# 外部ライブラリ
import requests
import matplotlib.pyplot as plt
import numpy as np

# ユーザ定義ライブラリ
from Logger import log, log_wait, log_result, set_isLog



class Airoco:
    """Airoco sensor class for fetching and displaying data from Airoco sensors"""


    # ---- Static Fields ---- #
    SENSOR_NAME: list = [
        "R3-401", # id = 0
        "R3-403", # id = 1
        "R3-301", # id = 2
        "R3-4F_EH", # id = 3
        "R3-3F_EH", # id = 4
        "R3-1F_EH", # id = 5
        "R3-B1F_EH" # id = 6
    ]
    SENSOR_NAME_FULL: list = [
        "Ｒ３ー４０１", # id = 0
        "Ｒ３ー４０３", # id = 1
        "Ｒ３ー３０１", # id = 2
        "Ｒ３ー４Ｆ_ＥＨ", # id = 3
        "Ｒ３ー３Ｆ_ＥＨ", # id = 4
        "Ｒ３ー１Ｆ_ＥＨ", # id = 5
        "Ｒ３ーB１Ｆ_ＥＨ" # id = 6
    ]
    URL: str = "https://airoco.necolico.jp/data-api/day-csv?id=CgETViZ2&subscription-key=6b8aa7133ece423c836c38af01c59880"
    TRY: int = 3


    # ---- Instance Fields ---- #
    # センサーのID，名前，全角
    id: int
    name: str
    name_full: str

    cache_specific_sensor: np.ndarray = None
    cache_all_sensors: list[csv.reader] = []
    can_use_cache_all_sensors: bool = False
    can_use_cache_specific_sensor: bool = False


    # ---- Constructor ---- #
    def __init__(self, id = 0, day = 7) -> None:
        self.set_id(id)
        self.day = day
        log(f"Initialized Airoco sensor: {self.name} (ID: {id})")


    # ---- Setters and Getters ---- #
    def set_id(self, id) -> None:
        if id < 0 or id >= len(self.SENSOR_NAME):
            log(f"Invalid sensor ID: {id}. Must be between 0 and {len(self.SENSOR_NAME) - 1}.")
            raise ValueError("Invalid sensor ID")
        self.id = id
        self.name = self.SENSOR_NAME[id]
        self.name_full = self.SENSOR_NAME_FULL[id]
        log(f"Sensor ID set to {self.id} ({self.name})")
        self.can_use_cache_specific_sensor = False

    def set_day(self, day) -> None:
        if day <= 0:
            log(f"Invalid day value: {day}. Must be greater than 0.")
            raise ValueError("Day must be greater than 0")
        self.day = day
        log(f"Day set to {self.day} for sensor: {self.name}")
        self.can_use_cache_all_sensors = False
        self.can_use_cache_specific_sensor = False


    # ---- Methods ---- #
    def fetch_url(self, tt) -> csv.reader:
        url = f"{self.URL}&startDate={tt}"
        for attempt in range(self.TRY):
            log_wait(f"Fetching data from URL ({attempt+1}/{self.TRY}): {url} ...")
            res = requests.get(url)
            if res.status_code == 200:
                log_result("OK")
                break
            log_result("FAILED")
        else:
            raise Exception(f"Failed to fetch data: {res.status_code} {res.reason}")
        return csv.reader(res.text.strip().splitlines())

    def get_data_all_sensors(self, use_cache = True) -> list:
        if self.cache_all_sensors != [] and use_cache and self.can_use_cache_all_sensors:
            log(f"Using cached all data for sensor: {self.name}")
            return self.cache_all_sensors
        log(f"Fetching all data")
        resList = [[] for _ in range(len(self.SENSOR_NAME))]
        start_time = int(time.time()) - 3600 * 24 * self.day
        for day in range(self.day):
            tt = start_time + 3600 * 24 * day
            for row in self.fetch_url(tt):
                for index, sensor_name_full in enumerate(self.SENSOR_NAME_FULL):
                    if row[1] == sensor_name_full:
                        resList[index].append(list(map(float, row[3:7])))
                        break
        log(f"All data fetched successfully: {self.name}")
        # キャッシュを更新
        self.cache_all_sensors = resList
        self.can_use_cache_all_sensors = True
        return resList

    def get_data_specific_sensor(self, use_cache = True) -> np.ndarray:
        if self.cache_specific_sensor is not None and use_cache and self.can_use_cache_specific_sensor:
            log(f"Using cached data for sensor: {self.name}")
            return self.cache_specific_sensor
        resList = self.get_data_all_sensors()
        log(f"Getting data for sensor: {self.name}")
        data = np.array(resList[self.id])
        if data.size == 0:
            log(f"No data found for sensor: {self.name}")
            raise ValueError(f"No data found for sensor: {self.name}")
        log(f"Data for sensor {self.name} fetched successfully")
        # キャッシュを更新
        self.cache_specific_sensor = data
        self.can_use_cache_specific_sensor = True
        return data


    # ---- Plotting Methods ---- #
    def show_density(self) -> None:
        log(f"Showing density for sensor: {self.name}")
        data = self.get_data_specific_sensor()
        date = [datetime.datetime.fromtimestamp(ts) for ts in data[:,3]]
        plt.title(f"CO2 concentration trend: {self.name}")
        plt.plot(date, data[:,0])
        plt.xlabel('Time [s]')
        plt.ylabel('CO2 density [ppm]')
        plt.xticks(rotation=45)  # x軸のラベルを斜めに表示
        plt.tight_layout()  
        plt.show()

    def show_temperature(self) -> None:
        log(f"Showing temperature for sensor: {self.name}")
        data = self.get_data_specific_sensor()
        date = [datetime.datetime.fromtimestamp(ts) for ts in data[:,3]]
        plt.title(f"Temperature trend: {self.name}")
        plt.plot(date, data[:,1])
        plt.xlabel('Time [s]')
        plt.ylabel('Temperature [deg]')
        plt.xticks(rotation=45)  # x軸のラベルを斜めに表示
        plt.tight_layout()  
        plt.show()

    def show_humidity(self) -> None:
        log(f"Showing humidity for sensor: {self.name}")
        data = self.get_data_specific_sensor()
        date = [datetime.datetime.fromtimestamp(ts) for ts in data[:,3]]
        plt.title(f"Humidity trend: {self.name}")
        plt.plot(date, data[:,2])
        plt.xlabel('Time [s]')
        plt.ylabel('Relative humidity [%]')
        plt.xticks(rotation=45)  # x軸のラベルを斜めに表示
        plt.tight_layout()       # レイアウト調整でラベルが重ならないようにする
        plt.show()



if __name__ == "__main__":
    print("This is a library module.")