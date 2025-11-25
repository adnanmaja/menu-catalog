from flask import Blueprint, jsonify, current_app, request
from ...database.db import db
from ...models.model import Menu
from ...schemas.menu import MenuResponse, MenuCreate
from pydantic import ValidationError

bp = Blueprint('menu_id', __name__)

@bp.route('/menu/<int:menu_id>', methods=['GET'])
def get_menu_by_id(menu_id):
    try:
        current_app.logger.debug(f"menuid: {menu_id}")
        menu = Menu.query.filter(Menu.id == menu_id).first()

        if not menu:
            return jsonify({'error':'menu gak ditmeukan'}), 404
        
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
        return jsonify({'error': str(e)}), 500
    

@bp.route('/menu/<int:menu_id>', methods=['PUT'])
def update_menu_by_id(menu_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Nggak ada JSON yg diberikan'}), 400

        try: 
            MenuCreate(**data)
        except ValidationError as e:
            return jsonify({'error': e.errors()}), 500

        menu = Menu.query.filter(Menu.id == menu_id).first()

        if not menu:
            return jsonify({'error':'menu gak ditmeukan'}), 404

        menu.name = data.get('name', menu.name)
        menu.category = data.get('category', menu.category)
        menu.calories = data.get('calories', menu.calories)
        menu.price = data.get('price', menu.price)
        menu.ingredients = data.get('ingredients', menu.ingredients)
        menu.description = data.get('description', menu.description)
        
        db.session.commit()
        db.session.refresh(menu)

        response_data = MenuResponse(
            id=menu.id,
            name=menu.name,
            category=menu.category,
            calories=menu.calories,
            price=menu.price,
            ingredients=menu.ingredients,
            description=menu.description
        )

        return jsonify({
            'menu: ': response_data.model_dump(),
            'message': 'Berhasil diupdate'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
@bp.route('/menu/<int:menu_id>', methods=['DELETE'])
def delete_menu_by_id(menu_id):
    try:
        menu = Menu.query.filter(Menu.id == menu_id).first()

        if not menu:
            return jsonify({'error':'menu gak ditmeukan'}), 404

        response_data = MenuResponse(
            id=menu.id,
            name=menu.name,
            category=menu.category,
            calories=menu.calories,
            price=menu.price,
            ingredients=menu.ingredients,
            description=menu.description

        )

        db.session.delete(menu)
        db.session.commit()

        return jsonify({
            'menu: ': response_data.model_dump(),
            'message': 'Berhasil dihapus'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500