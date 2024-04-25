from flask import Flask, render_template, jsonify, request
from reddit_scraper import get_post, get_post_from_url

app = Flask(__name__)

@app.route('/api/get_post', methods=['GET'])
def api_get_post():
    subreddit_name = request.args.get('subreddit_name', default=None, type=str)
    result = get_post(subreddit_name=subreddit_name)
    if result:
        return jsonify(result.__dict__), 200
    else:
        return jsonify({'error': 'No suitable post found or invalid subreddit'}), 404

@app.route('/api/get_post_from_url', methods=['GET'])
def api_get_post_from_url():
    url = request.args.get('url', type=str)
    result = get_post_from_url(url)
    if result:
        return jsonify(result.__dict__), 200
    else:
        return jsonify({'error': 'Post not found or error accessing the URL'}), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def video():
    return render_template('video_creation.html')

if __name__ == '__main__':
    app.run(debug=True)