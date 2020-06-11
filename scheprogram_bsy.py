from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
from flask import Flask, render_template, jsonify, request
import csv
app = Flask(__name__)

# URL 별로 함수명이 같거나,
# route('/') 등의 주소가 같으면 안됩니다.

client = MongoClient('mongodb://baesy828:dudtjsqo828@3.34.48.233', 27017,
                     username='baesy828',
                     password='dudtjsqo828')  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbscheduleManager


@app.route('/')
def home():
    return render_template('index.html')

# 스케쥴 입력을 포스트로 db에 보내기
@app.route('/schedules', methods=['POST'])
def input_schedule():
    date_receive = request.form['date_give'].strip()
    project_receive = request.form['project_give']
    content_receive = request.form['content_give']
    dodont_receive = request.form['dodont_give']

    schedule = {
        'scheduleDate': date_receive,
        'scheduleProject': project_receive,
        'scheduleContent': content_receive,
        'scheduleDodont': dodont_receive
    }

    db.schedules.insert_one(schedule)
    return jsonify({'result': 'success'})

    #elif request.method == 'PUT':
    #    delschedule = request.form

@app.route('/delete_schedule', methods=['POST'])
def delete_schedule():
    project_receive = request.form['scheduleProject']
    content_receive = request.form['scheduleContent']
    db.schedules.update({'scheduleProject': project_receive, 'scheduleContent': content_receive},
        {'$set': {
            'scheduleDodont': 'N'
        }})
    return jsonify({'result': 'success'})

# 스케쥴 입력을 겟으로 프론트에 보내기
@app.route('/schedules', methods=['GET'])
def show_schedule():
    schedules = list(db.schedules.find({'scheduleDodont': 'Y'}, {'_id': 0}))
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

@app.route('/delete_project', methods=['POST'])
def delete_project():
    name_receive = request.form['name_give']
    db.projects.update({'projectName': name_receive}, {'$set': {'isDeleted': 'Y'}})
    return jsonify({'result': 'success'})

# 프로젝트 입력을 겟으로 프론트에 보내기
@app.route('/projects', methods=['GET'])
def show_project():
    projects = list(db.projects.find({'isDeleted': 'N'}, {'_id': 0}))
    return jsonify({'result': 'success', 'projects': projects})


# 리뷰 입력을 포스트로 db에 보내기
@app.route('/reviews', methods=['POST'])
def input_review():
    OX_receive = request.form['OX_give']
    review_receive = request.form['review_give']
    prjreview_receive = request.form['prjreview_give']
    schereview_receive = request.form['schereview_give']

    db.schedules.update_one({'scheduleProject': prjreview_receive, 'scheduleContent': schereview_receive},
        {'$set': {'scheduleReview': review_receive, 'scheduleOX': OX_receive}})
    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
