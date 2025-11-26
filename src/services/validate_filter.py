from flask import jsonify

def validate_menu_filters(filters):
    if filters['min_price'] and filters['min_price'] < 0:
        return jsonify({'error': 'min_price gaboleh negatif'}), 400
    
    if filters['max_price'] and filters['max_price'] < 0:
        return jsonify({'error': 'max_price gaboleh negatif'}), 400
    
    if filters['max_cal'] and filters['max_cal'] < 0:
        return jsonify({'error': 'max_cal gaboleh negaitf'}), 400
    
    if filters['page'] < 1 or filters['per_page'] < 1:
        return jsonify({'error': 'page dan per_page harus integer positif'}), 400
    
    return None
