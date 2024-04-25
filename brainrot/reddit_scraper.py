import praw
import os
from dotenv import load_dotenv
from dataclasses import dataclass
from better_profanity import profanity

def get_current_index(file_path):
    try:
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        # If the file does not exist, create it and initialize with 0
        with open(file_path, 'w') as file:
            file.write("0")
        return 0
    except Exception as e:
        print(f"Error reading index file: {e}")
        return 0  # Default to 0 if file does not exist or error occurs

def update_index(file_path, current_index, max_index):
    try:
        new_index = (current_index + 1) % max_index  # Cycle back to 0 after reaching the max index
        with open(file_path, 'w') as file:
            file.write(str(new_index))
    except Exception as e:
        print(f"Error updating index file: {e}")

@dataclass
class RedditPost:
    title: str
    text: str

def get_post():
    load_dotenv()
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT")
        )
    except Exception as e:
        print(f"Error setting up Reddit API: {e}")
        return None

    subreddits = ["shortscarystories", "nosleep", "creepypasta", "horrorstories"]
    index_file = 'subreddit_index.txt'

    for _ in range(len(subreddits)):
        current_index = get_current_index(index_file)
        subreddit_name = subreddits[current_index]
        update_index(index_file, current_index, len(subreddits))

        try:
            subreddit = reddit.subreddit(subreddit_name)
            print(f"Accessing subreddit: {subreddit_name}\n")

            for post in subreddit.hot(limit=10):
                if post.is_self and not post.stickied:
                    profanity.load_censor_words()
                    title = profanity.censor(post.title)
                    text = profanity.censor(post.selftext)
                    return RedditPost(title=title, text=text)
        except Exception as e:
            print(f"Error accessing subreddit or processing posts: {e}")

    print("No suitable text posts found.\n")
    return None

if __name__ == "__main__":
    post = get_post()
    if post:
        print(post.title)
        print(post.text)
    else:
        print("Failed to retrieve a post.")
        