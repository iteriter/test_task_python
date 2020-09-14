import sys, logging
import json
from typing import Dict
from aiohttp import web

POSTS_FILE = 'posts.json'
COMMENTS_FILE = 'comments.json'

log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

logger = logging.getLogger("posts_api")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(log_formatter)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class PostsApi:
    '''
    Api handler class
    '''
    posts: Dict
    comments: Dict

    def __init__(self):
        # load posts and comments from source files

        with open(POSTS_FILE, "r") as f:
            posts_json = f.read()
            self.posts = json.loads(posts_json)['posts']

            logger.debug(f'Loaded posts from file: {self.posts}')

        with open(COMMENTS_FILE, "r") as f:
            comments_json = f.read()
            self.comments = json.loads(comments_json)['comments']

            logger.debug(f'Loaded comments from file: {self.comments}')

    async def get_all_posts(self, request):
        logger.info('get_all_posts request')
        return web.json_response(text="This is get_all_posts request")

    async def get_post(self, request):
        logger.info('get_post request')
        return web.json_response(text="This is get post request")


if __name__ == "__main__":
    # start aiohttp server
    # listen for get requests
    # handle get requests with asyncio
        # handle all posts request
        # handle single post request

    logger.info('Starting Posts API web app')

    posts_api = PostsApi()

    app = web.Application()
    app.add_routes([web.get('/', posts_api.get_all_posts), web.get('/post/{id}', posts_api.get_post)])

    web.run_app(app)
