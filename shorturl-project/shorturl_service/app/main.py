from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Short URL Service API", version="1.0")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Short URL Service is running"}

@app.post("/shorten/", response_model=schemas.ShortURLInfo)
def create_short_url(url: schemas.ShortURLCreate, db: Session = Depends(get_db)):
    db_url = crud.create_short_url(db, original_url=url.original_url)
    
    return schemas.ShortURLInfo(
        id=db_url.id,
        original_url=db_url.original_url,
        short_key=db_url.short_key,
        created_at=db_url.created_at,
        clicks=db_url.clicks,
        short_url=f"http://localhost:8001/{db_url.short_key}"  # Изменится в продакшене
    )

@app.get("/{short_key}")
def redirect_to_url(short_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_key(db, short_key=short_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=db_url.original_url)

@app.get("/info/{short_key}", response_model=schemas.ShortURLInfo)
def get_url_info(short_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_info(db, short_key=short_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return schemas.ShortURLInfo(
        id=db_url.id,
        original_url=db_url.original_url,
        short_key=db_url.short_key,
        created_at=db_url.created_at,
        clicks=db_url.clicks,
        short_url=f"http://localhost:8001/{db_url.short_key}"
    )

@app.get("/urls/all", response_model=List[schemas.ShortURLInfo])
def get_all_urls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    urls = crud.get_all_urls(db, skip=skip, limit=limit)
    result = []
    for url in urls:
        result.append(
            schemas.ShortURLInfo(
                id=url.id,
                original_url=url.original_url,
                short_key=url.short_key,
                created_at=url.created_at,
                clicks=url.clicks,
                short_url=f"http://localhost:8001/{url.short_key}"
            )
        )
    return result