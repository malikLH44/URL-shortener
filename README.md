# URL Shortener

Service de raccourcissement d'URL avec cache et statistiques de clics.
Architecture multi-conteneurs orchestrée avec Docker Compose.

## Architecture

navigateur → nginx (React) → FastAPI → Redis (cache) → PostgreSQL (persistance)



| Service    | Rôle                                               | Image                              |
| ---------- | -------------------------------------------------- | ---------------------------------- |
| `frontend` | Interface React, servie par nginx (reverse proxy)  | build multi-stage → nginx:alpine   |
| `backend`  | API REST FastAPI                                   | build → python:3.12-slim           |
| `db`       | Persistance des liens et compteurs                 | postgres:16                        |
| `redis`    | Cache des redirections (TTL 1h)                    | redis:7-alpine                     |

## Démarrage

```bash
git clone <url-du-depot>
cd url-shortener
cp .env.example .env    
docker compose up -d
```

L'interface est disponible sur `http://localhost:3000`.

## API

| Méthode | Route           | Description                              |
| ------- | --------------- | ---------------------------------------- |
| `POST`  | `/shorten`      | Crée un lien court à partir d'une URL    |
| `GET`   | `/{code}`       | Redirige vers l'URL d'origine            |
| `GET`   | `/stats/{code}` | Retourne les statistiques du lien        |
| `GET`   | `/health`       | Vérification de l'état du service        |

## Choix techniques

**Cache Redis** — les redirections fréquentes sont servies depuis le cache
(TTL 1h), évitant un accès base à chaque clic. Les compteurs restent
persistés en base.

**Multi-stage build** — l'image frontend compile React avec Node puis ne
conserve que les fichiers statiques dans nginx (93 Mo au lieu de ~450 Mo,
sans outils de build en production).

**Reverse proxy** — nginx est le point d'entrée unique. Le backend n'est
pas exposé et n'est joignable que via le réseau interne Docker.

**Sécurité** — le backend s'exécute sous un utilisateur non privilégié.
Les secrets sont injectés par variables d'environnement et ne sont ni
commités ni inclus dans les images.

**Healthchecks** — chaque service expose une sonde de santé ; le backend
attend que la base et le cache soient réellement prêts avant de démarrer.

## Commandes utiles

```bash
docker compose ps                    # état des services
docker compose logs -f backend       # logs en direct
docker compose exec redis redis-cli  # inspecter le cache
docker compose down                  # arrêter (les données persistent)
docker compose down -v               # arrêter et supprimer les volumes
```