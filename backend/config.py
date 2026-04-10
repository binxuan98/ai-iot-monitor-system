import os


# 项目路径配置，统一管理文件位置，便于教学演示和二次开发
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_PATH = os.environ.get("DATABASE_PATH", os.path.join(DATA_DIR, "monitor.db"))
SENSOR_JSON_PATH = os.path.join(DATA_DIR, "sensor_data.json")
SENSOR_CSV_PATH = os.path.join(DATA_DIR, "sensor_data.csv")

# 会话密钥（教学场景使用，生产环境请改为环境变量）
SECRET_KEY = "smart-env-monitor-teaching-secret-key"

# 异常阈值配置，学生可在此基础上扩展不同场景策略
THRESHOLDS = {
    "temperature": {"min": 0, "max": 35},
    "humidity": {"min": 20, "max": 80},
    "pm25": {"min": 0, "max": 75},
    "light": {"min": 100, "max": 1200},
    "co2": {"min": 350, "max": 1000},
}
