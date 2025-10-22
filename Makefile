# Makefile for Gemini WebAPI Development

.PHONY: help install dev-install test format lint clean build

help:  ## 显示帮助信息
	@echo "Gemini WebAPI 开发命令:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## 安装项目依赖
	pip install -e .
	@echo "✅ 项目依赖安装完成"

dev-install:  ## 安装开发依赖
	pip install -e .
	pip install black flake8 pytest pytest-asyncio mypy
	pip install browser-cookie3
	@echo "✅ 开发环境配置完成"

test:  ## 运行测试
	pytest tests/ -v

test-cov:  ## 运行测试并生成覆盖率报告
	pytest tests/ --cov=src/gemini_webapi --cov-report=html
	@echo "📊 覆盖率报告生成在 htmlcov/index.html"

format:  ## 格式化代码
	black src/ tests/
	@echo "✅ 代码格式化完成"

format-check:  ## 检查代码格式（不修改）
	black --check src/ tests/

lint:  ## 代码质量检查
	flake8 src/ tests/ --max-line-length=120
	@echo "✅ 代码检查通过"

type-check:  ## 类型检查
	mypy src/ --ignore-missing-imports

verify:  ## 验证安装
	python test_installation.py

dev-test:  ## 运行开发测试
	python dev_example.py

clean:  ## 清理临时文件
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf dist/ build/
	@echo "✅ 清理完成"

build:  ## 构建包
	pip install build
	python -m build
	@echo "✅ 包构建完成，位于 dist/ 目录"

docs:  ## 生成文档（如果有）
	@echo "📚 文档已在 README.md 和 DEVELOPMENT.md"

all: clean format lint test  ## 运行所有检查
	@echo "✅ 所有检查完成"
