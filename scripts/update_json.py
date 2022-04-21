import json
from flask import request, jsonify


# Load the File
def load_data():
    with open('./scripts/db.json') as f:
        return json.load(f)


class Notes:
    def __init__(self) -> None:
        self.file_data = load_data()

    # Save the file with new data
    def save_data(self, file_data):
        with open('./scripts/db.json', 'w') as f:
            json.dump(file_data, f, indent=4)

    # Read an Item from file
    def get_note_or_index(self, note_id, return_index=False, return_note=False):
        for idx, note in enumerate(self.file_data):
            if note['id'] == note_id:
                if return_index and return_note:
                    return idx, note
                elif return_note:
                    # note_json = []
                    # note_json.append(note)
                    return jsonify(note)
                return idx

    # Create New Item and save it into file
    def insert_one_note(self):
        note = request.get_json()
        if len(self.file_data) > 0:
            new_id = int(
                (max(self.file_data, key=lambda x: x['id'])['id'])) + 1
        else:
            new_id = 1
        updated = note['updated'][:19].replace('T', ' ')
        new_note = {"id": new_id,
                    "body": note['body'],
                    "updated": updated}
        self.file_data.append(new_note)
        self.save_data(self.file_data)
        return 'Done'

    # Delete One Item from Json
    def delete_one_note(self, note_id):
        idx = self.get_note_or_index(note_id=note_id, return_index=True)
        del self.file_data[idx]
        self.save_data(self.file_data)
        return 'Done'

    # Update One Item from JSON
    def update_one_note(self, note_id):
        note = request.get_json()
        idx = self.get_note_or_index(note_id=note_id, return_index=True)
        self.file_data[idx]["body"] = note['body']
        self.file_data[idx]["updated"] = note['updated'][:19].replace('T', ' ')
        self.save_data(self.file_data)
        return 'Done'

    def get_all_notes(self):
        return jsonify(self.file_data)
