import json
from datetime import datetime
import ijson

# Fill Data collection
import configuration
configuration.init()

# Fill Total Load collection
def fill_data():

    count = 0
    batch = configuration.db.batch()
    with open('./data_files/ActualTotalLoad_202111241118.json') as f:
        data = ijson.items(f, 'ActualTotalLoad.item')

        for x in data:
            if x['Id'] > 249832583:

                doc_ref = configuration.db.collection('total_load_data').document(str(x['Id']))
                count += 1

                # Refactor datetime from str to date-objects
                datetime_keys = ['EntityCreatedAt', 'EntityModifiedAt', 'DateTime', 'UpdateTime']
                for key in datetime_keys:
                    if key in x.keys():
                        x[key] = datetime.strptime(x[key], "%Y-%m-%d %H:%M:%S")

                x['TotalLoadValue'] = float(x['TotalLoadValue'])

                if count % 500 == 0:
                    batch.commit()
                    print(count)
                    batch = configuration.db.batch()
                else:
                    batch.set(doc_ref, x)

                # Add to firestore
                #configuration.db.collection('total_load_data').document(str(x['Id'])).set(x)

# Fill Resolution Codes collection
def fill_codes():

    # Read JSON file
    with open('data_files/ResolutionCode_202111071645.json') as f:
        resolution_codes = json.load(f)['ResolutionCode']

    for code in resolution_codes:

        # Refactor datetime from str to date-objects
        code['EntityCreatedAt'] = datetime.strptime(code['EntityCreatedAt'], "%Y-%m-%d %H:%M:%S")
        code['EntityModifiedAt'] = datetime.strptime(code['EntityModifiedAt'], "%Y-%m-%d %H:%M:%S")

        # Add to firestore
        configuration.db.collection('resolution_codes').document(str(code['Id'])).set(code)

# Fill Reference Zones collection
def fill_zones():

    # Read JSON file
    with open('data_files/entsoeAreaRef_202111071647.json') as f:
        reference_zones = json.load(f)['entsoeAreaRef']

    for zone in reference_zones:
        print(zone['Id'])
        # Refactor datetime from str to date-objects
        zone['AreaRefAddedOn'] = datetime.strptime(zone['AreaRefAddedOn'][:-3], "%Y-%m-%d %H:%M:%S.%f")

        # Add to firestore
        configuration.db.collection('reference_zones').document(str(zone['Id'])).set(zone)

fill_data()
