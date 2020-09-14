import pytest
import json
from aiohttp import web
from test_task import PostsApi

pytest_plugins = 'aiohttp.pytest_plugin'

@pytest.fixture
def server(loop, aiohttp_client):
    posts_api = PostsApi()

    app = web.Application()
    app.add_routes([web.get('/', posts_api.get_all_posts), web.get('/post/{id}', posts_api.get_post)])

    return loop.run_until_complete(aiohttp_client(app))

def get_item_ids(items):
    return [item['id'] for item in items]

async def test_get_all_posts(server):
    resp = await server.get('/')
    content = await resp.text()
    data = json.loads(content)

    assert resp.status == 200
    assert data['posts_count'] == 4

    # check number of posts returned is correct
    assert len(data['posts']) == 4

async def test_get_all_posts_sorted(server):
    resp = await server.get('/')
    content = await resp.text()
    data = json.loads(content)

    # check posts returned in correct orders
    ids = get_item_ids(data['posts'])
    assert ids == [5, 1, 2, 8] or ids == [5, 2, 1, 8]

async def test_get_all_posts_comments_count(server):
    resp = await server.get('/')
    content = await resp.text()
    data = json.loads(content)

    for post in data['posts']:
        if post['id'] == 1:
            assert post['comments_count'] == 2
            assert len(post['comments']) == 2

async def test_get_all_posts_only_valid(server):
    resp = await server.get('/')
    content = await resp.text()
    data = json.loads(content)

    ids = get_item_ids(data['posts'])
    assert 6 not in ids
    assert 7 not in ids

async def test_get_post(server):
    resp = await server.get('/post/1')

    assert resp.status == 200

async def test_get_post_comments_count(server):
    resp = await server.get('/post/1')
    content = await resp.text()
    data = json.loads(content)

    assert data['comments_count'] == 2

    resp = await server.get('/post/2')
    content = await resp.text()
    data = json.loads(content)

    assert data['comments_count'] == 0

async def test_get_post_comments_sorted(server):
    resp = await server.get('/post/1')
    content = await resp.text()
    data = json.loads(content)

    comments = data['comments']
    ids = get_item_ids(comments)

    assert ids == [2,1]

async def test_get_post_deleted(server):
    resp = await server.get('/post/6')

    assert resp.status == 404

async def test_get_post_non_existent(server):
    resp = await server.get('/post/100')

    assert resp.status == 404

async def test_get_post_future(server):
    resp = await server.get('/post/7')

    assert resp.status == 404
