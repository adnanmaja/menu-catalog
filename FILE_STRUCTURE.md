# Project File Structure

## Directory Tree

```
menu-catalog/
├── main.py                          # Flask application entry point
├── Dockerfile                       # Docker configuration
├── requirements.txt                 # Python dependencies
├── README.md                        # Project readme
├── notes.md                         # Project notes
├── ROUTES_DOCUMENTATION.md          # API routes documentation
├── FILE_STRUCTURE.md                # This file
│
├── __pycache__/                     # Python bytecode cache
│
└── src/                             # Source code directory
    ├── __init__.py                  # Package initializer
    │
    ├── api/                         # API layer
    │   ├── __init__.py
    │   └── routes/                  # Route blueprints
    │       ├── __init__.py
    │       ├── menu_post.py         # POST /api/menu - Create menu
    │       ├── menu_put_delete.py   # PUT/DELETE /api/menu/<id> - Update/Delete menu
    │       ├── menu_filters_pagination.py  # GET /api/menu - Get with filters & pagination
    │       ├── menu_search.py       # GET /api/menu/search - Simple name search
    │       ├── menu_smart_search.py # GET /api/menu/smart - AI natural language search
    │       ├── menu_group_by_cat.py # GET /api/menu/group-by-category - Group by category
    │       └── __pycache__/
    │
    ├── database/                    # Database configuration
    │   ├── __init__.py
    │   ├── db.py                    # SQLAlchemy setup & initialization
    │   └── __pycache__/
    │
    ├── models/                      # Database models
    │   ├── __init__.py
    │   ├── model.py                 # Menu model (ORM entity)
    │   └── __pycache__/
    │
    ├── schemas/                     # Pydantic schemas (validation)
    │   ├── __init__.py
    │   ├── menu.py                  # MenuCreate & MenuResponse schemas
    │   └── __pycache__/
    │
    ├── services/                    # Business logic layer
    │   ├── __init__.py
    │   ├── menu_service.py          # Menu query filtering, sorting, processing
    │   ├── gemini.py                # Google Gemini AI integration
    │   ├── json_to_sql.py           # Convert JSON filters to SQL queries
    │   ├── request_parser.py        # Parse query parameters
    │   ├── validate_filter.py       # Validate filter parameters
    │   └── __pycache__/
    │
    └── __pycache__/
```

---

## File Descriptions

### Root Level Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point for Flask application. Initializes app, registers blueprints, and defines root routes |
| `Dockerfile` | Docker containerization configuration |
| `requirements.txt` | Python package dependencies (Flask, SQLAlchemy, Pydantic, Google Genai, etc.) |
| `README.md` | Project overview and setup instructions |
| `notes.md` | Development notes and miscellaneous information |
| `ROUTES_DOCUMENTATION.md` | Comprehensive API routes documentation |
| `FILE_STRUCTURE.md` | This file - project structure reference |

---

## Directory Structure Details

### `src/api/routes/`
Contains Flask Blueprint route handlers. Each file represents a logical group of endpoints:

| File | Routes | Purpose |
|------|--------|---------|
| `menu_post.py` | `POST /api/menu` | Create new menu items with optional AI description/category generation |
| `menu_put_delete.py` | `GET /api/menu/<id>`, `PUT /api/menu/<id>`, `DELETE /api/menu/<id>` | Retrieve, update, or delete specific menu items |
| `menu_filters_pagination.py` | `GET /api/menu` | Retrieve menu items with advanced filtering, sorting, and pagination |
| `menu_search.py` | `GET /api/menu/search` | Simple name-based search (returns first match) |
| `menu_smart_search.py` | `GET /api/menu/smart` | AI-powered natural language search via Gemini |
| `menu_group_by_cat.py` | `GET /api/menu/group-by-category` | Group and display menu items by category |

### `src/database/`
Database configuration and initialization:

| File | Purpose |
|------|---------|
| `db.py` | SQLAlchemy instance creation and Flask app initialization with database URI from environment variables |

### `src/models/`
SQLAlchemy ORM entity definitions:

| File | Purpose |
|------|---------|
| `model.py` | `Menu` class - ORM model representing the `menus` table with columns: id, name, category, calories, price, description, ingredients |

### `src/schemas/`
Pydantic validation schemas:

| File | Purpose |
|------|---------|
| `menu.py` | `MenuCreate` - validation schema for POST/PUT requests; `MenuResponse` - schema for API responses |

### `src/services/`
Business logic and external integrations:

| File | Purpose |
|------|---------|
| `menu_service.py` | Query filtering, sorting, and item processing (translation, allergen detection) |
| `gemini.py` | Google Gemini AI integration: description generation, categorization, allergen detection, translation, natural language parsing |
| `json_to_sql.py` | Converts JSON filter structures from Gemini into SQLAlchemy query filters |
| `request_parser.py` | Extracts and parses all query parameters from HTTP requests into a standardized filter dictionary |
| `validate_filter.py` | Validates filter parameters (price, calories, pagination values) |

---

## Data Flow

### Creating a Menu Item
```
main.py (register route)
  ↓
menu_post.py (POST /api/menu)
  ↓
schemas/menu.py (MenuCreate validation)
  ↓
gemini.py (optional AI description/category generation)
  ↓
models/model.py (Menu ORM insert)
  ↓
database/db.py (commit to PostgreSQL)
```

### Getting Menu with Filters
```
main.py (register route)
  ↓
menu_filters_pagination.py (GET /api/menu)
  ↓
request_parser.py (parse query parameters)
  ↓
validate_filter.py (validate parameters)
  ↓
menu_service.py (apply filters & sorting)
  ↓
menu_service.py (process items - translate, detect allergens)
  ↓
gemini.py (translation, allergen detection if needed)
  ↓
database/db.py (pagination & query execution)
```

### Smart Search
```
main.py (register route)
  ↓
menu_smart_search.py (GET /api/menu/smart)
  ↓
request_parser.py (parse query parameter)
  ↓
gemini.py (natural_language_query - convert to filters)
  ↓
json_to_sql.py (convert JSON to SQLAlchemy query)
  ↓
database/db.py (execute query)
```

---

## Database Schema

**Table: `menus`**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer | Primary Key | Auto-incrementing menu item ID |
| `name` | String | Unique | Menu item name |
| `category` | String | Nullable | Category (drinks, appetizers, desserts, main course) |
| `calories` | Float | Nullable | Caloric content |
| `price` | Float | Nullable | Price in currency units |
| `description` | String | Nullable | Item description |
| `ingredients` | Array(String) | PostgreSQL ARRAY | List of ingredients |

---

## Key Technologies

- **Framework**: Flask
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Validation**: Pydantic
- **AI Integration**: Google Genai (Gemini 2.0 Flash Lite)
- **Web Server**: Flask development server (Gunicorn in production)

---

## Environment Configuration

### Required Environment Variables
```
DATABASE_URL=postgresql://user:password@host:port/database
GEMINI_API_KEY_2=your_gemini_api_key
```

### Loading Configuration
Configuration is loaded via `python-dotenv` in:
- `src/database/db.py`
- `src/services/gemini.py`

---

## Import Structure

### Circular Import Prevention
- Services import models and schemas
- Routes import services
- No reverse imports from models/schemas to routes/services
- Database initialization is centralized in `src/database/db.py`

### Blueprint Registration
All route blueprints are registered in `main.py`:
```python
app.register_blueprint(menu_post.bp, url_prefix="/api")
app.register_blueprint(menu_put_delete.bp, url_prefix="/api")
app.register_blueprint(menu_filters_pagination.bp, url_prefix="/api")
app.register_blueprint(menu_group_by_cat.bp, url_prefix="/api")
app.register_blueprint(menu_search.bp, url_prefix="/api")
app.register_blueprint(menu_smart_search.bp, url_prefix='/api')
```

---

## Caching Directories

Python automatically creates `__pycache__/` directories at each package level for bytecode caching:
- `__pycache__/` - root level
- `src/__pycache__/`
- `src/api/__pycache__/`
- `src/api/routes/__pycache__/`
- `src/database/__pycache__/`
- `src/models/__pycache__/`
- `src/schemas/__pycache__/`
- `src/services/__pycache__/`

These can be safely ignored in version control (typically added to `.gitignore`).

---

## File Size Hierarchy

```
src/                                # Business logic
├── services/                       # Core business logic (largest)
│   ├── gemini.py                  # AI integration
│   ├── menu_service.py            # Query processing
│   └── json_to_sql.py, request_parser.py, validate_filter.py
│
├── api/routes/                    # Request handlers
│   ├── menu_filters_pagination.py # Most complex route
│   ├── menu_smart_search.py
│   ├── menu_post.py, menu_put_delete.py, menu_group_by_cat.py, menu_search.py
│
├── models/                        # Data definitions (smallest)
│   └── model.py
│
├── schemas/                       # Validation schemas (small)
│   └── menu.py
│
└── database/                      # Setup only (small)
    └── db.py
```

---

## Development Workflow

1. **Define Models** (`src/models/model.py`) - Database schema
2. **Create Schemas** (`src/schemas/menu.py`) - Validation rules
3. **Build Services** (`src/services/`) - Business logic
4. **Add Routes** (`src/api/routes/`) - API endpoints
5. **Register in Main** (`main.py`) - Enable endpoints
6. **Test** - Via API calls or test suite

---

## Common File Modifications

| Task | Files to Modify |
|------|-----------------|
| Add new API endpoint | Create file in `src/api/routes/`, register in `main.py` |
| Add menu fields | Update `models/model.py`, `schemas/menu.py`, and related services |
| Add filtering capability | Update `request_parser.py`, `validate_filter.py`, `menu_service.py` |
| Integrate new AI feature | Add method to `services/gemini.py` and call from appropriate route |
| Change database | Update `DATABASE_URL` environment variable and `src/database/db.py` |

