from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash, secure_filename
from .services import flushingManager
import logging, json, os, config

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/sensingData", methods=['POST'])
def sensing():
	sensingData = request.form.to_dict()
	data = flushingManager.preProcessing(sensingData)
	if(data['status'] == 'ok'):
		logging.info(data['msg'])
		return jsonify(data), 200
	else:
		logging.error(data['msg'])
		return jsonify(data), 500

@api.route("/uploadModules", methods=['POST'])
def uploadModules():
	moduleFile = request.files['file']
	filename = secure_filename(moduleFile.filename)
	moduleFile.save(os.path.join(config.UPLOAD_PATH, filename))
	return jsonify({'oi':'test'})
	'''data = flushingManager.preProcessing(sensingData)
	if(data['status'] == 'ok'):
		logging.info(data['msg'])
		return jsonify(data), 200
	else:
		logging.error(data['msg'])
		return jsonify(data), 500'''