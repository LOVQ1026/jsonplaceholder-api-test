import pytest


class TestComments:
    """评论接口测试"""

    def test_get_comments_count(self, comments_api):
        """评论总数为 500"""
        resp = comments_api.get_comments()
        assert resp.status_code == 200
        assert len(resp.json()) == 500

    def test_get_comment_by_id(self, comments_api):
        """按 ID 查评论"""
        resp = comments_api.get_comment_by_id(1)
        assert resp.status_code == 200
        assert resp.json()["id"] == 1

    def test_get_comment_required_fields(self, comments_api):
        """评论包含 postId/id/name/email/body"""
        resp = comments_api.get_comment_by_id(1)
        comment = resp.json()
        for field in ["postId", "id", "name", "email", "body"]:
            assert field in comment

    def test_get_comment_nonexistent(self, comments_api):
        """查询不存在的评论"""
        resp = comments_api.get_comment_by_id(9999)
        assert resp.status_code == 404

    @pytest.mark.parametrize("post_id, expected_count", [
        (1, 5), (2, 5), (3, 5), (10, 5),
    ])
    def test_comments_by_post(self, comments_api, post_id, expected_count):
        """参数化：每个帖子都有 5 条评论"""
        resp = comments_api.get_comments_by_post(post_id)
        assert len(resp.json()) == expected_count

    def test_comment_email_format(self, comments_api):
        """评论邮箱格式校验"""
        resp = comments_api.get_comments()
        for c in resp.json()[:20]:
            assert "@" in c["email"]

    def test_create_comment(self, comments_api):
        """创建评论"""
        payload = {"postId": 1, "name": "测试评论", "email": "test@x.com", "body": "内容"}
        resp = comments_api.create_comment(payload)
        assert resp.status_code == 201
        assert resp.json()["name"] == "测试评论"

    def test_comments_filter_by_post(self, comments_api):
        """按 postId 过滤，返回结果全部匹配"""
        resp = comments_api.get_comments_by_post(5)
        for c in resp.json():
            assert c["postId"] == 5