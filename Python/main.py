# 1台のAirocoを選択し,過去1週間分のCO2濃度推移をグラフ表示するプログラム

import Airoco
Airoco.set_isLog(True)

if __name__ == "__main__":
    # AirocoのIDは6番を選択
    airoco = Airoco.Airoco(id = 6, day = 7)

    airoco.show_density()
    airoco.show_temperature()
    airoco.show_humidity()


