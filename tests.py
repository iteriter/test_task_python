import pytest
from aiohttp import web
from test_task import PostsApi

pytest_plugins = 'aiohttp.pytest_plugin'

@pytest.fixture
def server(loop, aiohttp_client):
    posts_api = PostsApi()

    app = web.Application()
    app.add_routes([web.get('/', posts_api.get_all_posts), web.get('/post/{id}', posts_api.get_post)])

    return loop.run_until_complete(aiohttp_client(app))

async def test_get_all_posts(server):
    resp = await server.get('/')
    assert resp.status == 200

def test_get_all_posts_sorted():
    pass

def test_get_all_posts_comments_count():
    pass

def test_get_all_posts_only_valid():
    pass

def test_get_post():
    pass

def test_get_post_comments_sorted():
    pass

def test_get_post_comments_count():
    pass

def test_get_post_deleted():
    pass

def test_get_post_non_existent():
    pass

def test_get_post_future():
    pass
