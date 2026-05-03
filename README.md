# 💬 智谱 AI 聊天助手 (GLM-4)

这是一个基于 Python 和智谱 AI (GLM-4) 开发的本地命令行聊天机器人。它支持多轮对话记忆、历史记录本地持久化存储以及基础的错误处理，旨在提供一个轻量级、可定制的交互式 AI 对话体验。

## ✨ 功能特性

*   **🧠 多轮对话管理**：自动维护对话上下文（`conversation_history`），使 AI 具备记忆能力，回答更连贯。
*   **💾 历史记录持久化**：采用 JSON 文件存储对话记录，即使关闭程序，下次启动也能恢复历史对话。
*   **⚙️ 灵活的 API 调用**：基于 `ZhipuAI` SDK 调用最新的 `glm-4-flash` 模型，支持调节 `temperature` 和 `max_tokens`。
*   **🛡️ 健壮的错误处理**：
    *   捕获 API 调用异常，防止程序崩溃。
    *   自动处理 JSON 文件读写错误。
    *   输入校验（禁止空输入）。
*   **📜 交互式命令行界面**：内置 Help 菜单，支持查看历史、清空记录等快捷指令。

## 🛠️ 技术栈

*   **Python 3.8+**
*   **ZhipuAI Python SDK**
*   **JSON** (数据存储)

## 🚀 快速开始

### 1. 环境准备
请确保你已经安装了 Python 和 `pip`。

### 2. 克隆项目
bash

git clone https://github.com/
[Myan-L]/[glm-chatbot].git

cd [glm-chatbot]

### 3. 安装依赖
bash

pip install zhipuai

### 4. 配置 API Key (!!!!!!!!!!)
**安全警告**：为了安全，请不要将 API Key 硬编码在代码中。
建议直接在代码中替换，或者在环境变量中设置。
如果你选择直接修改，请打开 `main.py`，填入你的 Key：
example:
api_key = "在此处填入你的ZhipuAI_API_Key"

### 5. 运行程序
bash

python main.py
根据提示输入你的昵称，即可开始聊天！

## 📖 使用指南

在聊天界面中，你可以使用以下命令：

| 命令 | 功能 |
| :--- | :--- |
| `help` | 显示帮助菜单 |
| `history` | 查看最近 5 条对话历史 |
| `clear` | 清空当前对话历史 |
| `quit` | 退出程序 |

## 📂 项目结构
.

├── main.py          # 主程序入口及 ChatAssistant 类实现

├── README.md        # 项目说明文档

└── *.json           # 自动生成的对话历史文件 (例如: default_user_history.json)

## 🔮 未来计划
*   [ ] 引入 `.env` 文件管理 API Key，增强安全性。
*   [ ] 增加 Streamlit 前端，打造 Web UI。
*   [ ] 支持切换不同的大模型（如 DeepSeek, OpenAI）。

## 📄 License
MIT