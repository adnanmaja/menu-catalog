from flask import Blueprint, jsonify, current_app, request
from ...database.db import db
from ...models.model import Menu
from ...schemas.menu import MenuResponse, MenuCreate
from ...services.gemini import Gemini
from ...services.json_to_sql import json_to_sql
from ...services.request_parser import parse_filters
import json
from google.genai import errors

bp = Blueprint('smart_search', __name__)
gemini = Gemini()

@bp.route('/menu/smart', methods=['GET'])
def menu_smart_search(): 
    try:
        filters = parse_filters(request)

        try:
            response_text = gemini.natural_language_query(query=filters['user_query'])
        except errors.APIError as e:
            return jsonify({'Gemini API error': e.message}), e.code
        
        response_json = response_text.replace('```json', '').replace('```', '').strip()
        try:
            filters = json.loads(response_json)
        except json.JSONDecodeError as e:
            return jsonify({'error': str(e)})

        print(filters)

        query = json_to_sql(Menu=Menu, filters=filters)
        menus = query.all()
        print('QUERY MENU PASSEDDDD ')
        print(f'query: {query}')
        print(f"menu: {menus}")

        if not menus:
            return jsonify({'message': 'Menu tidak ditemukan'}), 404

        response_data = []
        for menu in menus:
            item_data = {
                'id': menu.id,
                'name': menu.name,
                'category': menu.category,
                'calories': menu.calories,
                'price': menu.price,
                'ingredients': menu.ingredients,
                'description': menu.description
            }
            response_data.append(item_data)

        return jsonify(response_data), 200
    
    except Exception as e:
        return jsonify({'e': str(e)}), 400