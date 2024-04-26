from flask import Flask, render_template, jsonify, request
from .reddit_scraper import get_post, get_post_from_url
from .video import get_video
import json
from .reddit_scraper import get_post, get_post_from_url
from .video import get_video

app = Flask(__name__)


@app.route("/api/get_post", methods=["GET"])
def api_get_post():
    subreddit_name = request.args.get("subreddit_name", default=None, type=str)
    post = get_post(subreddit_name=subreddit_name)

    if post:
        get_video(post)
        return jsonify(post.__dict__), 200
    else:
        return jsonify({"error": "No suitable post found or invalid subreddit"}), 404


@app.route("/api/get_post_from_url", methods=["GET"])
def api_get_post_from_url():
    url = request.args.get("url", type=str)
    post = get_post_from_url(url)

    if post:
        get_video(post)
        return jsonify(post.__dict__), 200
    else:
        return jsonify({"error": "Post not found or error accessing the URL"}), 404


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def video():
    if request.method == "POST":
        data = json.loads(request.data)
        url = data["url"]
        post = get_post_from_url(url)
        get_video(post)
        return jsonify({"url": data})
    elif request.method == "GET":
        return render_template("video_creation.html")


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
