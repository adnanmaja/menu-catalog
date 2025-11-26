from ..models.model import Menu
from .gemini import Gemini
from ..schemas.menu import MenuResponse
from google.genai import errors
from flask import jsonify

class MenuService:
    def __init__(self):
        self.gemini = Gemini()

    def query_filters(self, query, filters):
        if filters.get('q'):
            query = query.filter(
                Menu.name.ilike(f"%{filters['q']}%") |
                Menu.description.ilike(f"%{filters['q']}%")
            )

        if filters.get('category'):
            query = query.filter(Menu.category.ilike(f"%{filters['category']}%"))
        
        if filters.get('min_price') is not None:
            query = query.filter(Menu.price >= filters['min_price'])
        
        if filters.get('max_price') is not None:
            query = query.filter(Menu.price <= filters['max_price'])
        
        if filters.get('max_cal') is not None:
            query = query.filter(Menu.calories <= filters['max_cal'])
        
        return query
    
    def sorting(self, query, sort):
        field, direction = sort.split(':')
    
        if direction.lower() == 'asc':
            query = query.order_by(getattr(Menu, field).asc())
        else:
            query = query.order_by(getattr(Menu, field).desc())

        return query
    
    def process_items(self, items, language, alergen_tags):
        response_data = []

        for item in items:
            try: 
                # gemini description translation
                if language == 'id':
                    item.description = self.gemini.translate_description(menu=item, language='Bahasa Indonesia')

                alergen = None
                
                # gemini alergen identification
                if alergen_tags:
                    alergen = self.gemini.classify_alergen(menu=item)
                    print(f"menu_service, gemini response: {alergen}")
   
                item_data = {
                    'id': item.id,
                    'name': item.name,
                    'category': item.category,
                    'calories': item.calories,
                    'price': item.price,
                    'ingredients': item.ingredients,
                    'description': item.description
                }
                
                if alergen is not None:
                    item_data['alergen'] = alergen
                    
                response_data.append(item_data)
                
            except errors.APIError as e:
                return [{'error': 'Gemini API error', 'message': str(e.message)}], e.code
    
        return response_data