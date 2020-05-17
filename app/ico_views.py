from flask import Blueprint, current_app


ico = Blueprint('ico', __name__)

@ico.route('/favicon.ico', methods=['GET'])
def get_fav():
    return current_app.send_static_file('ico/favicon.ico')