from http.client import HTTPException
from fastapi import FastAPI,status
from app.db import models
from app.db.database import engine
from app.api.endpoints import books, users, favorites
from slowapi import Limiter,_rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded



limiter = Limiter(key_func=get_remote_address)
app = FastAPI()

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)


models.Base.metadata.create_all(bind=engine)


app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
