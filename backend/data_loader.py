import json
import os
from datetime import datetime, timedelta
from typing import Dict, List

import pandas as pd

from backend.config import SENSOR_JSON_PATH, SENSOR_CSV_PATH


def normalize_records(records: List[Dict]) -> List[Dict]:
    # 统一字段格式并补充时间戳，保证后续写库逻辑一致
    normalized = []
    base_time = datetime.now() - timedelta(minutes=len(records))
    for index, row in enumerate(records):
        timestamp = row.get("timestamp")
        if not timestamp:
            timestamp = (base_time + timedelta(minutes=index)).isoformat(timespec="seconds")
        normalized.append(
            {
                "timestamp": timestamp,
                "temperature": float(row.get("temperature", 0)),
                "humidity": float(row.get("humidity", 0)),
                "pm25": float(row.get("pm25", 0)),
                "light": float(row.get("light", 0)),
                "co2": float(row.get("co2", 0)),
            }
        )
    return normalized


def load_sensor_data_from_json() -> List[Dict]:
    # 从 JSON 文件读取模拟传感器数据
    if not os.path.exists(SENSOR_JSON_PATH):
        return []
    with open(SENSOR_JSON_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)
    return normalize_records(data)


def load_sensor_data_from_csv() -> List[Dict]:
    # 从 CSV 文件读取模拟传感器数据
    if not os.path.exists(SENSOR_CSV_PATH):
        return []
    dataframe = pd.read_csv(SENSOR_CSV_PATH)
    records = dataframe.to_dict(orient="records")
    return normalize_records(records)
