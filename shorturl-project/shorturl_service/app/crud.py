import shortuuid
from sqlalchemy.orm import Session
from . import models

def generate_short_key():
    return shortuuid.uuid()[:8]

def create_short_url(db: Session, original_url: str):
    short_key = generate_short_key()
    
    # Проверяем, не существует ли уже такой ключ
    while db.query(models.ShortURL).filter(models.ShortURL.short_key == short_key).first():
        short_key = generate_short_key()
    
    db_url = models.ShortURL(
        original_url=original_url,
        short_key=short_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url_by_key(db: Session, short_key: str):
    url = db.query(models.ShortURL).filter(models.ShortURL.short_key == short_key).first()
    if url:
        url.clicks += 1
        db.commit()
        db.refresh(url)
    return url

def get_url_info(db: Session, short_key: str):
    return db.query(models.ShortURL).filter(models.ShortURL.short_key == short_key).first()

def get_all_urls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ShortURL).offset(skip).limit(limit).all()