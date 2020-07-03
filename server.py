from flask import Flask
from flask import render_template
import cv2, json, os

app = Flask(__name__)

with open('db.json', 'r') as f:
    db = json.load(f)

@app.route('/')
def home():
    with open('db.json', 'r') as f:
        db = json.load(f)

    for name, video in db.items():
        if not os.path.isfile(video['thumbnail']):
            cap = cv2.VideoCapture(os.path.join('static/', video['video_path']))
            ret, img = cap.read()
            cv2.imwrite('static/thumbnails/%s.jpg' % (name), img)
            cap.release()

    return render_template('home.html', db=db)

@app.route('/watch/')
@app.route('/watch/<name>')
def watch(name=None):
    video = db[name]
    db[name]['views'] += 1

    with open('db.json', 'w') as f:
        json.dump(db, f)

    return render_template('watch.html', video=video)