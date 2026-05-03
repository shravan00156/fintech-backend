from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

router = APIRouter()

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE transaction
@router.post("/transactions")
def create_transaction(txn: schemas.TransactionCreate, db: Session = Depends(get_db)):
    new_txn = models.Transaction(**txn.dict())
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn

# GET all transactions
@router.get("/transactions")
def get_transactions(db: Session = Depends(get_db)):
    return db.query(models.Transaction).all()
@router.put("/transactions/{id}")
def update_transaction(id: int, txn: schemas.TransactionCreate, db: Session = Depends(get_db)):
    existing_txn = db.query(models.Transaction).filter(models.Transaction.id == id).first()
    
    if not existing_txn:
        return {"error": "Transaction not found"}

    existing_txn.amount = txn.amount
    existing_txn.type = txn.type
    existing_txn.description = txn.description

    db.commit()
    db.refresh(existing_txn)

    return existing_txn