import pytest
from api.users_api import UsersApi
from api.posts_api import PostsApi
from api.comments_api import CommentsApi

BASE_URL = "https://jsonplaceholder.typicode.com"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def users_api(base_url):
    return UsersApi(base_url)


@pytest.fixture(scope="session")
def posts_api(base_url):
    return PostsApi(base_url)


@pytest.fixture(scope="session")
def comments_api(base_url):
    return CommentsApi(base_url)