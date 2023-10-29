from machine import Pin 
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

# Bluetooth Low Energy (BLE) オブジェクトを作成する。
ble = bluetooth.BLE()

# BLE オブジェクトを使用して BLESimplePeripheral クラスのインスタンスを作成。
sp = BLESimplePeripheral(ble)

# オンボード LED の Pin オブジェクトを作成し、出力として設定。
led = Pin("LED", Pin.OUT)

# LED の状態を 0 (オフ) に初期化します。
led_state = 0
led.value(led_state)

# 受信したデータを処理するコールバック関数
def on_rx(data):
    # Bluetoothで受信したデータをコンソールに表示。
    print("Recive by central {}".format(data))
    sp.send("Responce by peripheral {} : {}".format(data,"any value"))

# メインループ
while True:
    # BLE 接続が確立されているかどうかを確認。
    if sp.is_connected():
        # データ受信用のコールバック関数を設定。
        sp.on_write(on_rx)