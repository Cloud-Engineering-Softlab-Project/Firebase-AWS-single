from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk.core import xray_recorder, patch_all

import configuration
app = configuration.init()

from resources.energy_data import EnergyData

configuration.api.add_resource(EnergyData, '/energy_data')

xray_recorder.configure(service='Energy APIs')

# Instrument the Flask application
XRayMiddleware(app, xray_recorder)

patch_all()


# We only need this for local development.
#if __name__ == '__main__':
#    configuration.app.run(debug=True)
