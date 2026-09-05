# 招聘AI助手（Recruit AI Assistant）

一个面向 HR/招聘者的本地化候选人管理 + AI 对话式指挥小应用。

## 功能特性

- **AI 助理（对话式指挥）**：用自然语言让 AI 完成候选人录入、查询、修改、生成沟通话术等操作（LLM 通过函数调用操作台账）
- **简历录入**：候选人/岗位/渠道等信息入库；支持上传 PDF/Word/TXT 文档自动解析提取文本
- **候选人台账**：候选人/岗位下拉选择、查重检测、更新状态（面试时间悬浮选择）、删除带确认
- **数据统计**：候选人总数、各岗位/渠道分布
- **多用户系统**：注册/登录 + 数据按用户隔离（每用户独立 Excel 台账）
- **模型切换**：前端可下拉切换 12 个 LLM 模型

## 技术栈

- 后端：FastAPI（端口 8010），Excel(openpyxl/pandas) 存储，PBKDF2 密码哈希，token 鉴权
- 前端：单页应用 app.py（端口 7860），代理转发后端 API
- 可选：AI 对话（openai SDK）、文档解析（pypdf / python-docx）

## 快速开始

```bash
# 1. 安装依赖
pip install fastapi uvicorn pandas openpyxl python-dotenv requests openai pypdf python-docx

# 2. 配置 .env（参考 .env.example）
#    LLM_BASE_URL / LLM_API_KEY / LLM_MODEL

# 3. 启动后端（8010）
python recruit_ai_qwen38.py

# 4. 启动前端（7860）
python app.py

# 或一键启动（自动起前后端 + 打开浏览器）
python launcher.py
```

访问 http://127.0.0.1:7860 ，默认管理员账号 `admin` / `123456`。

## 目录结构

```
recruit_ai/
├── recruit_ai_qwen38.py   # FastAPI 后端（用户系统/CRUD/AI Agent/文件解析）
├── app.py                 # 单页前端（登录/录入/台账/统计/AI 对话）
├── launcher.py            # 一键启动器（也是打包 exe 入口）
├── 招聘AI助手_最新.spec     # PyInstaller 打包配置
├── .env.example           # 环境变量模板（.env 不入库）
└── data/                  # 运行期生成：每用户台账 + users.json（不入库）
```

## 打包为 exe

```bash
pip install pyinstaller
pyinstaller 招聘AI助手_最新.spec --noconfirm
# 产物在 dist/招聘AI助手/，把 .env、data/ 放到 exe 同目录即可
```

## 说明

- `.env`、`data/`（用户台账与账号）、`dist/`、`build/` 均为运行期/构建产物，不入库，请勿提交。
- 项目为本地单机部署设计，数据保存在本机 `data/` 目录。
