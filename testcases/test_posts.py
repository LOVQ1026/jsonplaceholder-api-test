import pytest


class TestPostsList:
    """帖子列表"""

    def test_get_posts_count(self, posts_api):
        """帖子总数为 100"""
        resp = posts_api.get_posts()
        assert resp.status_code == 200
        assert len(resp.json()) == 100

    def test_get_posts_required_fields(self, posts_api):
        """每条帖子包含 userId/id/title/body"""
        resp = posts_api.get_posts()
        for post in resp.json():
            for field in ["userId", "id", "title", "body"]:
                assert field in post

    def test_get_posts_by_user_filter(self, posts_api):
        """按 userId 过滤，用户 1 应有 10 条帖子"""
        resp = posts_api.get_posts_by_user(1)
        assert resp.status_code == 200
        posts = resp.json()
        assert len(posts) == 10
        for post in posts:
            assert post["userId"] == 1

    @pytest.mark.parametrize("user_id, expected_count", [
        (1, 10), (2, 10), (3, 10), (5, 10), (10, 10),
    ])
    def test_posts_count_by_user(self, posts_api, user_id, expected_count):
        """参数化：每个用户都拥有 10 条帖子"""
        resp = posts_api.get_posts_by_user(user_id)
        assert len(resp.json()) == expected_count


class TestPostDetail:
    """帖子详情"""

    @pytest.mark.parametrize("post_id", [1, 10, 50, 100])
    def test_get_post_by_id(self, posts_api, post_id):
        """按 ID 查询帖子，ID 一致"""
        resp = posts_api.get_post_by_id(post_id)
        assert resp.status_code == 200
        assert resp.json()["id"] == post_id

    def test_get_post_nonexistent(self, posts_api):
        """查询不存在的帖子返回 404"""
        resp = posts_api.get_post_by_id(9999)
        assert resp.status_code == 404


class TestPostCRUD:
    """帖子增删改"""

    def test_create_post(self, posts_api):
        """创建帖子，返回 201"""
        payload = {"title": "自动化测试", "body": "pytest 实战", "userId": 1}
        resp = posts_api.create_post(payload)
        assert resp.status_code == 201
        created = resp.json()
        assert created["title"] == "自动化测试"
        assert created["body"] == "pytest 实战"
        assert created["userId"] == 1

    def test_create_post_empty_title(self, posts_api):
        """创建帖子 title 为空"""
        payload = {"title": "", "body": "正文", "userId": 1}
        resp = posts_api.create_post(payload)
        assert resp.status_code == 201  # JSONPlaceholder 不做校验

    def test_update_post(self, posts_api):
        """全量更新帖子"""
        payload = {"id": 1, "title": "更新后的标题", "body": "更新后的正文", "userId": 1}
        resp = posts_api.update_post(1, payload)
        assert resp.status_code == 200
        assert resp.json()["title"] == "更新后的标题"

    def test_delete_post(self, posts_api):
        """删除帖子"""
        resp = posts_api.delete_post(1)
        assert resp.status_code in [200, 204]


class TestPostComments:
    """帖子关联评论"""

    def test_get_post_comments(self, posts_api):
        """帖子 1 的评论数为 5"""
        resp = posts_api.get_post_comments(1)
        assert resp.status_code == 200
        comments = resp.json()
        assert len(comments) == 5
        for c in comments:
            assert c["postId"] == 1