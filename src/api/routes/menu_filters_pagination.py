from flask import Blueprint, jsonify, current_app, request
from ...database.db import db
from ...models.model import Menu
from ...services.request_parser import parse_filters
from ...services.validate_filter import validate_menu_filters
from ...services.menu_service import MenuService

bp = Blueprint('filters_pagination', __name__)
menu_service = MenuService()

@bp.route("/menu", methods=['GET'])
def menu_filters_pagination():
    try:
        print("woiwoiwoiwoiwoiwoi")

        filters = parse_filters(request)
        validate_menu_filters(filters)
        print("lolossss validationnn")
        

        query = Menu.query

        query = menu_service.query_filters(query, filters)
        query = menu_service.sorting(query, filters['sort'])
        print("sorting donee")

        pagination = query.paginate(
            page=filters['page'], 
            per_page=filters['per_page'], 
            error_out=False
        )

        response_data = menu_service.process_items(
            items=pagination.items, 
            language=filters['language'], 
            alergen_tags=filters['alergen_tags'])

        return jsonify({
            'items': response_data,
            'pagination': {
                'page': filters['page'],
                'per_page': filters['per_page'],
                'total': pagination.total,  
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500