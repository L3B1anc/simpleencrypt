from flask import request, Flask, jsonify
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/test', methods=['POST'])
def post_Data():
    payload = json.loads(request.data)
    return jsonify(payload), 201


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8888)