# 智慧环境监测与异常预警平台

Smart IoT Environment Monitoring & Alert Platform（教学版）

本项目面向高职院校《人工智能应用开发（物联网方向）》课程，模拟企业常见的 AI+IoT 应用开发流程，覆盖数据采集、异常检测、可视化、日志管理、角色协作与项目交付全过程。

## 1. 项目简介（发给学生）

你将参与开发一个可运行的智慧环境监测平台。系统从本地 JSON/CSV 模拟传感器数据中读取温度、湿度、PM2.5、光照、CO2 等指标，完成：

- 数据展示与定时刷新
- 阈值异常检测与告警记录
- 规则评分的智能分析
- 图表可视化（折线图、柱状图、仪表盘）
- 用户登录/退出
- 系统日志追踪

项目采用前后端相对独立架构，便于分组协作和岗位化实践。

## 2. 技术栈

- 后端：Python + Flask + Flask-Cors
- 数据处理：Pandas
- 数据库存储：SQLite
- 前端：HTML + CSS + JavaScript
- 图表：ECharts

## 3. 项目目录结构

```text
ai-iot-monitor-system/
├── backend/
│   ├── __init__.py
│   ├── analysis.py
│   ├── app.py
│   ├── config.py
│   ├── data_loader.py
│   └── database.py
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── api.js
│   │   └── app.js
│   └── index.html
├── data/
│   ├── init.sql
│   ├── sensor_data.csv
│   └── sensor_data.json
├── docs/
│   ├── API_DOC.md
│   ├── PROJECT_OVERVIEW.md
│   └── STUDENT_TASKS.md
├── scripts/
│   ├── init_db.py
│   ├── run_backend.py
│   └── run_frontend.py
├── tests/
│   └── test_api.py
├── requirements.txt
└── README.md
```

## 4. 快速启动（Windows/Mac/Linux 通用）

### 4.1 安装依赖

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### 4.2 启动后端

```bash
python scripts/run_backend.py
```

后端默认地址：`http://127.0.0.1:5000`

### 4.3 启动前端

新开终端：

```bash
python scripts/run_frontend.py
```

前端访问地址：`http://127.0.0.1:5500`

### 4.4 登录账号

- 管理员：`admin / admin123`
- 学生：`student / student123`

## 5. 核心功能说明

1. 用户登录与退出  
2. 最新环境数据展示  
3. 历史数据查询与图表可视化  
4. JSON/CSV 模拟数据加载  
5. 阈值异常检测与告警记录  
6. 简单评分机制的智能分析  
7. 系统日志记录关键行为  
8. 手动刷新 + 前端定时刷新

## 6. RESTful API 一览

- `POST /api/login`
- `POST /api/logout`
- `GET /api/sensors/latest`
- `GET /api/sensors/history`
- `GET /api/alerts`
- `GET /api/analysis`
- `GET /api/logs`
- `POST /api/refresh`

接口详情见 [docs/API_DOC.md](./docs/API_DOC.md)

## 7. 教学岗位分工建议（6 角色）

### 7.1 项目经理

- 拆分迭代任务与看板维护
- 组织站会与里程碑验收
- 管控分支策略与合并流程

### 7.2 前端开发工程师

- 登录页面与仪表盘交互
- 图表展示与告警/日志表格
- API 联调与页面状态管理

### 7.3 后端开发工程师

- Flask API 设计与实现
- SQLite 模型与数据读写
- 日志与异常处理机制完善

### 7.4 算法工程师

- 阈值规则优化与场景化参数
- 环境评分机制迭代
- 分析文案策略优化

### 7.5 测试工程师

- 接口测试与功能回归
- 构建测试数据与报告
- 常见错误复现与缺陷跟踪

### 7.6 运维/文档工程师

- 部署脚本和运行环境检查
- README、接口文档、版本记录
- 项目演示环境准备

更多任务分解见 [docs/STUDENT_TASKS.md](./docs/STUDENT_TASKS.md)

## 8. GitHub 协作规范

### 分支模型

- `main`：稳定可发布版本（教师验收基线）
- `develop`：日常集成分支
- `feature/*`：功能开发分支（按角色或模块命名）

### 分支命名建议

- `feature/frontend-dashboard`
- `feature/backend-alert-api`
- `feature/algo-score-rule`
- `fix/login-session-bug`

### Commit Message 规范（建议）

```text
feat: 新增告警历史查询接口
fix: 修复前端图表时间轴错位问题
test: 增加登录接口自动化测试
docs: 更新接口文档和部署步骤
refactor: 重构数据加载模块
```

### Pull Request 说明模板

1. 本次变更内容
2. 影响模块
3. 测试截图/测试结果
4. 是否存在已知问题
5. 关联任务编号

### 冲突避免建议

- 每天先拉取 `develop` 再开发
- 同一文件提前认领
- 小步提交，及时发起 PR
- 禁止直接推送 `main`

### 教师验收建议

- 能否完整启动与登录
- API 是否按文档可调用
- 核心功能是否通过
- PR 质量与提交规范是否达标

## 9. 学生提交规范

- 分支：禁止在 `main` 直接开发
- 提交：每次只做一件事，描述清晰
- PR：至少 1 名同学 Review 后合并
- 测试：提交前运行 `python -m unittest discover -s tests -p "test_*.py"`

## 10. 二次开发扩展任务（至少 10 项）

1. 支持角色权限控制（管理员/普通用户）
2. 增加告警确认与处理状态
3. 增加告警短信/邮件模拟通知
4. 接入真实串口或 MQTT 数据源
5. 增加多监测点位切换
6. 增加数据导出（CSV/Excel）
7. 实现阈值在线配置页面
8. 引入简单时间序列预测（滑动平均）
9. 增加暗色主题与移动端适配
10. 增加 Docker 部署支持
11. 增加异常检测准确率评估页面
12. 增加前端权限路由与菜单管理

## 11. 项目实施顺序（建议课堂节奏）

1. 环境准备与项目结构创建
2. 后端基础 API 完成
3. 前端静态页与登录流程
4. 前后端联调
5. 异常检测与分析优化
6. 测试与缺陷修复
7. 文档完善与演示答辩

## 12. 常见报错与排查

1. `ModuleNotFoundError: No module named 'backend'`  
   - 在项目根目录执行命令，避免路径错误。

2. 前端调用 API 跨域失败  
   - 确认后端已启动，且 `Flask-Cors` 已安装。

3. 登录失败  
   - 检查账号密码是否为 `admin/admin123` 或 `student/student123`。

4. 页面图表不显示  
   - 检查网络是否可访问 ECharts CDN。

5. SQLite 文件无法写入  
   - 确认 `data/` 目录有写权限。

## 13. 测试命令

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

如用于课程教学，建议教师按“需求讲解 → 分组开发 → 代码评审 → 课堂答辩”的流程组织项目化实践。
