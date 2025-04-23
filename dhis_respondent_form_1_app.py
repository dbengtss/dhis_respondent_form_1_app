from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# dhis config
DHIS2_BASE_URL = os.getenv("DHIS2_BASE_URL")
DHIS2_USERNAME = os.getenv("DHIS2_USERNAME")
DHIS2_PASSWORD = os.getenv("DHIS2_PASSWORD")
TRACKED_ENTITY_TYPE = os.getenv("TRACKED_ENTITY_TYPE")
ORG_UNIT_ID = os.getenv("ORG_UNIT_ID")

# consider using base orgunit for all

# att ids found in mnt > trck etity att > eplis far r > id & api

ATTRIBUTE_IDS = {
    "name": "att_id",
    "email": "att_id",
    "carpha_training": "att_id",
    "role": "att_id",
    "diseases": "att_id",
    "certifications": "att_id",
    "status": "att_id",
    "notice": "att_id",
    "language": "att_id",
    "education_level": "att_id",
}

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form

    # transform data into dhis2 tracker format
    attributes = []
    for key, attr_id in ATTRIBUTE_IDS.items():
        if key in data:
            attributes.append({
                "attribute": attr_id,
                "value": data[key]
            })

    payload = {
        "trackedEntityType": TRACKED_ENTITY_TYPE,
        "orgUnit": ORG_UNIT_ID,
        "attributes": attributes,
        "coordinates": {
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }
    }

    # Post to DHIS2
    response = requests.post(
        f"{DHIS2_BASE_URL}/api/trackedEntityInstances",
        json=payload,
        auth=(DHIS2_USERNAME, DHIS2_PASSWORD)
    )

    if response.status_code in [200, 201]:
        return jsonify({"status": "success", "dhis2_response": response.json()}), 201
    else:
        return jsonify({"status": "error", "message": response.text}), 400


if __name__ == '__main__':
    app.run(debug=True)