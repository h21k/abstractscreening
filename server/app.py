from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

DEBUG = True

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(__name__)

CORS(app, resources={r'/.*': {'origins': '*'}})

COURSES = [
    {
        'id': uuid.uuid4().hex,
        'ReviewID': '0001',
        'PubmedID': '33461210',
        'title': 'Effective JavaScript: 68 Specific Ways to Harness the Power of JavaScript ',
        'abstract': 'Senolysis by glutaminolysis inhibition ameliorates various age-associated disorders',
        'ToBeScreened': True,
        'Inclusion': True,
        'NValue': '46.99'
    },
    {
        'id': uuid.uuid4().hex,
        'ReviewID': '0002',
        'PubmedID': '02470038',
        'title': 'JavaScript: The Good Parts ',
        'abstract': 'Death from stroke has decreased over the past decade, with stroke now the fifth leading cause of death in the United States',
        'ToBeScreened': False,
        'Inclusion': False,
        'NValue': '821.30'
    },
    {
        'id': uuid.uuid4().hex,
        'ReviewID': '0003',
        'PubmedID': '10630539',
        'title': 'Eloquent JavaScript: A Modern Introduction to Programming ',
        'abstract': 'According to the World Health Organization, stroke is the incoming epidemic of the 21st century',
        'ToBeScreened': False,
        'Inclusion': True,
        'NValue': '12.00'
    }
]

@app.route('/courses', methods=['GET', 'POST'])
def all_courses():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        COURSES.append({
            'id': uuid.uuid4().hex,
            'ReviewID': post_data.get('ReviewID'),
            'PubmedID': post_data.get('PubmedID'),
            'title': post_data.get('title'),
            'abstract': post_data.get('abstract'),
            'ToBeScreened': post_data.get('ToBeScreened'),
            'Inclusion': post_data.get('Inclusion'),
            'NValue': post_data.get('NValue')
        })
        response_object['message'] = 'Review added!'
    else:
        response_object['courses'] = COURSES
    return jsonify(response_object)

@app.route('/courses/<course_id>', methods=['GET', 'PUT', 'DELETE'])
def single_course(course_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        return_course = ''
        for course in COURSES:
            if course['id'] == course_id:
                return_course = course
        response_object['course'] = return_course
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_course(course_id)
        COURSES.append({
            'id': uuid.uuid4().hex,
            'ReviewID': post_data.get('ReviewID'),
            'PubmedID': post_data.get('PubmedID'),
            'title': post_data.get('title'),
            'abstract': post_data.get('abstract'),
            'ToBeScreened': post_data.get('ToBeScreened'),
            'Inclusion': post_data.get('Inclusion'),
            'NValue': post_data.get('NValue')
        })
        response_object['message'] = 'Review updated!'
    if request.method == 'DELETE':
        remove_course(course_id)
        response_object['message'] = 'Review removed!'
    return jsonify(response_object)

def remove_course(course_id):
    for course in COURSES:
        if course['id'] == course_id:
            COURSES.remove(course)
            return True
    return False

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
