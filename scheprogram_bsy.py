from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

# URL 별로 함수명이 같거나,
# route('/') 등의 주소가 같으면 안됩니다.

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbscheduleManager


@app.route('/')
def home():
    return render_template('index.html')

# 스케쥴 입력을 포스트로 db에 보내기
@app.route('/schedules', methods=['POST'])
def input_schedule():
    date_receive = request.form['date_give']
    project_receive = request.form['project_give']
    content_receive = request.form['content_give']

    schedule = {
        'scheduleDate': date_receive,
        'scheduleProject': project_receive,
        'scheduleContent': content_receive
    }

    db.schedules.insert_one(schedule)
    return jsonify({'result': 'success'})

# 스케쥴 입력을 겟으로 프론트에 보내기
@app.route('/schedules', methods=['GET'])
def show_schedule():
    schedules = list(db.schedules.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'schedules': schedules})


# 프로젝트 입력을 포스트로 db에 보내기
@app.route('/projects', methods=['POST'])
def input_project():
    name_receive = request.form['name_give']
    goal_receive = request.form['goal_give']
    pcontent_receive = request.form['pcontent_give']

    project = {
        'projectName': name_receive,
        'projectGoal': goal_receive,
        'projectContent': pcontent_receive
    }

    db.projects.insert_one(project)
    return jsonify({'result': 'success'})

# 프로젝트 입력을 겟으로 프론트에 보내기
@app.route('/projects', methods=['GET'])
def show_project():
    projects = list(db.projects.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'projects': projects})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
