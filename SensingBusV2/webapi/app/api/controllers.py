from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
from .services import flushingManager
import logging, json

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
