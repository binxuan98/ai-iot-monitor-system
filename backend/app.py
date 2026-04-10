from flask import Flask, jsonify, request, session
from flask_cors import CORS

from backend.analysis import evaluate_alerts, score_environment
from backend.config import SECRET_KEY
from backend.data_loader import load_sensor_data_from_csv, load_sensor_data_from_json
from backend.database import (
    add_log,
    fetch_alerts,
    fetch_latest_sensor,
    fetch_logs,
    fetch_sensor_history,
    get_connection,
    init_db,
    insert_sensor_batch,
    save_alert,
)


app = Flask(__name__)
app.secret_key = SECRET_KEY
CORS(app, supports_credentials=True)


def bootstrap_data() -> None:
    # 启动时若数据库没有传感器数据，则自动导入 JSON/CSV 示例数据
    latest = fetch_latest_sensor()
    if latest:
        return
    records = load_sensor_data_from_json()
    if not records:
        records = load_sensor_data_from_csv()
    if records:
        insert_sensor_batch(records)
        add_log("数据初始化", f"已导入 {len(records)} 条模拟传感器数据")


def current_user():
    # 获取当前登录用户，未登录时返回空
    return session.get("user")


@app.route("/api/login", methods=["POST"])
def login():
    # 用户登录接口：教学场景使用明文密码，便于学生先理解流程
    payload = request.get_json() or {}
    username = payload.get("username", "").strip()
    password = payload.get("password", "").strip()
    if not username or not password:
        return jsonify({"success": False, "message": "用户名和密码不能为空"}), 400

    conn = get_connection()
    row = conn.execute(
        "SELECT username, role FROM users WHERE username = ? AND password = ?;",
        (username, password),
    ).fetchone()
    conn.close()

    if not row:
        add_log("登录失败", f"用户 {username} 登录失败")
        return jsonify({"success": False, "message": "用户名或密码错误"}), 401

    user_info = {"username": row["username"], "role": row["role"]}
    session["user"] = user_info
    add_log("登录成功", f"用户 {username} 登录系统")
    return jsonify({"success": True, "message": "登录成功", "data": user_info})


@app.route("/api/logout", methods=["POST"])
def logout():
    # 用户退出接口：清理会话并记录日志
    user = current_user()
    if user:
        add_log("退出登录", f"用户 {user['username']} 退出系统")
    session.clear()
    return jsonify({"success": True, "message": "已退出登录"})


@app.route("/api/sensors/latest", methods=["GET"])
def get_latest_sensor():
    # 返回最新环境数据，并在每次请求时执行一次异常检测
    sensor = fetch_latest_sensor()
    if not sensor:
        return jsonify({"success": False, "message": "暂无环境数据"}), 404

    alerts = evaluate_alerts(sensor)
    for alert in alerts:
        save_alert(alert["level"], alert["metric"], alert["value"], alert["message"])

    return jsonify({"success": True, "data": sensor, "alerts": alerts})


@app.route("/api/sensors/history", methods=["GET"])
def get_sensor_history():
    # 返回历史数据，默认 50 条，可用于折线图/柱状图
    limit = request.args.get("limit", default=50, type=int)
    data = fetch_sensor_history(limit=max(1, min(limit, 500)))
    return jsonify({"success": True, "data": data})


@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    # 返回告警历史记录
    limit = request.args.get("limit", default=100, type=int)
    data = fetch_alerts(limit=max(1, min(limit, 500)))
    return jsonify({"success": True, "data": data})


@app.route("/api/analysis", methods=["GET"])
def get_analysis():
    # 对当前环境进行评分并生成状态说明
    sensor = fetch_latest_sensor()
    if not sensor:
        return jsonify({"success": False, "message": "暂无环境数据"}), 404
    result = score_environment(sensor)
    add_log("智能分析", f"环境评分 {result['score']}，状态：{result['status']}")
    return jsonify({"success": True, "data": result})


@app.route("/api/logs", methods=["GET"])
def get_logs():
    # 返回系统日志供教学观察系统行为
    limit = request.args.get("limit", default=100, type=int)
    data = fetch_logs(limit=max(1, min(limit, 500)))
    return jsonify({"success": True, "data": data})


@app.route("/api/refresh", methods=["POST"])
def refresh_data():
    # 模拟“定时刷新”：从 CSV 追加一条数据作为最新值
    csv_records = load_sensor_data_from_csv()
    if not csv_records:
        return jsonify({"success": False, "message": "未找到可用的 CSV 数据"}), 404
    latest_record = csv_records[-1]
    insert_sensor_batch([latest_record])
    add_log("数据刷新", "通过 /api/refresh 追加 1 条模拟数据")
    return jsonify({"success": True, "message": "数据刷新成功", "data": latest_record})


def create_app():
    # 工厂函数，方便测试与脚本调用
    init_db()
    bootstrap_data()
    return app


if __name__ == "__main__":
    create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
