from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def video():
    return render_template('video_creation.html')

if __name__ == '__main__':
    app.run(debug=True)