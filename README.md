# ロボットシステム学課題2
## 概要
raspberry pi3 model b+上で秋月のbmx055使用９軸センサーモジュールと通信するためのrosのパッケージです。
## 動作環境
os ubuntu20.04
## 使用部品
1. raspberry pi3 model b+
2. bmx055使用９軸センサーモジュール
## 動画
動作中の動画です。
　　　
   
[![Audi R8](http://img.youtube.com/vi/zCPmWQxajbs/1.jpg)](https://studio.youtube.com/video/zCPmWQxajbs/edit)
## インストール方法
次のコマンドを実行します。
```
cd ~/catkin_ws/src
git clone https://github.com/YokoyamaRyota/robosys2020_kadai2.git
cd ..
catkin_make
cd src/robosys2020_kadai2/scripts
chmod +x bmx055.py
```
## 実行方法
秋月のbmx055使用９軸センサーモジュールでは裏のJP7をショートし、GNDと3V3を繋げSDAとGPIO2,SCLとGPIO3を繋げます。その後次のコマンドを実行します。
```
roscore
rosrun mypkg bmx055.py
```
通信ができているか別の端末で確認します。
```
rostopic echo Imu_pub
rostopic echo mag_pub
```
Imu_pubは角速度と加速度、mag_pubは磁気センサの値が送られています。
センサの傾きによって値が変化すれば成功です。

## ライセンス
[GNU General Public License v3.0](https://github.com/YokoyamaRyota/robosys2020_kadai1/blob/main/COPYING)

