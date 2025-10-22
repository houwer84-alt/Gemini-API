#!/usr/bin/env python3
"""
开发环境快速测试脚本
用于验证修改后的代码是否正常工作
"""
import asyncio
import os
from pathlib import Path

# 从本地源码导入（开发模式）
from gemini_webapi import GeminiClient, set_log_level
from gemini_webapi.constants import Model

# 设置日志级别
set_log_level("DEBUG")


async def test_basic_chat():
    """测试基本对话功能"""
    print("=" * 60)
    print("测试 1: 基本对话")
    print("=" * 60)
    
    # 从环境变量读取 cookies（推荐）
    secure_1psid = os.getenv("SECURE_1PSID")
    secure_1psidts = os.getenv("SECURE_1PSIDTS")
    
    # 创建客户端
    if secure_1psid:
        client = GeminiClient(secure_1psid, secure_1psidts)
    else:
        # 尝试从浏览器自动读取
        print("⚠️  未设置环境变量，尝试从浏览器读取 cookies...")
        client = GeminiClient()
    
    try:
        # 初始化客户端
        await client.init(auto_refresh=False, verbose=True)
        
        # 发送测试消息
        response = await client.generate_content(
            "用一句话介绍你自己",
            model=Model.G_2_5_FLASH
        )
        
        print(f"\n✅ 回复: {response.text}\n")
        
        # 关闭客户端
        await client.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}\n")
        return False


async def test_chat_session():
    """测试多轮对话"""
    print("=" * 60)
    print("测试 2: 多轮对话")
    print("=" * 60)
    
    secure_1psid = os.getenv("SECURE_1PSID")
    secure_1psidts = os.getenv("SECURE_1PSIDTS")
    
    client = GeminiClient(secure_1psid, secure_1psidts) if secure_1psid else GeminiClient()
    
    try:
        await client.init(auto_refresh=False, verbose=True)
        
        # 创建对话会话
        chat = client.start_chat()
        
        # 第一轮
        response1 = await chat.send_message("记住这个数字：42")
        print(f"第一轮: {response1.text}")
        
        # 第二轮（测试上下文记忆）
        response2 = await chat.send_message("我刚才让你记住的数字是多少？")
        print(f"第二轮: {response2.text}")
        
        # 检查是否记住了
        if "42" in response2.text:
            print("\n✅ 上下文记忆测试通过！\n")
            return True
        else:
            print("\n⚠️  上下文记忆可能有问题\n")
            return False
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}\n")
        return False
    finally:
        await client.close()


async def test_file_upload():
    """测试文件上传功能"""
    print("=" * 60)
    print("测试 3: 文件上传")
    print("=" * 60)
    
    # 检查是否有测试文件
    test_file = Path("assets/banner.png")
    if not test_file.exists():
        print(f"⚠️  测试文件不存在: {test_file}")
        print("跳过文件上传测试\n")
        return None
    
    secure_1psid = os.getenv("SECURE_1PSID")
    secure_1psidts = os.getenv("SECURE_1PSIDTS")
    
    client = GeminiClient(secure_1psid, secure_1psidts) if secure_1psid else GeminiClient()
    
    try:
        await client.init(auto_refresh=False, verbose=True)
        
        response = await client.generate_content(
            "这张图片里有什么？请简短描述。",
            files=[str(test_file)]
        )
        
        print(f"\n✅ 回复: {response.text}\n")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}\n")
        return False
    finally:
        await client.close()


async def main():
    """运行所有测试"""
    print("\n🚀 开始开发环境测试...\n")
    
    # 检查环境变量
    if not os.getenv("SECURE_1PSID"):
        print("⚠️  提示: 未设置 SECURE_1PSID 环境变量")
        print("   可以:")
        print("   1. 创建 .env 文件并设置环境变量")
        print("   2. 或安装 browser-cookie3 自动读取浏览器 cookies")
        print("   3. 或通过 export SECURE_1PSID=xxx 设置\n")
    
    results = []
    
    # 运行测试
    results.append(("基本对话", await test_basic_chat()))
    results.append(("多轮对话", await test_chat_session()))
    results.append(("文件上传", await test_file_upload()))
    
    # 总结
    print("=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    for test_name, result in results:
        if result is None:
            status = "⊘ 跳过"
        elif result:
            status = "✅ 通过"
        else:
            status = "❌ 失败"
        print(f"{test_name:20} {status}")
    
    print("=" * 60)
    print("\n✨ 测试完成！")


if __name__ == "__main__":
    asyncio.run(main())
