from typing import Dict, List

from backend.config import THRESHOLDS


def evaluate_alerts(sensor: Dict) -> List[Dict]:
    # 基于阈值规则检测异常，并返回告警详情
    alerts = []
    for metric, rule in THRESHOLDS.items():
        value = sensor.get(metric, 0)
        if value < rule["min"] or value > rule["max"]:
            level = "高危" if value > rule["max"] * 1.2 or value < rule["min"] * 0.8 else "一般"
            alerts.append(
                {
                    "level": level,
                    "metric": metric,
                    "value": value,
                    "message": f"{metric} 当前值 {value} 超出阈值区间 [{rule['min']}, {rule['max']}]",
                }
            )
    return alerts


def score_environment(sensor: Dict) -> Dict:
    # 简单评分机制：每项扣分并生成环境状态说明
    score = 100
    deduction_detail = []

    for metric, rule in THRESHOLDS.items():
        value = sensor.get(metric, 0)
        if rule["min"] <= value <= rule["max"]:
            continue
        if value > rule["max"]:
            delta = value - rule["max"]
        else:
            delta = rule["min"] - value
        penalty = min(25, int(delta / max(1, (rule["max"] - rule["min"]) * 0.1)) + 5)
        score -= penalty
        deduction_detail.append(f"{metric} 偏离阈值，扣分 {penalty}")

    score = max(0, score)
    if score >= 85:
        status = "环境状态良好"
    elif score >= 60:
        status = "环境状态一般，建议关注"
    else:
        status = "环境状态较差，请立即处理异常"

    return {
        "score": score,
        "status": status,
        "detail": "；".join(deduction_detail) if deduction_detail else "各项指标正常",
    }
