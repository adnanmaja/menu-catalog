from flask import Blueprint, jsonify, current_app, request
from ...database.db import db
from ...models.model import Menu
from ...schemas.menu import MenuResponse

bp = Blueprint('menu_search', __name__)

@bp.route("/menu/search", methods=['GET'])
def menu_search():
    try:
        search = request.args.get('q', '').lower()
        print(f'search: {search}')

        menu = Menu.query.filter(Menu.name.ilike(f'{search}')).first()

        if not menu:
            print("BEREHNEIITTIIIIII!!!")
            return jsonify({'message': 'Menu yang dicari ga ada'}), 404

        print(menu.name)
        response_data = MenuResponse(
            id=menu.id,
            name=menu.name,
            category=menu.category,
            calories=menu.calories,
            price=menu.price,
            ingredients=menu.ingredients,
            description=menu.description

        )

        return jsonify(response_data.model_dump()), 200 
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400