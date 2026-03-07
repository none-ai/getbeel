from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Mock data for products
products = [
    {
        "id": 1,
        "name": "BeelAI",
        "tagline": "AI-powered productivity assistant for teams",
        "votes": 142,
        "category": "Productivity",
        "description": "BeelAI helps teams collaborate smarter with AI-powered insights and automation."
    },
    {
        "id": 2,
        "name": "BeelChat",
        "tagline": "Real-time messaging for remote teams",
        "votes": 98,
        "category": "Communication",
        "description": "Seamless communication platform built for distributed teams."
    },
    {
        "id": 3,
        "name": "BeelFlow",
        "tagline": "Visual workflow automation tool",
        "votes": 76,
        "category": "Developer Tools",
        "description": "Automate your workflows with a drag-and-drop visual editor."
    },
    {
        "id": 4,
        "name": "BeelSpace",
        "tagline": "All-in-one workspace for creators",
        "votes": 203,
        "category": "Productivity",
        "description": "The ultimate workspace for content creators and makers."
    }
]


@app.route('/')
def index():
    """Home page - list all products"""
    sort_by = request.args.get('sort', 'votes')
    sorted_products = sorted(products, key=lambda x: x['votes'], reverse=True)
    if sort_by == 'newest':
        sorted_products = products  # Keep original order for newest
    return render_template('index.html', products=sorted_products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return "Product not found", 404
    return render_template('product.html', product=product)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Submit a new product"""
    if request.method == 'POST':
        name = request.form.get('name')
        tagline = request.form.get('tagline')
        category = request.form.get('category')
        description = request.form.get('description')

        new_product = {
            "id": len(products) + 1,
            "name": name,
            "tagline": tagline,
            "votes": 0,
            "category": category,
            "description": description
        }
        products.append(new_product)
        return redirect(url_for('index'))

    return render_template('submit.html')


@app.route('/api/products')
def api_products():
    """API endpoint to get all products"""
    return jsonify(products)


@app.route('/api/products/<int:product_id>/vote', methods=['POST'])
def vote_product(product_id):
    """API endpoint to vote for a product"""
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    product['votes'] += 1
    return jsonify({"votes": product['votes']})


if __name__ == '__main__':
    app.run(debug=True)
