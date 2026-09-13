# TestDuck

基于 Python + pytest + requests 的 RESTful API 接口自动化测试框架，覆盖 JSONPlaceholder 公开 API 的用户、帖子、评论三大资源，共 **48 条测试用例**。

![CI](https://github.com/LOVQ1026/TestDuck/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-9.1.1-0A9EDC?logo=pytest&logoColor=white)

---

## 项目简介

本项目针对 [JSONPlaceholder](https://jsonplaceholder.typicode.com/) 公开 REST API 搭建了一套**分层接口自动化测试框架**，覆盖用户（Users）、帖子（Posts）、评论（Comments）三大资源的 CRUD 操作及异常场景。

框架采用 **API 封装层 / 用例层 / 数据层 / 配置层** 四层架构，支持 YAML 数据驱动、参数化测试、Allure 可视化报告，并集成 **GitHub Actions** 实现持续集成。

---

## 技术栈

| 类别 | 技术 |
| :--- | :--- |
| 编程语言 | Python 3.14 |
| 测试框架 | pytest 9.1.1 |
| HTTP 请求 | requests 2.32.3 |
| 数据驱动 | ruamel.yaml 0.18.6 |
| 测试报告 | pytest-html 4.2.0 + Allure 2.13.5 |
| 持续集成 | GitHub Actions |
| 开发工具 | PyCharm |

---

## 测试覆盖

| 模块 | 用例数 | 覆盖场景 |
| :--- | :---: | :--- |
| 用户模块 | 23 | 列表查询、参数化 ID 查询、关联资源、CRUD、404 异常、非法 ID、邮箱格式、YAML 数据驱动 |
| 帖子模块 | 18 | 列表查询、按用户过滤、参数化详情、CRUD、空标题边界、关联评论 |
| 评论模块 | 11 | 列表查询、详情、字段完整性、参数化按帖子过滤、邮箱格式、创建评论 |
| **合计** | **48** | — |

**断言维度**：状态码 → 响应结构 → 字段完整性 → 业务数据一致性 → 数据格式（邮箱）。

---

## 目录结构

```
TestDuck/
├── .github/
│   └── workflows/
│       └── test.yml              # GitHub Actions CI 配置
├── api/                          # 接口封装层
│   ├── __init__.py
│   ├── base_api.py               # 基础请求封装
│   ├── users_api.py              # 用户模块接口
│   ├── posts_api.py              # 帖子模块接口
│   └── comments_api.py           # 评论模块接口
├── testcases/                    # 测试用例层
│   ├── __init__.py
│   ├── test_users.py             # 用户模块用例
│   ├── test_posts.py             # 帖子模块用例
│   └── test_comments.py          # 评论模块用例
├── data/                         # 测试数据层
│   └── test_data.yaml            # YAML 数据驱动文件
├── conftest.py                   # pytest 全局 fixture
├── pytest.ini                    # pytest 配置
├── requirements.txt              # 项目依赖
├── .gitignore
└── README.md
```

---

## 快速开始

### 环境要求

- Python 3.10+
- pip

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
# 运行全部用例
pytest

# 只运行某个模块
pytest testcases/test_users.py -v

# 查看详细输出
pytest -v -s
```

### 生成测试报告

pytest-html 报告（自动生成到 `report/report.html`）：

```bash
pytest
```

Allure 报告：

```bash
allure serve ./report/allure-results
```

---

## 持续集成

项目已配置 **GitHub Actions**，在代码 `push` 或 `pull request` 时自动：

1. 拉取代码
2. 安装 Python
3. 安装依赖
4. 执行全部测试用例
5. 上传 pytest-html 报告和 Allure 结果

工作流文件：[`.github/workflows/test.yml`](.github/workflows/test.yml)

---

## 作者

**LOVQ1026**

- GitHub：https://github.com/LOVQ1026
- 仓库：https://github.com/LOVQ1026/TestDuck

---

## License

本项目仅用于学习与个人能力展示。