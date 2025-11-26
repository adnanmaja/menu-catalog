from flask import Blueprint, jsonify, current_app, request
from ...database.db import db
from ...models.model import Menu
from sqlalchemy import func
from itertools import groupby
from operator import attrgetter

bp = Blueprint('menu_group', __name__)

@bp.route('/menu/group-by-category', methods=['GET'])
def menu_group_by_category():
    try: 
        mode = request.args.get('mode', 'list').strip().lower()
        per_category = request.args.get('per_category', '5').strip().lower()

        if mode == 'count':
            results = (
                Menu.query.with_entities(
                    Menu.category,
                    func.count(Menu.id).label('count')
                ).group_by(Menu.category).all()
            )

            response_data = [
                {'category':category, 'count': count}
                for category, count, in results
            ]

        if mode == 'list':
            results = Menu.query.order_by(Menu.category).all()

            response_data = []
            for category, items in groupby(results, key=attrgetter('category')):
                items_list = list(items)
                try:
                    limit = int(per_category)
                    items_list = items_list[:limit]
                except ValueError:
                    pass
                    
                response_data.append({
                    'category': category,
                    'list': [item.name for item in items_list]
                })
        
        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

    
