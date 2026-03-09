import json
import os
from datetime import datetime
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash

app = Flask(__name__)
app.secret_key = 'getbeel-secret-key-change-in-production'

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')


def is_valid_url(url):
    """Validate URL format"""
    if not url:
        return True  # Empty URL is optional
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False


def load_data():
    """Load data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"products": [], "comments": [], "next_product_id": 1, "next_comment_id": 1}


def save_data(data):
    """Save data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@app.route('/')
def index():
    """Home page - list all products with search and filter"""
    data = load_data()
    products = data.get('products', [])

    # Search functionality
    search_query = request.args.get('q', '').strip().lower()
    if search_query:
        products = [p for p in products if search_query in p['name'].lower() or search_query in p['tagline'].lower()]

    # Category filter
    category = request.args.get('category', '')
    if category:
        products = [p for p in products if p['category'] == category]

    # Sort
    sort_by = request.args.get('sort', 'votes')
    if sort_by == 'votes':
        products = sorted(products, key=lambda x: x['votes'], reverse=True)
    elif sort_by == 'newest':
        products = sorted(products, key=lambda x: x.get('created_at', ''), reverse=True)

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = 10
    total = len(products)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_products = products[start:end]

    # Get unique categories for filter
    categories = sorted(list(set(p.get('category', 'Other') for p in data.get('products', []))))

    return render_template('index.html',
                         products=paginated_products,
                         categories=categories,
                         search_query=search_query,
                         selected_category=category,
                         sort_by=sort_by,
                         page=page,
                         total=total,
                         per_page=per_page)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page with comments"""
    data = load_data()
    product = next((p for p in data.get('products', []) if p['id'] == product_id), None)

    if product is None:
        return "Product not found", 404

    # Get comments for this product
    comments = [c for c in data.get('comments', []) if c['product_id'] == product_id]
    comments = sorted(comments, key=lambda x: x.get('created_at', ''), reverse=True)

    return render_template('product.html', product=product, comments=comments)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Submit a new product"""
    data = load_data()
    categories = ['Productivity', 'Communication', 'Developer Tools', 'Design Tools', 'Marketing', 'Other']

    if request.method == 'POST':
        name = request.form.get('name')
        tagline = request.form.get('tagline')
        category = request.form.get('category')
        description = request.form.get('description')
        maker = request.form.get('maker', 'Anonymous')
        maker_url = request.form.get('maker_url', '')

        # Validate required fields
        if not name or not name.strip():
            flash('Product name is required', 'error')
            return render_template('submit.html', categories=categories)

        if not tagline or not tagline.strip():
            flash('Tagline is required', 'error')
            return render_template('submit.html', categories=categories)

        # Validate maker URL
        if maker_url and not is_valid_url(maker_url):
            flash('Please enter a valid URL for maker website', 'error')
            return render_template('submit.html', categories=categories)

        new_product = {
            "id": data['next_product_id'],
            "name": name,
            "tagline": tagline,
            "votes": 0,
            "category": category,
            "description": description,
            "maker": maker,
            "maker_url": maker_url,
            "thumbnail_url": "",
            "created_at": datetime.now().strftime('%Y-%m-%d')
        }

        data['products'].append(new_product)
        data['next_product_id'] += 1
        save_data(data)

        flash('Product submitted successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('submit.html', categories=categories)


@app.route('/api/products')
def api_products():
    """API endpoint to get all products"""
    data = load_data()
    return jsonify(data.get('products', []))


@app.route('/api/products/<int:product_id>/vote', methods=['POST'])
def vote_product(product_id):
    """API endpoint to vote for a product"""
    data = load_data()
    product = next((p for p in data['products'] if p['id'] == product_id), None)

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    product['votes'] += 1
    save_data(data)

    return jsonify({"votes": product['votes']})


@app.route('/product/<int:product_id>/comment', methods=['POST'])
def add_comment(product_id):
    """Add a comment to a product"""
    data = load_data()
    product = next((p for p in data['products'] if p['id'] == product_id), None)

    if product is None:
        flash('Product not found', 'error')
        return redirect(url_for('index'))

    author = request.form.get('author', 'Anonymous')
    content = request.form.get('content', '').strip()

    if not content:
        flash('Comment cannot be empty', 'error')
        return redirect(url_for('product_detail', product_id=product_id))

    new_comment = {
        "id": data['next_comment_id'],
        "product_id": product_id,
        "author": author,
        "content": content,
        "created_at": datetime.now().strftime('%Y-%m-%d')
    }

    data['comments'].append(new_comment)
    data['next_comment_id'] += 1
    save_data(data)

    flash('Comment added successfully!', 'success')
    return redirect(url_for('product_detail', product_id=product_id))


@app.route('/maker/<username>')
def maker_profile(username):
    """Maker profile page showing all products by a maker"""
    data = load_data()
    maker_products = [p for p in data.get('products', []) if p.get('maker', '').lower() == username.lower()]

    if not maker_products:
        return "Maker not found", 404

    return render_template('maker.html', maker=username, products=maker_products)


@app.route('/categories')
def categories():
    """Categories overview page"""
    data = load_data()
    products = data.get('products', [])

    # Group products by category
    category_data = {}
    for p in products:
        cat = p.get('category', 'Other')
        if cat not in category_data:
            category_data[cat] = []
        category_data[cat].append(p)

    # Sort categories by total votes
    sorted_categories = sorted(category_data.items(),
                              key=lambda x: sum(p.get('votes', 0) for p in x[1]),
                              reverse=True)

    return render_template('categories.html', categories=sorted_categories)


if __name__ == '__main__':
    app.run(debug=True)
