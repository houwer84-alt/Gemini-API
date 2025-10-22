# 🚀 快速开始 - 本地开发

## 一键设置（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/HanaokaYuzu/Gemini-API.git
cd Gemini-API

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装开发环境（使用 Makefile）
make dev-install

# 4. 验证安装
make verify

# 5. 运行示例测试
make dev-test
```

## 手动设置

如果你的系统不支持 `make`：

```bash
# 1. 克隆并进入项目
git clone https://github.com/HanaokaYuzu/Gemini-API.git
cd Gemini-API

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -e .
pip install black flake8 pytest pytest-asyncio mypy
pip install browser-cookie3

# 4. 验证安装
python test_installation.py

# 5. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入你的 cookies
```

## 获取 Cookies

### 方法 1: 使用 browser-cookie3（推荐）

安装 `browser-cookie3` 后，只需在浏览器登录 https://gemini.google.com，代码会自动读取。

### 方法 2: 手动获取

1. 访问 https://gemini.google.com 并登录
2. 按 `F12` 打开开发者工具
3. 切换到 `Application` 标签（Chrome）或 `Storage` 标签（Firefox）
4. 在左侧找到 `Cookies` → `https://gemini.google.com`
5. 复制以下两个 Cookie 的值：
   - `__Secure-1PSID`
   - `__Secure-1PSIDTS`
6. 在 `.env` 文件中设置：

```bash
SECURE_1PSID=你的__Secure-1PSID值
SECURE_1PSIDTS=你的__Secure-1PSIDTS值
```

## 开发工作流

### 1. 日常开发

```bash
# 修改代码...

# 格式化代码
make format

# 代码检查
make lint

# 运行测试
make test

# 或一次性运行所有检查
make all
```

### 2. 添加新功能

```bash
# 1. 创建功能分支
git checkout -b feature/my-new-feature

# 2. 编写代码（参考 DEVELOPMENT.md）
# 3. 编写测试（在 tests/ 目录）
# 4. 运行测试
make test

# 5. 提交代码
git add .
git commit -m "feat: add my new feature"
git push origin feature/my-new-feature
```

### 3. 测试你的修改

创建测试文件 `my_test.py`:

```python
import asyncio
import os
from gemini_webapi import GeminiClient

async def main():
    # 使用环境变量
    client = GeminiClient(
        os.getenv("SECURE_1PSID"),
        os.getenv("SECURE_1PSIDTS")
    )
    
    # 或自动读取浏览器 cookies
    # client = GeminiClient()
    
    await client.init()
    
    # 测试你的修改
    response = await client.generate_content("Hello!")
    print(response.text)
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

运行：

```bash
python my_test.py
```

## 常用命令

```bash
make help           # 查看所有可用命令
make install        # 安装项目依赖
make dev-install    # 安装开发依赖
make test           # 运行测试
make format         # 格式化代码
make lint           # 代码检查
make clean          # 清理临时文件
make build          # 构建包
make verify         # 验证安装
```

## 项目结构速览

```
src/gemini_webapi/
├── client.py          # 主客户端类 ⭐
├── constants.py       # 常量定义（端点、模型）
├── exceptions.py      # 异常类
├── components/        # 组件（Gem 功能等）
├── types/            # 数据类型定义
└── utils/            # 工具函数
```

**核心文件说明**：
- `client.py`: 实现 `GeminiClient` 和 `ChatSession`，大部分修改会在这里
- `constants.py`: 定义 API 端点和模型配置
- `types/`: 定义数据结构（如 `ModelOutput`, `Gem` 等）

## 开发提示

### 调试技巧

```python
# 1. 启用详细日志
from gemini_webapi import set_log_level
set_log_level("DEBUG")

# 2. 查看原始响应
# 在 client.py 中添加：
print(response.text)  # 查看原始响应

# 3. 使用断点
breakpoint()  # 在需要调试的地方添加
```

### 常见问题

**Q: 为什么测试失败？**
- 检查是否正确设置了 cookies
- 确保网络连接正常
- 查看是否有 Google 区域限制

**Q: 如何更新依赖？**
```bash
pip install -U httpx loguru orjson pydantic
```

**Q: 如何抓包分析 API？**
1. Chrome DevTools → Network
2. 过滤 XHR/Fetch 请求
3. 查看 `StreamGenerate` 等请求
4. 分析请求头和请求体

## 下一步

1. 📖 阅读 [DEVELOPMENT.md](DEVELOPMENT.md) 了解详细开发指南
2. 📝 查看 [README.md](README.md) 了解使用方法
3. 🧪 查看 `tests/` 目录学习测试编写
4. 💡 查看 GitHub Issues 了解待实现功能

## 需要帮助？

- 📚 文档：[README.md](README.md) 和 [DEVELOPMENT.md](DEVELOPMENT.md)
- 🐛 报告问题：https://github.com/HanaokaYuzu/Gemini-API/issues
- 💬 讨论：GitHub Discussions

---

**祝你开发愉快！** 🎉
