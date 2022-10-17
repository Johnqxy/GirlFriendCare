#!/usr/bin/python3
# coding=utf-8
import datetime,pytz
import os
import time

import json
import requests


def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    bee = eed.json()  # 返回的数据
    english = bee['content']
    zh_CN = bee['note']
    str = '【奇怪的知识】\n' + english + '\n' + zh_CN
    return str


def BarkPush(info, type):  # CoolPush酷推
    if type == 0:
        api = "https://api.day.app/RPsaiEemhQrS6zCchywL4j/小钱跟你说：Have a nice day!/" + str(info) + '?sound=birdsong'
    if type == 1:
        api = "https://api.day.app/RPsaiEemhQrS6zCchywL4j/小钱跟你说:生日快乐！我的宝贝~/" + str(
            info) + '?sound=birdsong'
    if type == 2:
        api = "https://api.day.app/RPsaiEemhQrS6zCchywL4j/小钱跟你说:今天别忘了祝他生日快乐/" + str(
            info) + '?sound=birdsong'
    if type == 3:
        api = "https://api.day.app/RPsaiEemhQrS6zCchywL4j/" + str(info) + '?sound=birdsong'
    if type == 4:
        api = "https://api.day.app/jczfKrq4ofQmkHmc6R7ZYm/" + str(info) + '?sound=birdsong'
    requests.post(api)


def get_info():
    api = 'http://t.weather.itboy.net/api/weather/city/'  # API地址，必须配合城市代码使用
    city_code = '101320101'  # 进入https://where.heweather.com/index.html查询你的城市代码
    tqurl = api + city_code
    response = requests.get(tqurl)
    d = response.json()
    return d


def main():
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    d1 = datetime.datetime(2022, 8, 16)
    # try:
    BarkPush("测试消息", 4)
    BarkPush(str(datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))),4)
    while True:
        time_struct = time.localtime()
        dateStr = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
        if dateStr.hour == 9 and dateStr.minute == 7 and dateStr.second == 0:
            BarkPush("定时测试", 4)
            time.sleep(1)
        if time_struct.tm_hour == 7 and time_struct.tm_min == 30 and time_struct.tm_sec == 0:
            print(time_struct)
            d2 = datetime.datetime(time_struct.tm_year, time_struct.tm_mon, time_struct.tm_mday)
            interval = d2 - d1
            d = get_info()  # 将数据以json形式返回，这个d就是返回的json数据
            if d['status'] == 200:  # 当返回状态码为200，输出天气状况
                parent = d["cityInfo"]["parent"]  # 省
                city = d["cityInfo"]["city"]  # 市
                update_time = d["time"]  # 更新时间
                date = d["data"]["forecast"][0]["ymd"]  # 日期
                week = d["data"]["forecast"][0]["week"]  # 星期
                weather_type = d["data"]["forecast"][0]["type"]  # 天气
                wendu_high = d["data"]["forecast"][0]["high"]  # 最高温度
                wendu_low = d["data"]["forecast"][0]["low"]  # 最低温度
                shidu = d["data"]["shidu"]  # 湿度
                pm25 = str(d["data"]["pm25"])  # PM2.5
                pm10 = str(d["data"]["pm10"])  # PM10
                quality = d["data"]["quality"]  # 天气质量
                fx = d["data"]["forecast"][0]["fx"]  # 风向
                fl = d["data"]["forecast"][0]["fl"]  # 风力
                ganmao = d["data"]["ganmao"]  # 感冒指数
                tips = d["data"]["forecast"][0]["notice"]  # 温馨提示
                # 天气提示内容
                morning_message = '今天是恋爱的第' + str(
                    interval.days) + '天\n' + '今日份的天气\n城市：' + parent + city + "\n日期： " + date + "\n星期: " + week + "\n天气: " + weather_type + "\n温度: " + wendu_high + '-' + wendu_low + "\n湿度: " + \
                                  shidu + "\nPM25: " + pm25 + "\nPM10: " + pm10 + "\n空气质量: " + quality + \
                                  "\n风力风向: " + fx + fl + "\n感冒指数: " + ganmao + "\n温馨提示： " + tips + "\n更新时间: " + update_time + "\n✁-----------------------------------------\n" + get_iciba_everyday()
                if time_struct.tm_mon == 10 and time_struct.tm_mday == 17:
                    BarkPush(morning_message, 1)
                elif time_struct.tm_mon == 4 and time_struct.tm_mday == 29:
                    BarkPush(morning_message, 2)
                else:
                    BarkPush(morning_message, 0)
                time.sleep(1)
        if time_struct.tm_hour == 23 and time_struct.tm_min == 30 and time_struct.tm_sec == 00:
            print(time_struct)
            evening_message = '不早了，还没睡要赶紧睡觉哦~亲亲宝贝（我也要亲亲'
            BarkPush(evening_message, 3)
            time.sleep(1)

    # except Exception:
    #     error = '【出现错误】\n　　今日天气推送错误，请检查服务或网络状态！'
    #     print(error)
    #     print(Exception)


if __name__ == '__main__':
    main()
