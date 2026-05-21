import json
import os

import requests

# 通过青龙环境变量配置，或直接修改下方默认值
KEY = os.environ.get("CAIYUN_KEY", "")
LON = os.environ.get("CAIYUN_LON", "")
LAT = os.environ.get("CAIYUN_LAT", "")

# 综合接口：包含实况、 hourly、 daily、 alert
api_url = (
    f"https://api.caiyunapp.com/v2.6/{KEY}/{LON},{LAT}/weather"
    "?dailysteps=3&hourlysteps=48&alert=true"
)

resp = requests.get(api_url, timeout=15)
resp.raise_for_status()
data = resp.json()

if data.get("status") != "ok":
    print("API 返回异常:", json.dumps(data, ensure_ascii=False, indent=2))
    raise SystemExit(1)

weather = data["result"]
realtime = weather["realtime"]

# 预警
alert_content = weather.get("alert", {}).get("content", [])
tip = alert_content[0]["description"] if alert_content else ""

# 全天预报（取第1天）
daily = weather["daily"]
day0 = daily["temperature"][0]
day0_08h_20h = daily["temperature_08h_20h"][0]
day0_20h_32h = daily["temperature_20h_32h"][0]

info = f"""
实时天气:
天气现象:{realtime['skycon']}
温度:{realtime['temperature']}°C
体感温度:{realtime['apparent_temperature']}°C
湿度:{realtime['humidity']}
能见度:{realtime['visibility']}KM
紫外线强度:{realtime['life_index']['ultraviolet']['desc']}
空气质量:{realtime['air_quality']['description']['chn']}
总体感觉:{realtime['life_index']['comfort']['desc']}

全天:
温度:{day0['min']} - {day0['max']}°C
白天温度:{day0_08h_20h['min']} - {day0_08h_20h['max']}°C
夜间温度:{day0_20h_32h['min']} - {day0_20h_32h['max']}°C
紫外线强度:{daily['life_index']['ultraviolet'][0]['desc']}
总体感觉:{daily['life_index']['comfort'][0]['desc']}

预测:{weather['hourly']['description']}
{tip}
"""

print(info)

try:
    from notify import send as send_notify
    send_notify("彩云天气", info)
except ImportError:
    print("未找到 notify 模块，跳过推送")
