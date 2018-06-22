import codecs
import webbrowser
import re

from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask import jsonify, json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import default_comparator

from werkzeug.utils import secure_filename

import os
import pandas as pd
import numpy as np
#from PIL import Image
#import re
import base64
#import io

from datetime import datetime

UPLOAD_FOLDER = 'static/screenshots'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test_key'

db = SQLAlchemy(app)


class Person(db.Model):

    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(30), nullable=False)
    sname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_on' : type,
        'polymorphic_identity' : 'person'
    }

class Patient(Person):


    birth_date = db.Column(db.DateTime,default=None)
    sex = db.Column(db.Boolean)

    __mapper_args__ = {
        'polymorphic_identity':'patient'
    }

    def __repr__(self):
        #return "id {}; name: {}; birth: {}".format(self.id, self.fname, self.birth_date)
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}        

class Doctor(Person):

    clinic = db.Column(db.Integer)
    __mapper_args__ = {
        'polymorphic_identity':'doctor'
    }

    def __repr__(self):
        #return "id {}; name: {}; birth: {}".format(self.id, self.fname, self.clinic)
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    visit_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class BasicTest(db.Model):

    __tablename__ = 'basic_test'

    id = db.Column(db.Integer, primary_key=True)
    visit_id = db.Column(db.Integer, db.ForeignKey('visit.id'), nullable=False)
    screenshot_path = db.Column(db.String(), unique=True, nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity' : 'basic_test',
        'polymorphic_on' : type
    }

    def __repr__(self):
        return 'Id: {0}, screen: {1}, type: {2}, visit_Id: {3}'.format(self.id, self.screenshot_path, self.type, self.visit_id)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.template_filter('screen_path')
def reverse_filter(s):
    #return s.split('\\')[-1]
    return '/' + s.replace('\\','/')

class EDSS(BasicTest):

    __tablename__ = 'Expanded Disability Status Scale (EDSS)'
    
    id = db.Column(db.Integer, db.ForeignKey('basic_test.id'), primary_key=True)
    
    visual = db.Column(db.Float)
    brainstem = db.Column(db.Float)
    pyramidal = db.Column(db.Float)
    cerebellar = db.Column(db.Float)
    sensory = db.Column(db.Float)
    bowel_bladder = db.Column(db.Float)
    cerebral = db.Column(db.Float)
    ambulation_score = db.Column(db.Float)
    edss_step = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity':'Expanded Disability Status Scale (EDSS)',
    }

class FSMC(BasicTest):

    __tablename__ = 'Fatigue Scale for Motor and Cognitive Functions (FSMCF)'
    
    id = db.Column(db.Integer, db.ForeignKey('basic_test.id'), primary_key=True)
    kog = db.Column(db.Integer)
    mot = db.Column(db.Integer)
    total = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity':'Fatigue Scale for Motor and Cognitive Functions (FSMCF)',
    }

class Foot25(BasicTest):

    __tablename__ = '25 Foot'
    
    id = db.Column(db.Integer, db.ForeignKey('basic_test.id'), primary_key=True)
    foot25_try1 = db.Column(db.Float)
    foot25_try2 = db.Column(db.Float)
    foot25_tools = db.Column(db.String)
    foot25_addition = db.Column(db.Text)

    __mapper_args__ = {
        'polymorphic_identity':'25 Foot',
    }

class HADS(BasicTest):

    __tablename__ = 'Hospital Anxiety and Depression Scale (HADS)'
    
    id = db.Column(db.Integer, db.ForeignKey('basic_test.id'), primary_key=True)
    anxiety = db.Column(db.Integer)
    depression = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity':'Hospital Anxiety and Depression Scale (HADS)',
    }

class MemoryTest(BasicTest):

    __tablename__ = 'Symbol Digit Modalities Test  (SDMT)'
    
    id = db.Column(db.Integer, db.ForeignKey('basic_test.id'), primary_key=True)
    memtest_all = db.Column(db.Float)
    memtest_correct = db.Column(db.Float)
    memtest_wrong = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity':'Symbol Digit Modalities Test  (SDMT)',
    }

class SF36(BasicTest):

    __tablename__ = 'SF-36'
    
    id = db.Column(db.Integer, db.ForeignKey('basic_test.id'), primary_key=True)
    PHC = db.Column(db.Integer)
    MHC = db.Column(db.Integer)

    __mapper_args__ = {
        'polymorphic_identity':'SF-36',
    }

class PASAT3(BasicTest):

    __tablename__ = 'PASAT 3'
    
    id = db.Column(db.Integer, db.ForeignKey('basic_test.id'), primary_key=True)
    form_type = db.Column(db.String(5))
    correct = db.Column(db.Integer)
    procent = db.Column(db.Float)

    __mapper_args__ = {
        'polymorphic_identity':'PASAT 3',
    }

class HPT9(BasicTest):

    __tablename__ = 'HPT 9'
    
    id = db.Column(db.Integer, db.ForeignKey('basic_test.id'), primary_key=True)
    main_hand = db.Column(db.String(10))
    attempt_main_hand_1 = db.Column(db.Float)
    attempt_main_hand_2 = db.Column(db.Float)
    note_main = db.Column(db.Text)
    attempt_sec_hand_1 = db.Column(db.Float)
    attempt_sec_hand_2 = db.Column(db.Float)
    note_sec = db.Column(db.Text)


    __mapper_args__ = {
        'polymorphic_identity':'HPT 9',
    }

@app.route('/search_visit', methods=['POST'])
def search_visit():
    if request.method == 'POST':
        print(request.form)
        print(request)
        print (request.is_json)
        content = request.get_json()
        print (content)

        filters = {}

        if content['sname']:
            filters['patient_sname'] = content['sname']
        if content['fname']:
            filters['patient_fname'] = content['fname']
        if content['lname']:
            filters['patient_lname'] = content['lname']

        patients = Visit.query.filter_by(**filters)

        if content['from_date']:
            print(content['from_date'])
            patients = patients.filter(Visit.visit_date >= datetime.strptime(content['from_date'], '%Y-%m-%d'))
        if content['to_date']:
            print(content['to_date'])
            patients = patients.filter(Visit.visit_date <= datetime.strptime(content['to_date'], '%Y-%m-%d'))

        patients = patients.all()

    print(patients)

    print([patient.as_dict() for patient in patients])

    return jsonify([patient.as_dict() for patient in patients])

@app.route('/visit/<visit_id>', methods=['GET','POST'])
def view_tests(visit_id):
    tests = BasicTest.query.filter_by(visit_id = visit_id).all()
    return render_template("tests_view.html", tests = tests)



def check_form(request, template_path):
    if request.method == 'GET':
        OK_FLAG = True
        correct_dict = {}
        if 'sex' not in request.args:
            OK_FLAG = False
            flash('Укажите пол!')
        else:
            correct_dict['sex'] = request.args['sex']
        for key in request.args:
            if request.args[key] == '':
                OK_FLAG = False
                flash('Сперва укажите ' + str(key))
            else:
                correct_dict[key] = request.args[key]
        if OK_FLAG == False:
            return render_template('index.html', **correct_dict)
    return render_template(template_path, **correct_dict)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        correct_dict = {}
        for key in request.form:
            correct_dict[key] = request.form[key]
        return render_template('index.html', **correct_dict)
    return render_template('index.html')

@app.route('/memory_test', methods=['GET'])
def memory_test():
    return check_form(request, 'tests/MemoryTest.html')

@app.route('/hads', methods=['GET'])
def hads():
    return check_form(request, 'tests/HADS.html')

@app.route('/sf36', methods=['GET'])
def sf36():
    return check_form(request, 'tests/sf36.html')

@app.route('/foot25', methods=['GET'])
def foot_25():
    return check_form(request, 'tests/foot25.html')

@app.route('/hpt9', methods=['GET'])
def hpt_9():
    return check_form(request, 'tests/hpt9.html')

@app.route('/passat3', methods=['GET'])
def passat_3():
    return check_form(request, 'tests/passat3.html')

@app.route('/neurostatus', methods=['GET','POST'])
def neurostatus():
    if request.method == 'GET':
        return check_form(request, 'tests/neurostatus.html')

@app.route('/fsmc', methods=['GET'])
def fsmc():
    return check_form(request, 'tests/FSMC.html')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/screen', methods=['POST'])
def screen():
    if request.method == 'POST':
        
        #[print(key) for key in request.form.keys()]

        name_of_test = request.form['name_of_test']
        if name_of_test not in ['fsmc', 'hads', 'memory_test', 'sf-36', '25_foot', '9_hpt', 'pasat_3', 'neurostatus_scoring']:
            print('error')

        print(request.form['birth_date'])
        print(request.form['visit_date'])

        patient = Patient.query.filter_by(fname=request.form['fname'],
                                          sname = request.form['sname'],
                                          lname = request.form['lname'],
                                          birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d')).first()

        if not patient:

            patient = Patient(
                fname=request.form['fname'],
                sname = request.form['sname'],
                lname = request.form['lname'],
                birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d'),
                sex = True if request.form['sex'] == "male" else False,
            )

            db.session.add(patient)
            db.session.commit()

        print("Patient OK", patient)
        print(request.form['clinic'])
        
        doctor = Doctor.query.filter_by(fname=request.form['spec_fname'],
                                        sname = request.form['spec_sname'],
                                        lname = request.form['spec_lname'],
                                        clinic = int(request.form['clinic'])).first()
        
        if not doctor:

            doctor = Doctor(fname=request.form['spec_fname'],
                            sname = request.form['spec_sname'],
                            lname = request.form['spec_lname'],
                            clinic = int(request.form['clinic']))
            
            db.session.add(doctor)
            db.session.commit()
        
        print("Doctor OK", doctor)

        visit = Visit(patient_id = patient.id,
                      doctor_id = doctor.id,
                      visit_date = datetime.strptime(request.form['visit_date'], '%Y-%m-%d'))

        print("Visit OK", visit)

        visit = Visit.query.filter_by(patient_fname = request.form['fname'],
                                 patient_sname = request.form['sname'],
                                 patient_lname = request.form['lname'],
                                 visit_date = datetime.strptime(request.form['visit_date'], '%Y-%m-%d')).first()

        print('from filter: ', visit)

        if not visit:

            visit = Visit(
                patient_fname = request.form['fname'],
                patient_sname = request.form['sname'],
                patient_lname = request.form['lname'],
                visit_date = datetime.strptime(request.form['visit_date'], '%Y-%m-%d'),

                patient_birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d'),
                patient_sex = True,

                doctor_fname = 'A',
                doctor_sname = 'B',
                doctor_lname = 'C',
            )

            print(visit)

            db.session.add(visit)
            db.session.commit()

            print(visit)

        screen_name = '_'.join([str(visit.id), name_of_test, '.png'])
        screen_name = os.path.join(UPLOAD_FOLDER, screen_name)

        screenshot = request.form['screen'].split(',')[1]
        screenshot = base64.b64decode(screenshot)

        with open(screen_name, 'wb') as file:
            file.write(screenshot)

        print(request.form)

        if name_of_test == 'neurostatus_scoring':

            test_summary = EDSS(visit_id = visit.id, 
                                screenshot_path = screen_name,
                                visual = float(request.form['visual']) ,
                                brainstem = float(request.form['brainstem']),
                                pyramidal = float(request.form['pyramidal']),
                                cerebellar = float(request.form['cerebellar']),
                                sensory = float(request.form['sensory']),
                                bowel_bladder = float(request.form['bowel_bladder']),
                                cerebral = float(request.form['cerebral']),
                                ambulation_score = float(request.form['ambulation_score']),
                                edss_step = float(request.form['edss_step']),
                                )
        
        if name_of_test == 'fsmc':

            test_summary = FSMC(visit_id = visit.id, 
                                screenshot_path = screen_name,
                                kog = int(request.form['kog']),
                                mot = int(request.form['mot']),
                                total = int(request.form['total']))
        
        if name_of_test == '25_foot':

            test_summary = Foot25(visit_id = visit.id, 
                                screenshot_path = screen_name,
                                foot25_try1 = float(request.form['foot25_try1']),
                                foot25_try2 = float(request.form['foot25_try1']),
                                foot25_tools = request.form['foot25_tools'],
                                foot25_addition = request.form['foot25_addition'])

        if name_of_test == 'hads':

            test_summary = HADS(visit_id = visit.id, 
                                screenshot_path = screen_name,
                                anxiety = int(request.form['hads_anx']),
                                depression = int(request.form['hads_dep']))

        if name_of_test == 'memory_test':

            test_summary = MemoryTest(visit_id = visit.id, 
                                screenshot_path = screen_name,
                                memtest_all = int(request.form['memtest_all']),
                                memtest_correct = int(request.form['memtest_correct']),
                                memtest_wrong = int(request.form['memtest_wrong']))

        if name_of_test == 'sf-36':

            test_summary = SF36(visit_id = visit.id, 
                                screenshot_path = screen_name,
                                PHC = int(request.form['PHC']),
                                MHC = int(request.form['MHC']))

        if name_of_test == 'pasat_3':

            test_summary = PASAT3(visit_id = visit.id, 
                                screenshot_path = screen_name,
                                form_type = request.form['pasat_form_type'],
                                correct = int(request.form['pasat_correct']),
                                procent = float(request.form['pasat_procent']))
        
        if name_of_test == '9_hpt' :

            test_summary = HPT9(visit_id = visit.id, 
                                screenshot_path = screen_name,
                                main_hand = request.form['hpt9_hand'],
                                attempt_main_hand_1 = float(request.form['hpt9_main_hand_1']),
                                attempt_main_hand_2 = float(request.form['hpt9_main_hand_2']),
                                note_main = request.form['hpt9_note_main'],
                                attempt_sec_hand_1 = float(request.form['hpt9_sec_hand_1']),
                                attempt_sec_hand_2 = float(request.form['hpt9_sec_hand_1']),
                                note_sec = request.form['hpt9_note_sec'])


        db.session.add(test_summary)
        db.session.commit()

        print(test_summary)

    return redirect(url_for('index'))

def main():

    if not 'visits.db' in os.listdir():
        db.create_all()

    url = 'http://localhost:5000/'
    webbrowser.open_new_tab(url)
    app.run(debug=True)

if __name__ == "__main__":
    main()
