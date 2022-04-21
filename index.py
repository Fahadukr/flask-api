from flask import Flask, request
from flask_cors import CORS
import traceback
import sys
from datetime import datetime
from scripts.update_json import Notes

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False


@app.route('/')
def hello():
    return 'Flask API success build'


@app.route('/notes/<note>', methods=['POST', 'PUT', 'GET', 'DELETE'])
def notes(note):
    note_api = Notes()
    try:
        if request.method == 'GET' and note == 'all':
            return note_api.get_all_notes()
        elif request.method == 'GET':
            return note_api.get_note_or_index(note_id=int(note), return_note=True)
        elif request.method == 'PUT':
            return note_api.update_one_note(note_id=int(note))
        elif request.method == 'POST':
            return note_api.insert_one_note()
        elif request.method == 'DELETE':
            return note_api.delete_one_note(int(note))
        else:
            return "Method not allowed"

    except Exception:
        logger = open("log.txt", "a")
        logger.write(f' \n \n DATE: {datetime.now().replace(microsecond=0)}: ---  ERROR in Flask API  ---')
        e_type, e_val, e_tb = sys.exc_info()
        traceback.print_exception(e_type, e_val, e_tb, file=logger)
        logger.close()
        return '---  ERROR in Flask API  ---'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
