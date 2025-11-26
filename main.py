from flask import Flask, jsonify
from flask_cors import CORS
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from src.database.db import init_app
from src.api.routes import menu_filters_pagination, menu_post, menu_group_by_cat, menu_put_delete, menu_search, menu_smart_search

app = Flask(__name__)
CORS(app)

app = init_app(app)

app.register_blueprint(menu_post.bp, url_prefix="/api")
app.register_blueprint(menu_put_delete.bp, url_prefix="/api")
app.register_blueprint(menu_filters_pagination.bp, url_prefix="/api")
app.register_blueprint(menu_group_by_cat.bp, url_prefix="/api")
app.register_blueprint(menu_search.bp, url_prefix="/api")
app.register_blueprint(menu_smart_search.bp, url_prefix='/api')

@app.route("/", methods=['GET'])
def root():
    return jsonify({'message': 'info infooo'})

@app.route('/routes', methods=['GET'])
def list_routes():
    try: 
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'path': str(rule)
            })
        return jsonify(routes)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)

