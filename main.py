from fastapi import FastAPI
from routers import products, users, jwt_auth_users
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Especifica los orígenes permitidos, por ejemplo ["http:/localhost:3000"]
    allow_origins=["*"],
    allow_credentials=True,
    # Especifica los métodos HTTP permitidos, por ejemplo ["GET", "POST"]
    allow_methods=["*"],
    # Especifica las cabeceras permitidas, por ejemplo ["Authorization"]
    allow_headers=["*"],
)


app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def hello():
    return {'gretting': "¡Hello Backend with python!"}
