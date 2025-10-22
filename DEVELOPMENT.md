# 🛠️ Gemini WebAPI 开发指南

## 项目结构说明

```
Gemini-API/
├── src/gemini_webapi/          # 主要源代码
│   ├── __init__.py             # 包入口，导出公共API
│   ├── client.py               # GeminiClient 和 ChatSession 核心类
│   ├── constants.py            # 常量定义（端点、模型、错误码等）
│   ├── exceptions.py           # 自定义异常类
│   │
│   ├── components/             # 组件模块
│   │   └── gem_mixin.py       # Gem 功能混入类
│   │
│   ├── types/                  # 类型定义
│   │   ├── __init__.py
│   │   ├── candidate.py       # Candidate 类型
│   │   ├── gem.py             # Gem 和 GemJar 类型
│   │   ├── grpc.py            # gRPC 相关类型
│   │   ├── image.py           # Image, WebImage, GeneratedImage
│   │   └── modeloutput.py     # ModelOutput 类型
│   │
│   └── utils/                  # 工具函数
│       ├── __init__.py
│       ├── decorators.py      # 装饰器（如 @running）
│       ├── get_access_token.py
│       ├── load_browser_cookies.py
│       ├── logger.py
│       ├── rotate_1psidts.py
│       └── upload_file.py
│
├── tests/                      # 测试文件
│   ├── test_client_features.py
│   ├── test_gem_mixin.py
│   └── test_save_image.py
│
├── assets/                     # 资源文件
│   ├── banner.png
│   ├── favicon.png
│   ├── logo.svg
│   └── sample.pdf
│
├── pyproject.toml             # 项目配置
├── README.md                  # 项目说明
├── LICENSE                    # AGPL-3.0 许可证
└── .gitignore                 # Git 忽略文件
```

---

## 开发环境设置

### 1. 安装开发依赖

```bash
# 以可编辑模式安装
pip install -e .

# 安装开发工具
pip install black flake8 pytest pytest-asyncio mypy

# 可选：浏览器 cookie 支持
pip install browser-cookie3
```

### 2. 代码风格

项目使用 **black** 代码格式化工具：

```bash
# 格式化代码
black src/ tests/

# 检查但不修改
black --check src/ tests/

# 检查代码质量
flake8 src/ tests/
```

### 3. 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_client_features.py

# 显示详细输出
pytest -v tests/

# 显示打印输出
pytest -s tests/
```

---

## 二次开发指南

### 添加新功能

#### 1. 添加新的 API 端点

编辑 `src/gemini_webapi/constants.py`:

```python
class Endpoint(StrEnum):
    GOOGLE = "https://www.google.com"
    GENERATE = "https://gemini.google.com/_/BardChatUi/data/..."
    # 添加新端点
    YOUR_NEW_ENDPOINT = "https://gemini.google.com/your/new/endpoint"
```

#### 2. 添加新的模型

编辑 `src/gemini_webapi/constants.py`:

```python
class Model(Enum):
    # 现有模型...
    YOUR_NEW_MODEL = (
        "model-name",
        {"x-goog-ext-525001261-jspb": '[your,header,data]'},
        False  # 是否需要高级账号
    )
```

#### 3. 添加新的方法到 GeminiClient

编辑 `src/gemini_webapi/client.py`:

```python
class GeminiClient(GemMixin):
    @running(retry=2)  # 使用装饰器添加重试和运行状态检查
    async def your_new_method(self, param1: str, **kwargs) -> YourReturnType:
        """
        你的新方法说明
        
        Parameters
        ----------
        param1: `str`
            参数说明
            
        Returns
        -------
        :class:`YourReturnType`
            返回值说明
        """
        # 实现你的逻辑
        response = await self.client.post(
            Endpoint.YOUR_NEW_ENDPOINT.value,
            data={...},
            **kwargs
        )
        
        # 处理响应
        return parsed_response
```

#### 4. 添加新的数据类型

在 `src/gemini_webapi/types/` 目录下创建新文件：

```python
# src/gemini_webapi/types/your_type.py
from pydantic import BaseModel

class YourNewType(BaseModel):
    """你的新类型说明"""
    
    field1: str
    field2: int
    optional_field: str | None = None
    
    def __str__(self):
        return f"YourNewType(field1='{self.field1}')"
```

然后在 `src/gemini_webapi/types/__init__.py` 中导出：

```python
from .your_type import YourNewType

__all__ = [
    # ... 现有导出
    "YourNewType",
]
```

#### 5. 添加新的异常类型

编辑 `src/gemini_webapi/exceptions.py`:

```python
class YourNewException(GeminiError):
    """
    你的新异常说明
    """
    pass
```

---

## 调试技巧

### 1. 启用详细日志

```python
from gemini_webapi import set_log_level

set_log_level("DEBUG")
```

### 2. 查看原始响应

在开发时，可以打印原始响应以了解数据结构：

```python
response = await self.client.post(...)
print(response.text)  # 查看原始文本
print(response.json())  # 查看 JSON（如果适用）
```

### 3. 使用断点调试

```python
import pdb

async def your_method(self):
    # ... 你的代码
    pdb.set_trace()  # 设置断点
    # ... 更多代码
```

或使用现代的 `breakpoint()`:

```python
async def your_method(self):
    # ... 你的代码
    breakpoint()  # Python 3.7+ 内置
    # ... 更多代码
```

---

## 常见开发任务

### 修改 API 请求结构

如果 Google 更新了 API 结构，你可能需要修改请求数据：

在 `client.py` 的 `generate_content` 方法中找到：

```python
data={
    "at": self.access_token,
    "f.req": json.dumps([
        None,
        json.dumps([
            # 这里是请求的实际数据结构
            # 根据抓包结果修改
        ]).decode(),
    ]).decode(),
}
```

### 解析新的响应字段

在 `client.py` 中，响应解析通常在这里：

```python
try:
    response_json = json.loads(response.text.split("\n")[2])
    # 根据新的响应结构调整索引
    body = json.loads(response_json[0][2])
    # ... 更多解析逻辑
except Exception:
    # 错误处理
```

### 添加新的工具函数

在 `src/gemini_webapi/utils/` 创建新文件或在现有文件中添加：

```python
# src/gemini_webapi/utils/your_util.py

async def your_utility_function(param):
    """工具函数说明"""
    # 实现
    return result
```

然后在 `utils/__init__.py` 导出：

```python
from .your_util import your_utility_function
```

---

## 测试你的修改

### 1. 编写单元测试

在 `tests/` 目录创建测试文件：

```python
# tests/test_your_feature.py
import unittest
from gemini_webapi import GeminiClient

class TestYourFeature(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = GeminiClient()
        await self.client.init()
    
    async def test_your_new_method(self):
        result = await self.client.your_new_method("test")
        self.assertIsNotNone(result)
        # 更多断言...
    
    async def asyncTearDown(self):
        await self.client.close()
```

### 2. 运行测试

```bash
pytest tests/test_your_feature.py -v
```

---

## 版本发布流程

### 1. 更新版本号

项目使用 `setuptools_scm`，版本自动从 git 标签生成：

```bash
# 创建新标签
git tag v0.2.0
git push origin v0.2.0
```

### 2. 构建包

```bash
# 安装构建工具
pip install build

# 构建
python -m build
```

### 3. 发布到 PyPI

```bash
# 安装 twine
pip install twine

# 上传到 TestPyPI（测试）
twine upload --repository testpypi dist/*

# 上传到 PyPI（正式）
twine upload dist/*
```

---

## 贡献代码

### 1. Fork 和分支

```bash
# Fork 项目后克隆你的 fork
git clone https://github.com/YOUR_USERNAME/Gemini-API.git

# 创建功能分支
git checkout -b feature/your-feature-name
```

### 2. 提交规范

```bash
# 提交消息格式
git commit -m "feat: add new feature description"
git commit -m "fix: fix bug description"
git commit -m "docs: update documentation"
```

### 3. 创建 Pull Request

- 确保所有测试通过
- 更新相关文档
- 在 PR 中详细描述你的更改

---

## 有用的资源

- **官方文档**: README.md
- **问题跟踪**: https://github.com/HanaokaYuzu/Gemini-API/issues
- **Python 异步编程**: https://docs.python.org/3/library/asyncio.html
- **Pydantic 文档**: https://docs.pydantic.dev/
- **HTTPX 文档**: https://www.python-httpx.org/

---

## 常见问题

### Q: 如何抓包分析 Gemini API？

**A**: 使用浏览器开发者工具：
1. 打开 https://gemini.google.com
2. F12 打开开发者工具
3. 切换到 Network 标签
4. 执行操作（发送消息等）
5. 查看 XHR/Fetch 请求
6. 分析请求和响应结构

### Q: 如何处理 API 变化？

**A**: 
1. 抓包查看新的请求/响应结构
2. 更新 `constants.py` 中的端点或模型
3. 修改 `client.py` 中的请求数据结构
4. 调整响应解析逻辑
5. 更新测试

### Q: 代码风格规范是什么？

**A**: 
- 使用 `black` 格式化
- 遵循 PEP 8
- 使用类型提示
- 编写 docstrings

---

## 开发检查清单

- [ ] 代码通过 `black` 格式化
- [ ] 代码通过 `flake8` 检查
- [ ] 添加了适当的类型提示
- [ ] 编写了 docstrings
- [ ] 添加了单元测试
- [ ] 所有测试通过
- [ ] 更新了文档
- [ ] 遵循 AGPL-3.0 许可证

---

**祝你开发愉快！** 🚀

如有问题，请在 GitHub Issues 中提出。
