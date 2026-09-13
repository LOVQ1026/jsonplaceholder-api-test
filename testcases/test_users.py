import pytest
from api.users_api import UsersApi


class TestUsersList:
    """用户列表查询"""

    def test_get_users_list_status_code(self, users_api):
        """获取用户列表，状态码 200"""
        resp = users_api.get_users()
        assert resp.status_code == 200

    def test_get_users_list_count(self, users_api):
        """用户列表默认返回 10 条数据"""
        resp = users_api.get_users()
        assert len(resp.json()) == 10

    def test_get_users_list_is_array(self, users_api):
        """响应体为数组类型"""
        resp = users_api.get_users()
        assert isinstance(resp.json(), list)

    def test_get_users_list_required_fields(self, users_api):
        """每条用户数据都包含 id/name/username/email 等核心字段"""
        resp = users_api.get_users()
        required = ["id", "name", "username", "email", "address", "phone", "website", "company"]
        for user in resp.json():
            for field in required:
                assert field in user, f"缺少字段: {field}"

    def test_get_users_email_format(self, users_api):
        """用户邮箱格式符合 xxx@xxx.xxx"""
        resp = users_api.get_users()
        for user in resp.json():
            assert "@" in user["email"] and "." in user["email"]


class TestUserDetail:
    """单个用户查询（参数化）"""

    @pytest.mark.parametrize("user_id, expected_name", [
        (1, "Leanne Graham"),
        (2, "Ervin Howell"),
        (3, "Clementine Bauch"),
        (5, "Chelsey Dietrich"),
        (10, "Clementina DuBuque"),
    ])
    def test_get_user_by_id(self, users_api, user_id, expected_name):
        """按 ID 查询用户，校验 ID 和 name 一致"""
        resp = users_api.get_user_by_id(user_id)
        assert resp.status_code == 200
        user = resp.json()
        assert user["id"] == user_id
        assert user["name"] == expected_name

    def test_get_user_nonexistent(self, users_api):
        """查询不存在的用户，返回 404"""
        resp = users_api.get_user_by_id(9999)
        assert resp.status_code == 404

    def test_get_user_illegal_id(self, users_api):
        """非法 ID（字符串），返回 404"""
        resp = users_api.send("get", "/users/abc")
        assert resp.status_code in [404, 400]


class TestUserRelatedResources:
    """用户关联资源查询"""

    def test_get_user_posts(self, users_api):
        """查询用户 1 的所有帖子，应返回 10 条"""
        resp = users_api.get_user_posts(1)
        assert resp.status_code == 200
        posts = resp.json()
        assert len(posts) == 10
        for post in posts:
            assert post["userId"] == 1

    def test_get_user_todos(self, users_api):
        """查询用户 1 的待办事项"""
        resp = users_api.get_user_todos(1)
        assert resp.status_code == 200
        todos = resp.json()
        assert len(todos) > 0
        for todo in todos:
            assert todo["userId"] == 1

    def test_get_user_albums(self, users_api):
        """查询用户 1 的相册"""
        resp = users_api.get_user_albums(1)
        assert resp.status_code == 200
        albums = resp.json()
        assert len(albums) == 10


class TestUserCRUD:
    """用户增删改"""

    def test_create_user(self, users_api):
        """创建用户，返回 201 且回显提交字段"""
        payload = {
            "name": "张三",
            "username": "zhangsan",
            "email": "zhangsan@example.com"
        }
        resp = users_api.create_user(payload)
        assert resp.status_code == 201
        created = resp.json()
        assert created["name"] == "张三"
        assert created["username"] == "zhangsan"
        assert created["email"] == "zhangsan@example.com"
        assert "id" in created

    def test_update_user(self, users_api):
        """全量更新用户，校验字段被覆盖"""
        payload = {
            "id": 1,
            "name": "New Name",
            "username": "newname",
            "email": "new@example.com"
        }
        resp = users_api.update_user(1, payload)
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["name"] == "New Name"
        assert updated["email"] == "new@example.com"

    def test_patch_user(self, users_api):
        """部分更新用户，仅修改 name"""
        resp = users_api.patch_user(1, {"name": "Patched Name"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Patched Name"

    def test_delete_user(self, users_api):
        """删除用户，返回 200 或 204"""
        resp = users_api.delete_user(1)
        assert resp.status_code in [200, 204]