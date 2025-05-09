from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import inventory, user, orders, auth, category, supplier, customer
from app.models.user import Base
from app.db.session import engine


app = FastAPI(title="Auto Parts Inventory Management")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(category.router, prefix="/categories", tags=["Categories"])
app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(supplier.router, prefix="/suppliers", tags=["Suppliers"])
app.include_router(customer.router, prefix="/customers", tags=["Customers"])


@app.get("/")
def root():
    return {"message": "Welcome to the Auto Parts Inventory Management API"}
