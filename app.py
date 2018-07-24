import codecs
import webbrowser
import re

from flask import Flask, send_file
from flask import render_template, request, redirect, url_for, flash
from flask import jsonify, json

from werkzeug.utils import secure_filename

import os
import pandas as pd
import numpy as np
from io import BytesIO

#from PIL import Image
#import re
import base64
#import io

from datetime import datetime

UPLOAD_FOLDER = 'static/screenshots'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

from models import app
from models import db
from models import Person, Patient, Doctor, Visit
from models import BasicTest, EDSS, FSMC, Foot25, HADS, MemoryTest, SF36, PASAT3, HPT9

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'test_key'

def visit_to_json(objects):

    result = []
    for obj in objects:
        visit_dict = obj.__dict__.copy()
        patient_dict = Patient.query.get(visit_dict['patient_id']).__dict__.copy()
        doctor_dict = Doctor.query.get(visit_dict['doctor_id']).__dict__.copy()

        for key in set([*visit_dict.keys(), *patient_dict.keys(), *doctor_dict.keys()]):
            if key in ["_sa_instance_state"]:
                for _dict in [visit_dict, patient_dict, doctor_dict]:
                    _dict.pop(key, None)
        result.append((visit_dict, patient_dict, doctor_dict))
    
    print(result)
    return jsonify(result)

@app.template_filter('screen_path')
def reverse_filter(s):
    #return s.split('\\')[-1]
    return '/' + s.replace('\\','/')

@app.route('/search_visit', methods=['POST'])
def search_visit():
    if request.method == 'POST':
        #print(request.form)
        #print(request)
        #print (request.is_json)
        content = request.get_json()
        #print (content)

        filters = {}

        if content['sname']:
            filters['sname'] = content['sname']
        if content['fname']:
            filters['fname'] = content['fname']
        if content['lname']:
            filters['lname'] = content['lname']

        #patients_id = Patient.query.filter_by(**filters).with_entities(Patient.id).all()
        patients = Patient.query.filter_by(**filters).all() #db.session.query(Patient.id).all()
        #print(patients)

        patients_id = list(map(lambda patient: patient.id, patients))
        #print(patients_id)

        #visits = Visit.query.filter(Visit.patient_id in patients_id).all()
        visits = db.session.query(Visit).filter(Visit.patient_id.in_(patients_id)) #.all()
        #print(visits)
        
        if content['from_date']:
            #print(content['from_date'])
            visits = visits.filter(Visit.visit_date >= datetime.strptime(content['from_date'], '%Y-%m-%d'))
        #print(visits.all())
        if content['to_date']:
            #print(content['to_date'])
            visits = visits.filter(Visit.visit_date <= datetime.strptime(content['to_date'], '%Y-%m-%d'))

    visits = visits.all()
    return visit_to_json(visits)

@app.route('/visit/<visit_id>', methods=['GET','POST'])
def visit_view(visit_id):
    tests = BasicTest.query.filter_by(visit_id = visit_id).all()
    print(tests)
    return render_template("visit_view.html", tests = tests)

@app.route('/patient/<patient_id>', methods=['GET','POST'])
def patient_view(patient_id):
    patient = Patient.query.get(patient_id)
    visits = Visit.query.filter_by(patient_id = patient_id).all()
    visit_tests = []
    for visit in visits:
        tests = []
        tests.append(visit)
        tests.append(BasicTest.query.filter_by(visit_id = visit.id).all())
        visit_tests.append(tests)
    print(visit_tests)
    return render_template("patient_view.html", visit_tests = visit_tests, patient = patient)

@app.route('/to_excel', methods=['GET','POST'])
def to_excel():
    if request.method == 'POST':

        tests = BasicTest.query.filter_by( type = request.form["type"]).filter(BasicTest.visit_id.in_(request.form["visits"])).all()
        print(request.form)

        results = []

        for test in tests:
            print(test)
            print(Visit.query.get(test.visit_id).visit_date)
            date = {"visit_date" : Visit.query.get(test.visit_id).visit_date.strftime('%d.%m.%Y')}
            test = test.as_dict()
            test.update(date)
            results.append(test)

        df = pd.DataFrame.from_dict(results)
        df = df.set_index("id")
        print(df)

        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.close()
        output.seek(0)

        return send_file(output, attachment_filename="export.xlsx", as_attachment=True)

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
            print("Patient Created")
        else:
            print("Patient Existed")
        
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
            print("Doctor Created")
        else:
            print("Doctor Existed")

        visit = Visit.query.filter_by(patient_id = patient.id,
                                       doctor_id = doctor.id,
                                       visit_date = datetime.strptime(request.form['visit_date'], '%Y-%m-%d')).first()

        if not visit:

            visit = Visit(patient_id = patient.id,
                          doctor_id = doctor.id,
                          visit_date = datetime.strptime(request.form['visit_date'], '%Y-%m-%d'))

            db.session.add(visit)
            db.session.commit()
            print("Visit Created")
        else:
            print("Visit Existed")

        screen_name = '_'.join([str(visit.id), name_of_test]) + '.png'
        screen_name = os.path.join(UPLOAD_FOLDER, screen_name)

        screenshot = request.form['screen'].split(',')[1]
        screenshot = base64.b64decode(screenshot)

        with open(screen_name, 'wb') as file:
            file.write(screenshot)

        print(name_of_test)

        test_summary = None
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
                                PHC = float(request.form['PHC']),
                                MHC = float(request.form['MHC']))

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

        try:
            assert test_summary
            db.session.add(test_summary)
            db.session.commit()
        except AssertionError:
            print('No information about test results')

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
