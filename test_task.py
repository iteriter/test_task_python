import sys, logging
import json
from datetime import datetime
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

        # store posts in dict by id
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

    async def get_all_posts(self, request):
        logger.info('get_all_posts request')

        # only return posts that are not deleted and the date is not in the future
        posts = [post for post in self.posts.values() if not post['deleted']
                                                and datetime.fromisoformat(post['date']) < datetime.now()]

        # remove irrelevant field from response
        for post in posts:
            post.pop('deleted')

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
