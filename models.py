from datetime import datetime

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import default_comparator

import os

app = Flask(__name__, root_path=os.getcwd())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app, session_options={"expire_on_commit" : False}) // allows to call __dict__ without refresh
db = SQLAlchemy(app)

class Person(db.Model):

    __tablename__ = 'person'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    sname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_on' : type,
        'polymorphic_identity' : 'person'
    }

    def as_dict(self):
        return self.__dict__

class Patient(Person):

    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    birth_date = db.Column(db.DateTime,default=None, nullable=False)
    sex = db.Column(db.Boolean, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity':'patient'
    }


class Doctor(Person):

    id = db.Column(db.Integer, db.ForeignKey('person.id'), primary_key=True)
    clinic = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity':'doctor'
    }

class Visit(db.Model):

    __tablename__ = 'visit'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
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
    PHC = db.Column(db.Float)
    MHC = db.Column(db.Float)

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
