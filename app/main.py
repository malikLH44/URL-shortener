from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import RedirectResponse
from app.cache import get_cached_url, set_cached_url
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
    # 1. On regarde d'abord dans le cache
    cached = get_cached_url(code)
    if cached:
        print(f"CACHE HIT  → {code}", flush=True)
        # On compte quand même le clic en base
        db.query(Link).filter(Link.code == code).update(
            {Link.clicks: Link.clicks + 1}
        )
        db.commit()
        return RedirectResponse(url=cached)

    # 2. Sinon, on va chercher en base
    print(f"CACHE MISS → {code}", flush=True)
    link = db.query(Link).filter(Link.code == code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Lien introuvable")

    link.clicks += 1
    db.commit()

    # 3. On met en cache pour la prochaine fois
    set_cached_url(code, link.url)
    return RedirectResponse(url=link.url)


@app.get("/stats/{code}")
def stats(code: str, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.code == code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Lien introuvable")
    return {"code": link.code, "url": link.url, "clicks": link.clicks}