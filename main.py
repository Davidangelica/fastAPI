from fastapi import FastAPI
from routers.users import router as u
from security.auth_user import router as au
from routers.employees import router as e
from routers.products import router as p
# app
app = FastAPI()

# routers
app.include_router(u)
app.include_router(e)
app.include_router(p)
app.include_router(au)