from flask import request, jsonify
from flask_restx import Resource, fields, abort

import configuration

class HardSleep(Resource):

    @configuration.measure_time
    def get(self, sleep_id):

        # Initialize global times keeper
        configuration.times = {}

        a = 0
        for i in range(3000):
            for j in range(10000):
                a += i * j

        return {
            'times': configuration.times,
            'msg': sleep_id
        }

class SoftSleep(Resource):

    @configuration.measure_time
    def get(self, sleep_id):

        # Initialize global times keeper
        configuration.times = {}

        a = 0
        for i in range(1000):
            for j in range(10000):
                a += i * j

        return {
            'times': configuration.times,
            'msg': sleep_id
        }