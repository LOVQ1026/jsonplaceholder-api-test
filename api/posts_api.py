from api.base_api import BaseApi


class PostsApi(BaseApi):
    def get_posts(self):
        return self.send("get", "/posts")

    def get_post_by_id(self, post_id):
        return self.send("get", f"/posts/{post_id}")

    def get_posts_by_user(self, user_id):
        return self.send("get", "/posts", params={"userId": user_id})

    def create_post(self, payload):
        return self.send("post", "/posts", json=payload)

    def update_post(self, post_id, payload):
        return self.send("put", f"/posts/{post_id}", json=payload)

    def delete_post(self, post_id):
        return self.send("delete", f"/posts/{post_id}")

    def get_post_comments(self, post_id):
        return self.send("get", f"/posts/{post_id}/comments")