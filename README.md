# Pip 源切换器
## 描述

Pip 源切换器是一个使用 Python 和 Tkinter 图形库开发的图形用户界面（GUI）工具。它允许用户轻松地在多个 PyPI 镜像源之间进行临时或永久的切换，从而优化 Python 包的安装速度。

## 功能特点

- **展示可用的 PyPI 镜像源**：应用程序会列出一系列常用的 PyPI 镜像源，并允许用户查看它们的 URL。
- **临时切换源**：用户可以选择一个镜像源并临时切换 pip 的源，这将影响当前终端会话中的所有 pip 命令。
- **永久切换源**：用户可以选择一个镜像源并将其设置为 pip 的默认源，这将永久更改用户的 pip 配置文件。
- **自动选择最佳源**：应用程序可以自动检测并选择最快的 PyPI 镜像源。

## 环境要求

- Python 3.6 或更高版本
- Tkinter 库（通常随 Python 一同安装）
- `requests` 库（可通过 `pip install requests` 安装）

## 快速开始

### 安装依赖

确保你的环境中已经安装了 `requests` 库。如果没有安装，可以通过以下命令进行安装：

```bash
#将本项目克隆到本地或下载源代码，并运行主 Python 脚本
pip install requests
python main.py
