def parse_filters(request):
    return {
        'q': request.args.get('q', '').strip(),
        'category': request.args.get('category', '').strip(),
        'min_price': request.args.get('min_price', type=float),
        'max_price': request.args.get('max_price', type=float),
        'max_cal': request.args.get('max_cal', type=float),
        'page': request.args.get('page', 1, type=int),
        'per_page': request.args.get('per_page', 10, type=int),
        'sort': request.args.get('sort', 'price:asc'),
        'alergen_tags': request.args.get('alergen_tags', False, type=bool),
        'language': request.args.get('language', 'en').strip().lower()
    }