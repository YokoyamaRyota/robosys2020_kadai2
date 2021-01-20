#!/usr/bin/env python3
import smbus
import rospy
import time
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
acc_addr = 0x19
gyro_addr = 0x69
mag_addr = 0x13

bus = smbus.SMBus(1)
time.sleep(1)
rospy.init_node('Imu')
imupub = rospy.Publisher('Imu_pub',Imu,queue_size=10)
magpub = rospy.Publisher('mag_pub',MagneticField,queue_size=10)
rate = rospy.Rate(10)
imu = Imu()
mag = MagneticField()
data = [0]*6
bus.write_byte_data(mag_addr,0x4b,0x01)
bus.write_byte_data(mag_addr,0x4c,0x00)
bus.write_byte_data(mag_addr,0x4e,0x84)
bus.write_byte_data(mag_addr,0x51,0x04)
bus.write_byte_data(mag_addr,0x52,0x16)
while not rospy.is_shutdown():
    for i in range(6):
        data[i] = bus.read_byte_data(acc_addr,2+i)

    x_accl = ((data[1]*256)+(data[0]&0xF0))/16
    if x_accl > 2047:
        x_accl = x_accl-4096
    y_accl = ((data[3]*256)+(data[2]&0xF0))/16
    if y_accl > 2047:
        y_accl = y_accl-4096
    z_accl = ((data[5]*256)+(data[4]&0xF0))/16
    if z_accl > 2047:
        z_accl = z_accl-4096
    x_accl = x_accl*0.0098
    y_accl = y_accl*0.0098
    z_accl = z_accl*0.0098

    for i in range(6):
        data[i] = bus.read_byte_data(gyro_addr,2+i)
    
    x_gyro=(data[1]*256)+data[0]
    if x_gyro > 32767:
        x_gyro = x_gyro-65536
    y_gyro=(data[3]*256)+data[2]
    if y_gyro > 32767:
        y_gyro = y_gyro-65536
    z_gyro=(data[5]*256)+data[4]
    if z_gyro > 32767:
        z_gyro = z_gyro-65536
    x_gyro = x_gyro*0.0038*0.0174
    y_gyro = y_gyro*0.0038*0.0174
    z_gyro = z_gyro*0.0038*0.0174
    
    for i in range(6):
        data[i] = bus.read_byte_data(mag_addr,0x42+i)

    x_mag = ((data[1]*256)+(data[0]&0xF8))/8
    if x_mag > 4095:
        x_mag = x_mag-8192
    y_mag = ((data[3]*256)+(data[2]&0xF8))/8
    if y_mag > 4095:
        y_mag = y_mag-8192
    z_mag = ((data[5]*256)+(data[4]&0xFE))/2
    if z_mag > 16383:
        z_mag = z_mag-32768

    
    imu.linear_acceleration.x = x_accl
    imu.linear_acceleration.y = y_accl
    imu.linear_acceleration.z = z_accl
    imu.angular_velocity.x = x_gyro
    imu.angular_velocity.y = y_gyro
    imu.angular_velocity.z = z_gyro

    mag.magnetic_field.x = x_mag
    mag.magnetic_field.y = y_mag
    mag.magnetic_field.z = z_mag

    imupub.publish(imu)
    magpub.publish(mag)

    rate.sleep()


