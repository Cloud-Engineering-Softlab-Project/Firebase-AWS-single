from firebase_admin import credentials, firestore, initialize_app
from flask import Flask
from flask_restx import Api
import json
import time
import boto3

global db, app, api, times

def measure_time(func):
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        times[func.__name__] = end - start

        return result

    return wrap

def init():

    global times
    times = {}

    # Read ServiceAccount.json from S3
    s3 = boto3.resource('s3', 'eu-west-3')
    json_object = s3.Object('softlab-cloud-credentials', 'cloud-engineering-974ea-firebase-adminsdk-p2jkd-d073c8db95.json').get()['Body'].read().decode('utf-8')
    json_content = json.loads(json_object)

    # Initialize firestore
    global db
    cred = credentials.Certificate(json_content)
    initialize_app(cred)
    db = firestore.client()

    # Initialize Flask App
    global app, api
    app = Flask(__name__)
    api = Api(app=app, version="1.0", title="Softlab-Project APIs")

    return app
