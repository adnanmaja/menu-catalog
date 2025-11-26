from flask import Blueprint, jsonify, current_app, request
from ...database.db import db
from ...models.model import Menu
from ...schemas.menu import MenuResponse
from ...services.gemini import Gemini
from google.genai import errors
import logging

bp = Blueprint('filters_pagination', __name__)

@bp.route("/menu", methods=['GET'])
def menu_filters_pagination():
    print("woiwoiwoiwoiwoiwoi")

    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    max_cal = request.args.get('max_cal', type=float)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort = request.args.get('sort', 'price:asc')
    alergen_tags = request.args.get('alergen_tags', False, type=bool)

    query = Menu.query

    if q:
        query = query.filter(
            
            Menu.name.ilike(f'%{q}%') |
            Menu.description.ilike(f'%{q}%') 
        )
    if category:
        query = query.filter(Menu.category.ilike(f'%{category}%'))

    if min_price is not None:
        query = query.filter(Menu.price >= min_price)

    if max_price is not None:
        query = query.filter(Menu.price <= max_price)

    if max_cal is not None:
        query = query.filter(Menu.calories <= max_cal)

    field, direction = sort.split(':')
    
    if direction.lower() == 'asc':
        query = query.order_by(getattr(Menu, field).asc())
    else:
        query = query.order_by(getattr(Menu, field).desc())
  
    pagination = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )

    # gemini alergen tags
    if not alergen_tags:   
        response_data = [
            MenuResponse(
                id=item.id,
                name=item.name,
                category=item.category,
                calories=item.calories,
                price=item.price,
                ingredients=item.ingredients,
                description=item.description,
                alergen = "none"
            )
            for item in pagination.items
        ]

    try:
        gemini = Gemini()
        response_data = [
                MenuResponse(
                    id=item.id,
                    name=item.name,
                    category=item.category,
                    calories=item.calories,
                    price=item.price,
                    ingredients=item.ingredients,
                    description=item.description,
                    alergen = gemini.classify_alergen(menu=item)
                )
                for item in pagination.items
            ]
    except errors.APIError as e:
        return jsonify({'Gemini API error': e.message}), e.code

    return jsonify({
        'items': [item.model_dump() for item in response_data],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    }), 200

