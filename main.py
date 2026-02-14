from fastapi import FastAPI, Depends
from models import Product
from database import SessionLocal, engine
from sqlalchemy.orm import Session
import database_models

app = FastAPI()

database = database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return {"hello": "world!"}

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
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = SessionLocal()
    count = db.query(database_models.Product).count()
    
    if count == 0:
        for product in products:
            db.add(database_models.Product(**product.model_dump()))

        db.commit()

init_db()

@app.get("/status")
def get_status():
    return {"status": "okay"}

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "Product not Found"

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return {"message": "Product added successfully"}

@app.put("/products/{id}")
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product Updated"
    else:
        return "Product not Found"
    
@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        "Product not Found"