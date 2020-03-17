# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 11:14:07 2020

@author: Anh Hoang
"""
#TODO:
# fix some names
# test post and delete METHOD
# set ID to be primary key (I CAN'T YOU JUST HAVE TO REMEMBER THE IDs)
# comments
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
import sqlite3

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
parser = reqparse.RequestParser()


def dict_factory(cursor, row):
    d = {}
    for (idx, col) in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def convert_limit(limit):
    query = 'SELECT Name, COUNT(id) as Total\
            FROM games\
            GROUP BY Name\
            LIMIT ?;'
    conn = sqlite3.connect('game_data.db')
    cur = conn.cursor()
    df = cur.execute(query,(limit,)).fetchall()
    limit_param = 0
    for row in df:
        limit_param += row[1]
    return limit_param


class GameList(Resource):
    def get(self):
        query_params = request.args
        query = "SELECT * FROM games "

        limit = query_params.get('limit')
        
        conn = sqlite3.connect('game_data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
            
        if limit:
            query += "LIMIT ?;"
            result = cur.execute(query, (limit,)).fetchall()
        else:
            query += 'LIMIT 100;'
            result = cur.execute(query).fetchall()
        return jsonify(result)

    def post(self):
        parser.add_argument('ID', 'Name', 'Platform', 'Year_of_Release', 'Genre',
                            'Publisher', 'NA_Sales', 'EU_Sales', 'JP_Sales',
                            'Other_Sales', 'Global_Sales', 'Developer')
        args = parser.parse_args()
        conn = sqlite3.connect('game_data.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO games\
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', args.values())
        conn.commit()
        conn.close()
        return '', 201

    def delete(self):
        item_id = request.args.get('id')
        conn = sqlite3.connect('game_data.db')
        cur = conn.cursor()
        cur.execute('DELETE FROM games WHERE ID = ?;', item_id).fetchall()
        conn.commit()
        conn.close()
        return '', 204


class GameByName(Resource):
    def get(self):
        query_params = request.args
        query = 'SELECT * FROM games WHERE '

        name = query_params.get('name')
        sales = query_params.get('sales')
        after = query_params.get('after')
        limit = query_params.get('limit')

        params_filter = []

        conn = sqlite3.connect('game_data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        if name:
            query += 'name = ? AND'
            params_filter.append(name)
        if sales:
            query += 'Global_Sales > ? AND'
            params_filter.append(sales)
        if after:
            query += 'ID > ? AND'
            params_filter.append(after)
        query = query[:-3]

        if limit:
            query += "LIMIT ?;"
            params_filter.append(limit)
        else:
            query += ';'
        result = cur.execute(query, params_filter).fetchall()

        if len(result) == 0:
            abort(404)
        return jsonify(result)


class SalesList(Resource):
    def get(self):
        query_params = request.args
        query = "SELECT Name, Platform, Global_Sales as Sales\
        FROM games "

        limit = query_params.get('limit')
        conn = sqlite3.connect('game_data.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()

        query += "ORDER BY Name "
        if limit:
            limit = convert_limit(limit)
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


api.add_resource(GameList, '/api/v1/')
api.add_resource(GameByName, '/api/v1/games')
api.add_resource(SalesList, '/api/v1/sales')
api.add_resource(SalesByName, '/api/v1/sales/search')

if __name__ == '__main__':
    app.run(debug=True)