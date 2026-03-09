# GetBeel - Product Discovery Platform

A simple Flask application inspired by ProductHunt for discovering and sharing products.

## Features

- Browse products sorted by votes or newest
- View product details with full descriptions
- Submit new products with maker information
- Vote for products via API or UI
- Search products by name or tagline
- Filter products by category
- Paginated product listing
- Comments and reviews system
- Maker profiles - see all products by a maker
- Social sharing (Twitter, Facebook, LinkedIn)
- Categories overview page
- Data persistence with JSON storage

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home page - list all products with search/filter |
| `/product/<id>` | Product detail page with comments |
| `/submit` | Submit a new product |
| `/categories` | Browse products by category |
| `/maker/<username>` | Maker profile page |
| `/api/products` | Get all products (JSON API) |
| `/api/products/<id>/vote` | Vote for a product (POST) |

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## Tech Stack

- Flask 3.0.0
- Python
- JSON file-based data storage

## New Features in This Version

### Search & Filter
- Full-text search across product names and taglines
- Category filtering
- Sort by votes or newest

### Comments System
- Users can leave comments on products
- View all comments on product detail page

### Maker Profiles
- Track who made each product
- View all products by a specific maker
- Maker website links

### Social Sharing
- Share products on Twitter, Facebook, LinkedIn
- Copy link functionality

### Categories
- Dedicated categories page
- Products grouped by category
- Category statistics

### Pagination
- 10 products per page
- Navigate through large product lists

## 作者: stlin256的openclaw
