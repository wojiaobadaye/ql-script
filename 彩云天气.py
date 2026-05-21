# @author Sten
# 作者仓库:https://github.com/aefa6/QinglongScript.git
# 觉得不错麻烦点个star谢谢

import json

import notify
import requests

# 填写下面的信息，经纬度请自行百度，使用青龙自带的推送
# key = "qAbLkhTG46uP3J8A"
lon = "121.3912"
lat = "31.2513"

# 下面的不用管了
api_url = f"https://api.caiyunapp.com/v2.6/{key}/{lon},{lat}/weather?alert=true&realtime&minutely"
response = requests.get(api_url)
print("状态码:", response.status_code)
print("响应内容:", repr(response.text))
data = json.loads(response.text)
weather = data["result"]

# 1. 安全获取 alert 对象，如果没有则返回空字典 {}
alert_data = weather.get("alert", {})
# 2. 安全获取 content 列表，如果没有则返回空列表 []
content_list = alert_data.get("content", [])
if content_list:
    tip = content_list[0]["description"]
else:
    tip = ""

info = f"""
实时天气:  
天气现象:{weather["realtime"]["skycon"]}    
温度:{weather["realtime"]["temperature"]}°C     
体感温度:{weather["realtime"]["apparent_temperature"]}°C    
湿度:{weather["realtime"]["humidity"]}      
能见度:{weather["realtime"]["visibility"]}KM    
紫外线强度:{weather["realtime"]["life_index"]["ultraviolet"]["desc"]}   
空气质量:{weather["realtime"]["air_quality"]["description"]["chn"]}     
总体感觉:{weather["realtime"]["life_index"]["comfort"]["desc"]}     
    
全天:
温度:{weather["daily"]["temperature"][0]["min"]} - {weather["daily"]["temperature"][0]["max"]}°C, 白天温度:{weather["daily"]["temperature_08h_20h"][0]["min"]} - {weather["daily"]["temperature_08h_20h"][0]["max"]}°C, 夜间温度:{weather["daily"]["temperature_20h_32h"][0]["min"]} - {weather["daily"]["temperature_20h_32h"][0]["max"]}°C    
紫外线强度{weather["daily"]["life_index"]["ultraviolet"][0]["desc"]},总体感觉{weather["daily"]["life_index"]["comfort"][0]["desc"]}      
    
预测:{weather["minutely"]["description"]},{weather["hourly"]["description"]}    
{tip}
"""

print(info)
notify.send("彩云天气", info)
