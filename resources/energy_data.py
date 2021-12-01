from flask import request, jsonify
from flask_restx import Resource, fields, abort

import configuration
from modules import firestore

class EnergyData(Resource):

    @configuration.measure_time
    def post(self):

        # Get parameters
        payload = request.json
        zone_codes = payload['zone_codes']
        date_from = payload['date_from']
        duration = payload['duration']

        # Get data
        data = firestore.query_energy_data(zone_codes, date_from, duration, payload['join'], payload['light'])

        # Make them JSON serializable
        for i in range(len(data)):
            doc = data[i]

            # Refactor datetime from str to date-objects
            datetime_keys = ['EntityCreatedAt', 'EntityModifiedAt', 'DateTime', 'UpdateTime']
            for key in datetime_keys:
                if key in doc.keys():
                    data[i][key] = str(doc[key])

            if payload['join']:
                data[i]['ReferenceZoneInfo']['AreaRefAddedOn'] = str(doc['ReferenceZoneInfo']['AreaRefAddedOn'])
                data[i]['ResolutionCodeInfo']['EntityCreatedAt'] = str(doc['ResolutionCodeInfo']['EntityCreatedAt'])
                data[i]['ResolutionCodeInfo']['EntityModifiedAt'] = str(doc['ResolutionCodeInfo']['EntityModifiedAt'])

        return {
            'times': configuration.times,
            'parameters': payload,
            'len_of_data': len(data),
            'data': data
        }
