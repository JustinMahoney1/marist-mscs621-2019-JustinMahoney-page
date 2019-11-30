#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

groceries = [
    {
        'id': 1,
        'name': u'Milk',
        'description': u'Whole Milk', 
        'amount': u'1 Gallon'
    },
    {
        'id': 2,
        'name': u'Eggs',
        'description': u'Extra-Large', 
        'amount': u'2 Dozen'
    }
]

@app.route('/todo/api/v1.0/groceries', methods=['GET'])
def get_groceries():
    return jsonify({'groceries': groceries})


@app.route('/todo/api/v1.0/groceries/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = [item for item in groceries if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    return jsonify({'item': item[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/groceries', methods=['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        abort(400)
    item = {
        'id': groceries[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
	#'description':request.json['description'],
        'amount': request.json.get('amount',"")
    }
    groceries.append(item)
    return jsonify({'item': item}), 201

@app.route('/todo/api/v1.0/groceries/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = [item for item in groceries if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'amount' in request.json and type(request.json['amount']) is not unicode:
        abort(400)
    item[0]['name'] = request.json.get('name', item[0]['name'])
    item[0]['description'] = request.json.get('description', item[0]['description'])
    item[0]['amount'] = request.json.get('amount', item[0]['amount'])
    return jsonify({'item': item[0]})

@app.route('/todo/api/v1.0/groceries/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = [item for item in groceries if item['id'] == item_id]
    if len(item) == 0:
        abort(404)
    groceries.remove(item[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
