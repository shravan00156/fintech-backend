from fastapi import FastAPI
from database import engine, Base
from routes import transactions

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(transactions.router)

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}