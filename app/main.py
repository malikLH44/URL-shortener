from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
import secrets

from app.database import engine, get_db, Base
from app.models import Link

# Crée les tables au démarrage si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")


class LinkIn(BaseModel):
    url: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shorten")
def shorten(payload: LinkIn, db: Session = Depends(get_db)):
    code = secrets.token_urlsafe(4)[:6]
    link = Link(code=code, url=payload.url, clicks=0)
    db.add(link)
    db.commit()
    return {"code": code, "short_url": f"/{code}"}


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.code == code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Lien introuvable")
    link.clicks += 1
    db.commit()
    return RedirectResponse(url=link.url)


@app.get("/stats/{code}")
def stats(code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.code == code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Lien introuvable")
    return {"code": link.code, "url": link.url, "clicks": link.clicks}