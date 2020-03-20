# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 11:14:07 2020

@author: Anh Hoang
"""
#TODO:
# fix some names
# test post and delete METHOD
# comments
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
import sqlite3

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
parser = reqparse.RequestParser()


# Change SQL output (tuple -> dictionary)
def dict_factory(cursor, row):
    d = {}
    for (idx, col) in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Convert limit parameter from the URL to SQL limit
# Used for constructing the /api/v1/sales endpoint
# PARAMS:
#           @limit: limit parameter from the URL
def convert_limit(limit):
    query = 'SELECT Name, COUNT(id)\
            FROM games\
            GROUP BY Name\
            LIMIT ?;'
    conn = sqlite3.connect('game_data.db')
    cur = conn.cursor()
    df = cur.execute(query, (limit,)).fetchall()

    limit_param = 0
    for row in df:
        limit_param += row[1]  # the usable limit param is the sum the COUNT(id) column

    conn.commit()
    conn.close()

    return limit_param


# Generate URL to Homepage
# endpoint '/'
class HomePage(Resource):
    def get(self):
        return "<h1>Game Sale Api<h1>"


# Generate the endpoint to the entire list of games
# endpoint '/api/v1/games/'
class GameList(Resource):
    def get(self):
        query_params = request.args
        query = 'SELECT * FROM games '

        after = query_params.get('after')
        limit = query_params.get('limit')
        query_params = []

        conn = sqlite3.connect('game_data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()

        if after:
            query += 'WHERE ID > ? '
            query_params.append(after)
        if limit:
            query += 'LIMIT ?;'
            query_params.append(limit)
            result = cur.execute(query, query_params).fetchall()
        else:
            query += 'LIMIT 100;'
            result = cur.execute(query, query_params).fetchall()
        return jsonify(result)

    def post(self):
        parser.add_argument('ID', 'Name', 'Platform', 'Year_of_Release', 'Genre',
                            'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales',
                            'Other_Sales', 'Global_Sales', 'Developer')
        args = parser.parse_args()
        conn = sqlite3.connect('game_data.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO games\
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?);', args.values())
        conn.commit()
        conn.close()
        return '', 201

    def delete(self):
        query_params = request.args
        item_id = query_params.get('id')

        conn = sqlite3.connect('game_data.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM games WHERE ID = ?;', (item_id,))
        result = cur.execute('SELECT * FROM games WHERE ID = ?;', (item_id,)).fetchall()
        conn.commit()
        conn.close()
        if len(result) == 0:
            return 'Deleted', 204
        else:
            return 'Unable to Delete', 422


# Generate endpoints to search for specific game and its data
# endpoint '/api/v1/games/search/'
class GameByParams(Resource):
    def get(self):
        query_params = request.args
        query = 'SELECT * FROM games WHERE '

        name = query_params.get('name')
        sales = query_params.get('sales')
        item_id = query_params.get('id')

        conn = sqlite3.connect('game_data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()

        params_filter = []

        if name:
            query += 'name = ? AND'
            params_filter.append(name)
        if sales:
            query += 'Global_Sales > ? AND'
            params_filter.append(sales)
        if item_id:
            query += 'ID = ? AND'
            params_filter.append(item_id)
        query = query[:-3] + ';'
        result = cur.execute(query, params_filter).fetchall()

        if len(result) == 0:
            abort(404)
        return jsonify(result)


# Generate endpoints to entire list of games and theirs sales across different platforms (if there's more than one)
# endpoint '/api/v1/sales/'
class SalesList(Resource):
    def get(self):
        query_params = request.args
        query = "SELECT Name, Platform, Global_Sales as Sales\
        FROM games "

        limit = convert_limit(query_params.get('limit'))
        conn = sqlite3.connect('game_data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()

        query += "ORDER BY Name "
        if limit:
            query += "LIMIT ?;"
        else:
            query += "LIMIT 100;"
            
        result = cur.execute(query, (limit,)).fetchall()
        arr = []
        
        n = 0
        while n < len(result):
            dict_1 = {}
            plat_sale_arr = []
            if not result[n]['Name']:
                n += 1
                continue
            dict_1['game'] = result[n]['Name']
            while result[n]['Name'] == dict_1['game']:
                del result[n]['Name']
                plat_sale_arr.append(result[n])
                n += 1
                if n == len(result):
                    break
            dict_1['sales'] = list({v['Platform']: v for v in plat_sale_arr}.values())
            arr.append(dict_1)

        return jsonify(arr)


# Generate endpoints to search for specific game with its sales across different platforms
# endpoint '/api/v1/sales/search/'
class SalesByName(Resource):
    def get(self):
        query_params = request.args
        query = "SELECT Name, Platform, Global_Sales as Sales\
        FROM games WHERE Name = ?;"
        name = query_params.get('name')

        conn = sqlite3.connect('game_data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()

        result = cur.execute(query, (name,)).fetchall()
        if len(result) == 0:
            abort(404)

        d = {'game': name, 'sales': []}
        for item in result:
            del item['Name']
            d['sales'].append(item)

        return jsonify(d)


api.add_resource(HomePage, '/')
api.add_resource(GameList, '/api/v1/games')
api.add_resource(GameByParams, '/api/v1/games/search')
api.add_resource(SalesList, '/api/v1/sales')
api.add_resource(SalesByName, '/api/v1/sales/search')

if __name__ == '__main__':
    app.run()