from api.base_api import BaseApi


class CommentsApi(BaseApi):
    def get_comments(self):
        return self.send("get", "/comments")

    def get_comment_by_id(self, comment_id):
        return self.send("get", f"/comments/{comment_id}")

    def get_comments_by_post(self, post_id):
        return self.send("get", "/comments", params={"postId": post_id})

    def create_comment(self, payload):
        return self.send("post", "/comments", json=payload)