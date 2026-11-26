from flask import Flask, g, jsonify, request
from pydantic import TypeAdapter, ValidationError

import database_models
from database import SessionLocal, engine
from models import Product

app = Flask(__name__)
product_id = TypeAdapter(int)

products = [
    Product(id=1, name="Laptop", description="15-inch gaming laptop", price=1299.99, quantity=10),
    Product(id=2, name="Headphones", description="Noise-cancelling over-ear headphones", price=199.99, quantity=25),
    Product(id=3, name="Keyboard", description="Mechanical RGB keyboard", price=89.50, quantity=40),
    Product(id=4, name="Mouse", description="Wireless ergonomic mouse", price=49.99, quantity=60),
    Product(id=5, name="Monitor", description="27-inch 4K UHD monitor", price=349.99, quantity=15),
    Product(id=6, name="Chair", description="Ergonomic office chair", price=249.00, quantity=20),
    Product(id=7, name="Desk", description="Adjustable standing desk", price=499.99, quantity=8),
    Product(id=8, name="Webcam", description="1080p HD USB webcam", price=79.99, quantity=35),
    Product(id=9, name="Microphone", description="USB condenser microphone", price=129.95, quantity=18),
    Product(id=10, name="External SSD", description="1TB portable external SSD", price=159.99, quantity=22),
]


def get_db():
    if "db" not in g:
        g.db = SessionLocal()
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    database_models.Base.metadata.create_all(bind=engine)
    with SessionLocal.begin() as db:
        if db.query(database_models.Product).count() == 0:
            db.add_all(database_models.Product(**product.model_dump()) for product in products)


init_db()


def validation_response(error, location):
    details = error.errors(include_url=False, include_context=False, include_input=False)
    for detail in details:
        detail["loc"] = [*location, *detail["loc"]]
    return jsonify(detail=details), 422


def parse_product():
    payload = request.get_json(force=not request.mimetype, silent=True)
    return Product.model_validate(payload)


def get_product(id):
    return get_db().get(database_models.Product, id)


def serialize_product(product):
    return {field: getattr(product, field) for field in Product.model_fields}


@app.get("/")
def greet():
    return {"hello": "world!"}


@app.get("/status")
def get_status():
    return {"status": "okay"}


@app.get("/products")
def get_all_products():
    products = get_db().query(database_models.Product).all()
    return jsonify([serialize_product(product) for product in products])


@app.get("/products/<id>")
def get_product_by_id(id):
    try:
        id = product_id.validate_python(id)
    except ValidationError as error:
        return validation_response(error, ("path", "id"))
    product = get_product(id)
    if product is None:
        return jsonify("Product not Found")
    return jsonify(serialize_product(product))


@app.post("/products")
def add_product():
    try:
        product = parse_product()
    except ValidationError as error:
        return validation_response(error, ("body",))
    db = get_db()
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return {"message": "Product added successfully"}


@app.put("/products/<id>")
def update_product(id):
    try:
        id = product_id.validate_python(id)
    except ValidationError as error:
        return validation_response(error, ("path", "id"))
    try:
        product = parse_product()
    except ValidationError as error:
        return validation_response(error, ("body",))

    db_product = get_product(id)
    if db_product is None:
        return jsonify("Product not Found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    get_db().commit()
    return jsonify("Product Updated")


@app.delete("/products/<id>")
def delete_product(id):
    try:
        id = product_id.validate_python(id)
    except ValidationError as error:
        return validation_response(error, ("path", "id"))
    product = get_product(id)
    if product is not None:
        db = get_db()
        db.delete(product)
        db.commit()
    return jsonify(None)
