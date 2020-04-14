from flask import Flask, render_template,jsonify,request
app = Flask(__name__)

# URL 별로 함수명이 같거나,
# route('/') 등의 주소가 같으면 안됩니다.

from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbscheduleManager

@app.route('/')
def home():
    return render_template('index.html')

#API 역할을 하는 부분
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

@app.route('/schedules', methods=['GET'])
def show_schedule():
    schedules = list(db.schedules.find({},{'_id':0}))
    return jsonify({'result':'success', 'schedules':schedules})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
