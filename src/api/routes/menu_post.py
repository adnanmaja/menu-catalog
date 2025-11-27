from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from ...database.db import db
from ...models.model import Menu
from ...schemas.menu import MenuResponse, MenuCreate
from ...services.gemini import Gemini
from google.genai import errors

bp = Blueprint('menu', __name__)

@bp.route("/menu", methods=['POST'])
def create_menu():
    try: 

        ai_description = request.args.get('ai_description', 'false').strip()
        ai_category = request.args.get('ai_category', 'false').strip()

        data = request.get_json()
        if not data:
            return jsonify({'error': 'Nggak ada JSON yg diberikan'}), 400
        
        try: 
            menu_data = MenuCreate(**data)
        except ValidationError as e:
            return jsonify({'error': e.errors()}), 400 # kalo description sama category kosong gpp, yang penting string

        if Menu.query.filter_by(name=menu_data.name).first():
            return jsonify({'error': 'Menu sudah ada'}), 400
        
        # gemini generated description
        gemini = Gemini()
        if ai_description or menu_data.description is None:
            print(f"ai_desc called: {menu_data.description}")
            try: 
                menu_data.description = gemini.generate_menu_description(menu=menu_data)
                print(menu_data.description)
            except errors.APIError as e:
                return jsonify({'Gemini API error': e.message}), e.code
            
        # gemini generated category
        if ai_category or menu_data.category is None:
            print(f"ai_cat called: {menu_data.category}")
            try:
                menu_data.category = gemini.generate_category(menu=menu_data)
                print(menu_data.category)
            except errors.APIError as e:
                return jsonify({'Gemini API error': e.message}), e.code

        new_menu = Menu(
            name=menu_data.name,
            category=menu_data.category,
            calories=menu_data.calories,
            price=menu_data.price,
            ingredients=menu_data.ingredients,
            description=menu_data.description
        )

        db.session.add(new_menu)
        db.session.commit()

        response_data = MenuResponse(
            id=new_menu.id,
            name=new_menu.name,
            category=new_menu.category,
            calories=new_menu.calories,
            price=new_menu.price,
            ingredients=new_menu.ingredients,
            description=new_menu.description
        )
        

        return jsonify({
            'message': 'berhasil dibuat!!',
            'menu': response_data.model_dump()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    