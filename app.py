from flask import Flask
from config import load_config
import logging
import iotb

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

config = load_config('config.yaml')
print(config)

iotb.configure()

from routes import register_blueprints
register_blueprints(app)

iotb.client.request("GET", "service")

if __name__ == '__main__':
    app.run()
