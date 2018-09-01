from flask import Flask, render_template
from app.api.controllers import api
from logging.handlers import TimedRotatingFileHandler
import config, logging



app = Flask(__name__, static_folder="static")
app.config.from_object("config")
app.config['JSON_AS_ASCII'] = False

app.register_blueprint(api)

logging.basicConfig(level=config.log_level, format=config.log_formatter)
handler = TimedRotatingFileHandler(config.log_file,when="midnight")
handler.suffix = config.log_file_suffix
formatter = logging.Formatter(config.log_formatter)
handler .setFormatter(formatter)
logging.getLogger().addHandler(handler)