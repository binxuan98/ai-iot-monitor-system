import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional

from backend.config import DATABASE_PATH


def get_connection() -> sqlite3.Connection:
    # 创建数据库连接，并启用按列名访问
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    # 初始化数据库表结构，便于首次部署快速运行
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            pm25 REAL NOT NULL,
            light REAL NOT NULL,
            co2 REAL NOT NULL
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            level TEXT NOT NULL,
            metric TEXT NOT NULL,
            value REAL NOT NULL,
            message TEXT NOT NULL
        );
        """
    )
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            detail TEXT NOT NULL
        );
        """
    )

    cursor.execute("SELECT COUNT(*) AS total FROM users;")
    if cursor.fetchone()["total"] == 0:
        cursor.executemany(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?);",
            [
                ("admin", "admin123", "管理员"),
                ("student", "student123", "学生"),
            ],
        )

    conn.commit()
    conn.close()


def add_log(event_type: str, detail: str) -> None:
    # 记录关键操作日志，便于教学中的追踪与排障
    conn = get_connection()
    conn.execute(
        "INSERT INTO system_logs (timestamp, event_type, detail) VALUES (?, ?, ?);",
        (datetime.now().isoformat(timespec="seconds"), event_type, detail),
    )
    conn.commit()
    conn.close()


def insert_sensor_batch(records: List[Dict[str, Any]]) -> None:
    # 批量写入传感器数据，支持从 JSON/CSV 文件导入
    conn = get_connection()
    conn.executemany(
        """
        INSERT INTO sensor_data (timestamp, temperature, humidity, pm25, light, co2)
        VALUES (:timestamp, :temperature, :humidity, :pm25, :light, :co2);
        """,
        records,
    )
    conn.commit()
    conn.close()


def fetch_latest_sensor() -> Optional[Dict[str, Any]]:
    # 获取最新一条环境数据用于主面板显示
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1;"
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def fetch_sensor_history(limit: int = 50) -> List[Dict[str, Any]]:
    # 获取历史数据并按时间升序返回，便于图表绘制
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT ?;", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in reversed(rows)]


def save_alert(level: str, metric: str, value: float, message: str) -> None:
    # 存储异常告警记录，供告警页面展示
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO alerts (timestamp, level, metric, value, message)
        VALUES (?, ?, ?, ?, ?);
        """,
        (datetime.now().isoformat(timespec="seconds"), level, metric, value, message),
    )
    conn.commit()
    conn.close()


def fetch_alerts(limit: int = 100) -> List[Dict[str, Any]]:
    # 获取告警列表，默认返回最近 100 条
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?;", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def fetch_logs(limit: int = 100) -> List[Dict[str, Any]]:
    # 获取系统日志，帮助学生理解系统关键行为
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM system_logs ORDER BY timestamp DESC LIMIT ?;", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
