from api.base_api import BaseApi


class UsersApi(BaseApi):
    def get_users(self):
        return self.send("get", "/users")

    def get_user_by_id(self, user_id):
        return self.send("get", f"/users/{user_id}")

    def create_user(self, payload):
        return self.send("post", "/users", json=payload)

    def update_user(self, user_id, payload):
        return self.send("put", f"/users/{user_id}", json=payload)

    def patch_user(self, user_id, payload):
        return self.send("patch", f"/users/{user_id}", json=payload)

    def delete_user(self, user_id):
        return self.send("delete", f"/users/{user_id}")

    def get_user_posts(self, user_id):
        return self.send("get", "/posts", params={"userId": user_id})

    def get_user_todos(self, user_id):
        return self.send("get", "/todos", params={"userId": user_id})

    def get_user_albums(self, user_id):
        return self.send("get", "/albums", params={"userId": user_id})