# 接口文档

接口基地址：`http://127.0.0.1:5000`

## 1. 登录

- 方法：`POST`
- 路径：`/api/login`
- 请求体：

```json
{
  "username": "admin",
  "password": "admin123"
}
```

## 2. 退出

- 方法：`POST`
- 路径：`/api/logout`

## 3. 最新传感器数据

- 方法：`GET`
- 路径：`/api/sensors/latest`

## 4. 历史传感器数据

- 方法：`GET`
- 路径：`/api/sensors/history?limit=50`

## 5. 告警记录

- 方法：`GET`
- 路径：`/api/alerts?limit=100`

## 6. 智能分析

- 方法：`GET`
- 路径：`/api/analysis`

## 7. 系统日志

- 方法：`GET`
- 路径：`/api/logs?limit=100`

## 8. 手动刷新数据

- 方法：`POST`
- 路径：`/api/refresh`
