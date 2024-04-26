import praw
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from better_profanity import profanity


SUBREDDITS = ["shortscarystories", "nosleep", "creepypasta", "horrorstories"]

@dataclass
class RedditPost:
    title: str
    text: str

def get_post(subreddit_name=None):
    """Fetch and return a post from a specified subreddit, cycling through a list if none is specified."""
    reddit = setup_reddit_client()
    if reddit is None:
        return None

    if subreddit_name is None:
        subreddit_name = choose_subreddit()

    try:
        subreddit = reddit.subreddit(subreddit_name)
        print(f"Accessing subreddit: {subreddit_name}")
        for post in subreddit.hot(limit=10):
            if post.is_self and not post.stickied:
                return post_content(post)
    except praw.exceptions.PRAWException as e:
        print(f"Error accessing subreddit or processing posts: {e}")

    print("No suitable text posts found.")
    return None

def get_post_from_url(url):
    """Fetch and return a Reddit post by URL."""
    reddit = setup_reddit_client()
    if reddit is None:
        return None

    try:
        post = reddit.submission(url=url)
        if post.is_self:
            return post_content(post)
    except praw.exceptions.PRAWException as e:
        print(f"Error accessing specific post: {e}")
    return None


########## HELPER FUNCTIONS ##########

def setup_reddit_client():
    load_dotenv()
    try:
        return praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
    except Exception as e:
        print(f"Error setting up Reddit API: {e}")
        return None

def post_content(post):
    """Censor and return the title and text of a post."""
    profanity.load_censor_words()
    title = profanity.censor(post.title)
    text = profanity.censor(post.selftext)
    return RedditPost(title=title, text=text)

def choose_subreddit():
    subreddits = SUBREDDITS
    index_file = 'subreddit_index.txt'
    current_index = get_current_index(index_file)
    update_index(index_file, current_index, len(subreddits))
    return subreddits[current_index]

def get_current_index(file_path):
    try:
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        with open(file_path, 'w') as file:
            file.write("0")
        return 0
    except Exception as e:
        print(f"Error reading index file: {e}")
        return 0

def update_index(file_path, current_index, max_index):
    try:
        with open(file_path, 'w') as file:
            file.write(str((current_index + 1) % max_index))
    except Exception as e:
        print(f"Error updating index file: {e}")


if __name__ == "__main__":
    post = get_post()
    if post:
        print(post.title)
        print(post.text)
    else:
        print("Failed to retrieve a post.")
        