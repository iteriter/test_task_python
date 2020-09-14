import sys, logging
import json
from datetime import datetime
from typing import Dict
import pathlib

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

        # store posts in dict by id

        for file in (POSTS_FILE, COMMENTS_FILE):
            path = pathlib.Path(file)

            if not path.exists() or not path.is_file():
                logger.critical(f"Source file not found: {file}")
                raise FileNotFoundError

        with open(POSTS_FILE, "r") as f:
            posts_json = f.read()
            posts_list = json.loads(posts_json)['posts']

            self.posts = {}
            # keep id for completeness of post object
            for post in posts_list:
                self.posts[post['id']] = post

            logger.debug(f'Loaded posts from file: {self.posts}')

        with open(COMMENTS_FILE, "r") as f:
            comments_json = f.read()
            self.comments = json.loads(comments_json)['comments']

            logger.debug(f'Loaded comments from file: {self.comments}')

    @classmethod
    def post_to_response(cls, post):
        post.pop('deleted', None)
        return post

    @classmethod
    def post_available(cls, post):
        logger.debug(f'Checking if post is available for request: {post}')
        return not post['deleted'] and datetime.fromisoformat(post['date']) < datetime.now()

    async def get_all_posts(self, request):
        logger.info('get_all_posts request')

        # ATTENTION! make copy of post dicts to avoid modifying source data
        # only return posts that are not deleted and the date is not in the future
        posts = [post.copy() for post in self.posts.values() if self.post_available(post)]

        # remove irrelevant field from response
        posts = list(map(self.post_to_response, posts))

        # get comment counts for posts
        for post in posts:
            post['comments_count'] = len([comment for comment in self.comments if comment['post_id'] == post['id']])

        data = {
                "posts": posts,
                "posts_count": len(posts)
            }

        return web.json_response(text=json.dumps(data))


    async def get_post(self, request):
        logger.info('get_post request')

        post_id = int(request.match_info['id'])
        post = self.posts.get(post_id, None)

        logger.debug(f'Post requested with id {post_id}, lookup result: {post}')

        if post and self.post_available(post):
            post = self.post_to_response(post)
            return web.json_response(text=json.dumps(post))
        else:
            raise web.HTTPNotFound


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
