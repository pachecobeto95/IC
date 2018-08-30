from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug import check_password_hash, generate_password_hash
import logging


api = Blueprint("api", __name__, url_prefix="/api")

