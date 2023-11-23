from fastapi import FastAPI

from . import models
from .database import engine
from .routers import product, seller, login


app = FastAPI(
    title="Products API",
    description="This document is about Products Api",
    contact={
        "Developer name": "Nimesh Vishwakarma",
        "website": "https://nimesh-portfolio.vercel.app/",
        "email": "nimeshvishwav@gmail.com",
    },
)


app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)

models.Base.metadata.create_all(engine)
