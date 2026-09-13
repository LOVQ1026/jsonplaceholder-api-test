import pytest
import requests


# ============================================================
# 场景一：GET /users 获取用户列表
# ============================================================
def test_get_users_list(base_url):
    """获取用户列表，校验状态码、数据条数和字段完整性"""
    response = requests.get(f"{base_url}/users")

    # 断言状态码
    assert response.status_code == 200

    # 断言返回是列表且包含10个用户
    users = response.json()
    assert isinstance(users, list)
    assert len(users) == 10

    # 断言每个用户包含核心字段
    required_fields = ["id", "name", "username", "email"]
    for user in users:
        for field in required_fields:
            assert field in user, f"用户缺少字段: {field}"


# ============================================================
# 场景二：GET /users/{id} 单个用户 + 参数化
# ============================================================
@pytest.mark.parametrize("user_id, expected_name", [
    (1, "Leanne Graham"),
    (2, "Ervin Howell"),
    (3, "Clementine Bauch"),
])
def test_get_user_by_id(base_url, user_id, expected_name):
    """参数化测试：用多组数据验证单个用户查询接口（类似 Apifox 的 CSV 数据驱动）"""
    response = requests.get(f"{base_url}/users/{user_id}")

    assert response.status_code == 200
    user = response.json()

    # 这里直接对比数字和字符串，不用像 Apifox 那样强制转换
    assert user["id"] == user_id
    assert user["name"] == expected_name


# ============================================================
# 场景三：GET /users/9999 异常场景
# ============================================================
def test_get_nonexistent_user(base_url):
    """请求不存在的用户ID，应返回 404"""
    response = requests.get(f"{base_url}/users/9999")
    assert response.status_code == 404


# ============================================================
# 场景四：POST /users 创建用户
# ============================================================
def test_create_user(base_url):
    """创建用户，校验返回状态码、创建字段值和自动生成的ID"""
    payload = {
        "name": "测试用户",
        "username": "tester",
        "email": "tester@example.com"
    }
    response = requests.post(f"{base_url}/users", json=payload)

    # JSONPlaceholder 创建接口返回 201
    assert response.status_code == 201

    created_user = response.json()
    # 校验提交的字段值被正确接收
    assert created_user["name"] == "测试用户"
    assert created_user["username"] == "tester"
    assert created_user["email"] == "tester@example.com"
    # 校验服务端自动生成了ID
    assert "id" in created_user
    assert created_user["id"] == 11  # JSONPlaceholder 创建后固定返回的ID