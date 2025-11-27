# Menu API Routes Documentation

## Overview

This document provides comprehensive documentation for all API routes in the Menu Catalog application. The API is built with Flask and includes features for creating, retrieving, updating, and deleting menu items, with advanced search and filtering capabilities powered by Google Gemini AI.

---

## Base Configuration

- **Base URL**: `/api`
- **Framework**: Flask with SQLAlchemy ORM
- **Database**: PostgreSQL (via SQLAlchemy)
- **AI Integration**: Google Gemini API

---

## Menu Data Model

### Database Schema (Menu)

```
Table: menus
├── id (Integer, Primary Key)
├── name (String)
├── category (String)
├── calories (Float)
├── price (Float)
├── description (String)
└── ingredients (Array of Strings)
```

### Request/Response Schemas

**MenuCreate** (for POST/PUT requests):
```json
{
  "name": "string (required)",
  "category": "string (optional)",
  "calories": "float (required)",
  "price": "float (required)",
  "ingredients": ["string array (required)"],
  "description": "string (optional)"
}
```

**MenuResponse** (from GET requests):
```json
{
  "id": "integer",
  "name": "string",
  "category": "string",
  "calories": "float",
  "price": "float",
  "ingredients": ["string array"],
  "description": "string",
  "allergen": "string (optional)"
}
```

---

## Routes

### 1. Create Menu Item

**Endpoint**: `POST /api/menu`

**Purpose**: Create a new menu item with optional AI-powered description and category generation.

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `ai_description` | string | 'false' | If 'true' or description is null, Gemini generates a description |
| `ai_category` | string | 'false' | If 'true' or category is null, Gemini categorizes the item |

**Request Body**:
```json
{
  "name": "Espresso",
  "category": "drinks",
  "calories": 5,
  "price": 3.50,
  "ingredients": ["coffee", "water"],
  "description": "Strong black coffee"
}
```

**Response** (201 on success):
```json
{
  "message": "berhasil dibuat!!",
  "menu": {
    "id": 1,
    "name": "Espresso",
    "category": "drinks",
    "calories": 5,
    "price": 3.50,
    "ingredients": ["coffee", "water"],
    "description": "Strong black coffee"
  }
}
```

**Error Responses**:
- `400 Bad Request`: No JSON provided or validation error
- `400 Bad Request`: Menu with same name already exists
- `400/500 Gemini API Error`: Issue with AI description/category generation
- `500 Internal Server Error`: Unexpected server error

**Notes**:
- Name must be unique in the database
- If `ai_description` is true OR description is null, Gemini generates one (max 10 words)
- If `ai_category` is true OR category is null, Gemini categorizes from: drinks, appetizers, desserts, main course
- Category and description can be empty strings

---

### 2. Get Menu by ID

**Endpoint**: `GET /api/menu/<menu_id>`

**Purpose**: Retrieve a specific menu item by its ID.

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `menu_id` | integer | The menu item ID |

**Response** (200 on success):
```json
{
  "id": 1,
  "name": "Espresso",
  "category": "drinks",
  "calories": 5,
  "price": 3.50,
  "ingredients": ["coffee", "water"],
  "description": "Strong black coffee"
}
```

**Error Responses**:
- `404 Not Found`: Menu item not found
- `500 Internal Server Error`: Unexpected server error

---

### 3. Get Menu with Filters and Pagination

**Endpoint**: `GET /api/menu`

**Purpose**: Retrieve menu items with advanced filtering, sorting, and pagination options. Supports AI translation and allergen detection.

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | '' | Search term (searches in name and description) |
| `category` | string | '' | Filter by category |
| `min_price` | float | null | Minimum price filter |
| `max_price` | float | null | Maximum price filter |
| `max_cal` | float | null | Maximum calories filter |
| `page` | integer | 1 | Page number for pagination |
| `per_page` | integer | 10 | Items per page |
| `sort` | string | 'price:asc' | Sort format: `field:direction` (e.g., 'price:desc', 'calories:asc') |
| `language` | string | 'en' | Language for description translation ('en' or 'id' for Indonesian) |
| `allergen_tags` | boolean | false | If true, Gemini identifies allergens in each item |

**Example Request**:
```
GET /api/menu?q=coffee&category=drinks&min_price=2&max_price=5&page=1&per_page=5&sort=price:asc&language=id&allergen_tags=true
```

**Response** (200 on success):
```json
{
  "items": [
    {
      "id": 1,
      "name": "Espresso",
      "category": "drinks",
      "calories": 5,
      "price": 3.50,
      "ingredients": ["coffee", "water"],
      "description": "Kopi hitam pekat",
      "allergen": "none"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 5,
    "total": 15,
    "pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

**Error Responses**:
- `404 Not Found`: No menu items found matching filters
- `500 Internal Server Error`: Validation or server error
- Gemini API errors may include allergen or translation failures

**Notes**:
- Search is case-insensitive and uses LIKE matching
- Negative values for price/calories are rejected
- Page and per_page must be positive integers
- If `language` is 'id', descriptions are translated to Bahasa Indonesia via Gemini
- If `allergen_tags` is true, Gemini analyzes each item for allergens (nuts, dairy, eggs, etc.)

---

### 4. Update Menu Item

**Endpoint**: `PUT /api/menu/<menu_id>`

**Purpose**: Update an existing menu item.

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `menu_id` | integer | The menu item ID |

**Request Body** (partial or full):
```json
{
  "name": "Espresso Double Shot",
  "price": 4.50,
  "description": "Strong double shot"
}
```

**Response** (200 on success):
```json
{
  "menu: ": {
    "id": 1,
    "name": "Espresso Double Shot",
    "category": "drinks",
    "calories": 5,
    "price": 4.50,
    "ingredients": ["coffee", "water"],
    "description": "Strong double shot"
  },
  "message": "Berhasil diupdate"
}
```

**Error Responses**:
- `400 Bad Request`: No JSON provided
- `400/500 Validation Error`: Invalid data format
- `404 Not Found`: Menu item not found
- `500 Internal Server Error`: Unexpected server error

**Notes**:
- All fields are optional; only provided fields are updated
- Other fields retain their previous values

---

### 5. Delete Menu Item

**Endpoint**: `DELETE /api/menu/<menu_id>`

**Purpose**: Delete a menu item from the database.

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `menu_id` | integer | The menu item ID |

**Response** (200 on success):
```json
{
  "menu: ": {
    "id": 1,
    "name": "Espresso",
    "category": "drinks",
    "calories": 5,
    "price": 3.50,
    "ingredients": ["coffee", "water"],
    "description": "Strong black coffee"
  },
  "message": "Berhasil dihapus"
}
```

**Error Responses**:
- `404 Not Found`: Menu item not found
- `500 Internal Server Error`: Unexpected server error

---

### 6. Search Menu by Name

**Endpoint**: `GET /api/menu/search`

**Purpose**: Simple search for menu items by name (returns only the first match).

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `q` | string | '' | Search term for menu name |

**Example Request**:
```
GET /api/menu/search?q=espresso
```

**Response** (200 on success):
```json
{
  "id": 1,
  "name": "Espresso",
  "category": "drinks",
  "calories": 5,
  "price": 3.50,
  "ingredients": ["coffee", "water"],
  "description": "Strong black coffee"
}
```

**Error Responses**:
- `404 Not Found`: No matching menu item found
- `400 Bad Request`: Unexpected error

**Notes**:
- Search is case-insensitive (uses ILIKE)
- Returns only the first matching result
- Does not support pagination

---

### 7. Smart Search (Natural Language Query)

**Endpoint**: `GET /api/menu/smart`

**Purpose**: Advanced search using natural language powered by Google Gemini AI. Converts user queries into SQL-style filters.

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `query` | string | '' | Natural language search query |

**Example Request**:
```
GET /api/menu/smart?query=cheap coffee drinks under 5 dollars
```

**How It Works**:
1. Gemini AI processes the natural language query
2. Extracts filter parameters: name_contains, category, min_price, max_price, min_calories, max_calories
3. Converts to SQL filters
4. Returns matching menu items

**Response** (200 on success):
```json
[
  {
    "id": 1,
    "name": "Espresso",
    "category": "drinks",
    "calories": 5,
    "price": 3.50,
    "ingredients": ["coffee", "water"],
    "description": "Strong black coffee"
  }
]
```

**Error Responses**:
- `404 Not Found`: No items match the natural language query
- `400 Bad Request`: JSON parsing error or Gemini API error
- Gemini API error with error code and message

**Notes**:
- Gemini may suggest alternative categories and currency translations
- Available categories: drinks, appetizers, desserts, main course
- Supports both English and Bahasa Indonesia in queries
- Returns an array of matching items (not paginated)

---

### 8. Group Menu by Category

**Endpoint**: `GET /api/menu/group-by-category`

**Purpose**: Retrieve menu items grouped by category, with two display modes: count or list.

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `mode` | string | 'list' | Display mode: 'count' or 'list' |
| `per_category` | integer | 5 | Max items to return per category (list mode only) |

**Mode: count**

Returns count of items per category.

**Example Request**:
```
GET /api/menu/group-by-category?mode=count
```

**Response** (200 on success):
```json
[
  {
    "category": "drinks",
    "count": 10
  },
  {
    "category": "appetizers",
    "count": 8
  },
  {
    "category": "desserts",
    "count": 5
  },
  {
    "category": "main course",
    "count": 12
  }
]
```

**Mode: list**

Returns grouped items by category with limited items per category.

**Example Request**:
```
GET /api/menu/group-by-category?mode=list&per_category=3
```

**Response** (200 on success):
```json
[
  {
    "category": "drinks",
    "list": ["Espresso", "Cappuccino", "Latte"]
  },
  {
    "category": "appetizers",
    "list": ["Spring Rolls", "Bruschetta", "Calamari"]
  }
]
```

**Error Responses**:
- `400 Bad Request`: Unexpected server error

**Notes**:
- In list mode, `per_category` is limited to that number of items (default 5)
- If `per_category` is not a valid integer, the limit is ignored
- Items are sorted alphabetically by category
- Only returns items for categories that have at least one menu item

---

### 9. Root Endpoint

**Endpoint**: `GET /`

**Purpose**: API health check and basic info.

**Response**:
```json
{
  "message": "info infooo"
}
```

---

### 10. List All Routes

**Endpoint**: `GET /routes`

**Purpose**: Retrieve a list of all available API routes and their HTTP methods.

**Response** (200 on success):
```json
[
  {
    "endpoint": "menu",
    "methods": ["GET", "POST"],
    "path": "/api/menu"
  },
  {
    "endpoint": "menu_id",
    "methods": ["GET", "PUT", "DELETE"],
    "path": "/api/menu/<menu_id>"
  },
  ...
]
```

**Error Responses**:
- `400 Bad Request`: Unexpected server error

---

## Services

### MenuService

**Location**: `src/services/menu_service.py`

**Methods**:

#### `query_filters(query, filters)`
Applies filters to the database query based on filter parameters:
- `q`: Searches name and description
- `category`: Filters by category
- `min_price` / `max_price`: Price range filtering
- `max_cal`: Maximum calories filtering

#### `sorting(query, sort)`
Sorts results by field and direction. Format: `field:direction` (e.g., 'price:asc', 'calories:desc')

#### `process_items(items, language, allergen_tags)`
Processes items for response:
- Translates descriptions to requested language via Gemini (if `language='id'`)
- Identifies allergens via Gemini (if `allergen_tags=true`)
- Returns formatted response array

### Gemini Service

**Location**: `src/services/gemini.py`

**Methods**:

#### `generate_menu_description(menu)`
- Uses Gemini 2.0 Flash Lite model
- Generates short descriptions (max 10 words)
- Input: menu object with name, category, ingredients, description

#### `generate_category(menu)`
- Categorizes menu items into: drinks, appetizers, desserts, main course
- Returns lowercase category string
- Input: menu object

#### `classify_allergen(menu)`
- Identifies allergens in menu item
- Returns: comma-separated list or "none"
- Input: menu object with name, category, ingredients

#### `translate_description(menu, language)`
- Translates description to target language
- Input: menu object and language parameter
- Commonly used with language='Bahasa Indonesia'

#### `natural_language_query(query)`
- Converts natural language to SQL-style filter JSON
- Extracts: name_contains, category, min_price, max_price, min_calories, max_calories
- Returns: JSON string with filter structure

### Request Parser

**Location**: `src/services/request_parser.py`

**Function**: `parse_filters(request)`

Extracts and parses all query parameters:
```python
{
  'q': string,
  'category': string,
  'min_price': float or None,
  'max_price': float or None,
  'max_cal': float or None,
  'page': integer,
  'per_page': integer,
  'sort': string,
  'allergen_tags': boolean,
  'language': string,
  'user_query': string
}
```

### Filter Validation

**Location**: `src/services/validate_filter.py`

**Function**: `validate_menu_filters(filters)`

Validates filter parameters:
- `min_price`, `max_price`, `max_cal` must not be negative
- `page`, `per_page` must be positive integers

Returns error response if validation fails, else None.

### JSON to SQL Converter

**Location**: `src/services/json_to_sql.py`

**Function**: `json_to_sql(Menu, filters)`

Converts JSON filter structure to SQLAlchemy query:
- Supports: name_contains (list or string), category, min/max price, min/max calories
- Builds dynamic WHERE clauses
- Returns SQLAlchemy query object ready for execution

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success (GET, PUT) |
| 400 | Bad Request (invalid input, missing data) |
| 404 | Not Found (menu item doesn't exist) |
| 500 | Internal Server Error (unexpected exception) |

### Gemini API Errors

If Gemini API fails:
- Returns error code from Gemini API
- Response includes error message in `Gemini API error` field
- Common causes: API key issues, rate limiting, invalid requests

---

## Key Features

1. **AI-Powered Features**:
   - Auto-generate descriptions and categories
   - Natural language search queries
   - Multi-language description translation
   - Allergen detection and classification

2. **Advanced Search**:
   - Multi-field filtering (name, category, price, calories)
   - Natural language queries via Gemini
   - Simple name search
   - Grouped category search

3. **Flexible Sorting**:
   - Sort by any field (name, category, price, calories)
   - Ascending or descending order

4. **Pagination**:
   - Customizable page size
   - Includes pagination metadata (total, pages, has_next, has_prev)

5. **Data Validation**:
   - Pydantic schema validation
   - Filter parameter validation
   - Duplicate name prevention

---

## Configuration

**Environment Variables Required**:
- `DATABASE_URL`: PostgreSQL connection string
- `GEMINI_API_KEY_2`: Google Gemini API key

**Database**: PostgreSQL with SQLAlchemy ORM

---

## Language Support

- **English**: Default language for all endpoints
- **Bahasa Indonesia**: Supported for description translation (set `language=id`) and smart search queries

---

## Notes

- All menu items with the same name are prevented (unique constraint on name)
- Ingredients are stored as string arrays in PostgreSQL
- AI features require valid Gemini API credentials
- All string searches are case-insensitive
- Response times may increase when using AI features (Gemini integration)
