from fastapi import FastAPI
from Models.database import Base, engine, get_db, AsyncSession
from routes import users
from routes import license
from Models import User
from sqlalchemy.future import select
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
pwd_cxt = CryptContext(schemes=["argon2"], deprecated="auto")

app = FastAPI()
app.include_router(users.router)
app.include_router(license.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    # Create tables
    async with engine.begin() as conn:
        # Fungua connection
        # Tumia connection
        # Ikimaliza ifunge yenyewe
        await conn.run_sync(Base.metadata.create_all)

    # Seed admin data
    async for db in get_db():
        await seed_data(db)

async def seed_data(db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == "shamsay70@gmail.com"))
    existing_user = result.scalars().first()
    if not existing_user:
        admin = User(
            firstname="Shamis",
            lastname="Ali",
            email="shamsay70@gmail.com",
            password=pwd_cxt.hash("shamsay321!")
        )
        db.add(admin)
        await db.commit()



