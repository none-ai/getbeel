# GetBeel - Product Discovery Platform

A simple Flask application inspired by ProductHunt for discovering and sharing products.

## Features

- Browse products sorted by votes or newest
- View product details
- Submit new products
- Vote for products via API

## Routes

| Route | Description |
|-------|-------------|
| `/` | Home page - list all products |
| `/product/<id>` | Product detail page |
| `/submit` | Submit a new product |
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
