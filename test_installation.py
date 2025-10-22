#!/usr/bin/env python3
"""
测试 gemini-webapi 安装是否成功
"""
import sys

def test_imports():
    """测试所有核心模块是否可以导入"""
    print("🔍 测试模块导入...")
    
    try:
        from gemini_webapi import GeminiClient, ChatSession
        print("✅ GeminiClient, ChatSession 导入成功")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    
    try:
        from gemini_webapi.constants import Model, Endpoint, Headers
        print("✅ 常量模块导入成功")
    except ImportError as e:
        print(f"❌ 常量模块导入失败: {e}")
        return False
    
    try:
        from gemini_webapi.types import Gem, GemJar, ModelOutput, Candidate, Image
        print("✅ 类型模块导入成功")
    except ImportError as e:
        print(f"❌ 类型模块导入失败: {e}")
        return False
    
    try:
        from gemini_webapi.exceptions import (
            AuthError, APIError, GeminiError, 
            TimeoutError, UsageLimitExceeded
        )
        print("✅ 异常类导入成功")
    except ImportError as e:
        print(f"❌ 异常类导入失败: {e}")
        return False
    
    try:
        from gemini_webapi import set_log_level, logger
        print("✅ 日志模块导入成功")
    except ImportError as e:
        print(f"❌ 日志模块导入失败: {e}")
        return False
    
    return True


def test_dependencies():
    """测试依赖包是否安装"""
    print("\n🔍 测试依赖包...")
    
    dependencies = [
        ("httpx", "HTTP 客户端"),
        ("loguru", "日志系统"),
        ("orjson", "JSON 解析"),
        ("pydantic", "数据验证"),
    ]
    
    all_ok = True
    for module_name, desc in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {module_name:15} - {desc}")
        except ImportError:
            print(f"❌ {module_name:15} - {desc} (未安装)")
            all_ok = False
    
    # 可选依赖
    print("\n🔍 测试可选依赖...")
    try:
        import browser_cookie3
        print("✅ browser_cookie3  - 浏览器 Cookie 支持")
    except ImportError:
        print("⚠️  browser_cookie3  - 未安装 (可选)")
    
    return all_ok


def test_client_creation():
    """测试客户端创建"""
    print("\n🔍 测试客户端创建...")
    
    try:
        from gemini_webapi import GeminiClient
        
        # 测试不带参数创建
        client = GeminiClient()
        print("✅ 无参数创建客户端成功")
        
        # 测试带参数创建
        client = GeminiClient(
            secure_1psid="test_psid",
            secure_1psidts="test_psidts",
            proxy="http://127.0.0.1:7890"
        )
        print("✅ 带参数创建客户端成功")
        
        # 测试 ChatSession
        chat = client.start_chat()
        print("✅ 创建聊天会话成功")
        
        return True
    except Exception as e:
        print(f"❌ 客户端创建失败: {e}")
        return False


def test_version():
    """测试版本信息"""
    print("\n🔍 版本信息...")
    
    try:
        import gemini_webapi
        if hasattr(gemini_webapi, '__version__'):
            print(f"✅ gemini-webapi 版本: {gemini_webapi.__version__}")
        else:
            print("⚠️  版本信息未找到 (开发模式正常)")
    except Exception as e:
        print(f"⚠️  无法获取版本: {e}")
    
    print(f"✅ Python 版本: {sys.version}")


def main():
    """主测试函数"""
    print("=" * 60)
    print("🚀 Gemini WebAPI 安装验证")
    print("=" * 60)
    
    results = []
    
    # 运行所有测试
    results.append(("模块导入", test_imports()))
    results.append(("依赖包", test_dependencies()))
    results.append(("客户端创建", test_client_creation()))
    test_version()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("🎉 所有测试通过！环境配置成功！")
        print("\n📝 下一步:")
        print("   1. 查看 README.md 了解使用方法")
        print("   2. 运行 python examples/basic_usage.py 查看示例")
        print("   3. 开始你的二次开发！")
        return 0
    else:
        print("⚠️  部分测试失败，请检查安装")
        print("\n🔧 建议:")
        print("   1. 运行: pip install -e .")
        print("   2. 确保 Python >= 3.10")
        print("   3. 检查依赖是否正确安装")
        return 1


if __name__ == "__main__":
    sys.exit(main())
