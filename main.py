# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 11:14:07 2020

@author: Anh Duy Hoang
"""

from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
import json

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

parser = reqparse.RequestParser()
parser.add_argument('name', 'platform', 'year', 'genre', 'publisher', 'NA_sales', 'EU_sales', 'JP_sales', 'other_sales',
                    'global_sales', 'developer')
with open('game_db.json', 'r') as game_data:
    db = json.load(game_data)


# Generate URL to Homepage
# endpoint '/'
@app.route('/', methods=['GET'])
def home():
    return "<h1>Game Sale API</h1>"


# Generate the endpoint to the entire list of games
# endpoint '/api/v1/games/'
class GameList(Resource):
    def get(self):
        args = request.args

        if args.get('limit'):
            limit = int(args.get('limit'))
            return db[:limit]
        else:
            return db[:20]

    def post(self):
        args = parser.parse_args()
        item_id = int(db[-1]['ID']) + 1
        d = {'ID': item_id,
             'Name': args['name'],
             'Platform': args['platform'],
             'Year': args['year'],
             'Genre': args['genre'],
             'Publisher': args['publisher'],
             'NA_Sales': args['NA_sales'],
             'JP_Sales': args['JP_sales'],
             'Other_Sales': args['other_sales'],
             'Global_Sales': args['global_sales'],
             'Developer': args['developer']}
        db.append(d)
        if len(d) != 11:
            abort(400)
        return d, 201


# Generate endpoints to search for specific game and its data
# endpoint '/api/v1/games/search/'
class GameByParams(Resource):
    def get(self, game_id):
        result = [item for item in db if item['ID'] == game_id]
        return result

    def put(self, game_id):
        args = parser.parse_args()
        result = [item for item in db if item['ID'] == game_id][0]
        result['Name'] = args['name']
        result['Platform'] = args['platform']
        result['Year'] = args['year']
        result['Genre'] = args['genre']
        result['Publisher'] = args['publisher']
        result['NA_Sales'] = args['NA_sales']
        result['JP_Sales'] = args['JP_sales']
        result['Other_Sales'] = args['other_sales']
        result['Global_Sales'] = args['global_sales']
        result['Developer'] = args['developer']

        return result, 200

    def delete(self, game_id):
        del db[game_id]
        return '', 204


# Generate endpoints to entire list of games and theirs sales across different platforms (if there's more than one)
# endpoint '/api/v1/sales/'
class SalesList(Resource):
    def get(self):
        args = request.args
        n = 0
        lst = []
        # construct the sales JSON format
        while n < len(db):
            d = {}
            sales_lst = []

            if not db[n]['Name']:
                n += 1
                continue

            d['game'] = db[n]['Name']

            # construct the inner list
            while db[n]['Name'] == d['game']:
                sales_lst.append({'platform': db[n]['Platform'],
                                  'global_sales': db[n]['Global_Sales']})
                n += 1
                if n == len(db):
                    break

            d['sales'] = sales_lst
            lst.append(d)
        if args.get('limit'):
            limit = int(args.get('limit'))
            return lst[:limit]
        return lst[:20]


# Generate endpoints to search for specific game with its sales across different platforms
# endpoint '/api/v1/sales/search/'
class SalesByName(Resource):
    def get(self):
        args = request.args
        name = args.get('name')

        result = [db[n] for n in range(len(db)) if db[n]['Name'] == name]
        d = {'game': name}
        sales_lst = []
        for item in result:
            sales_lst.append({'platform': item['Platform'],
                              'global_sales': item['Global_Sales']})
        d['sales'] = sales_lst
        if not name:
            abort(404)
        return d


api.add_resource(GameList, '/api/v1/games/')
api.add_resource(GameByParams, '/api/v1/games/<int:game_id>')
api.add_resource(SalesList, '/api/v1/sales/')
api.add_resource(SalesByName, '/api/v1/sales/search')

if __name__ == '__main__':
    app.run(debug=True)