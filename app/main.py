from fastapi import FastAPI
from app.routes import inventory, user, orders, auth
from app.models.user import Base
from app.db.session import engine


app = FastAPI(title="Auto Parts Inventory Management")

# Create tables in the database
Base.metadata.create_all(bind=engine)

# Include routers
# app.include_router(inventory.router, prefix="/inventory", tags=["Inventory"])
app.include_router(inventory.router, tags=["Inventory"])
app.include_router(user.router, prefix="/users", tags=["Users"])
# app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])


@app.get("/")
def root():
    return {"message": "Welcome to the Auto Parts Inventory Management API"}
