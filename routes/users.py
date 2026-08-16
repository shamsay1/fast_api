from fastapi import APIRouter, Depends, Response, status, HTTPException
from Schemas.users import UserCreate, UserResponse,LoginResponse,LoginCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Models import User
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from Models.database import get_db
from passlib.context import CryptContext
from Schemas.users import ChangePasswordRequest
from Auth.auth import verify_password, create_access_token,hash_password,get_current_user

router = APIRouter(prefix="/users", tags=["Users"])
pwd_cxt = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

@router.get("/allusers", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.post("/register", response_model=UserResponse)
async def register_user(request: UserCreate, db: AsyncSession = Depends(get_db)):
    hash_password = pwd_cxt.hash(request.password)
    new_user = User(
        firstname=request.firstname,
        lastname=request.lastname,
        email=request.email,
        password=hash_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post(
    "/login_user",
    response_model=LoginResponse
)
@router.post("/login_user")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):

    # Tafuta user kwa kutumia email
    query = await db.execute(
        select(User).where(
            User.email == form_data.username
        )
    )

    user = query.scalars().first()

    # Kama user hayupo
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Hakikisha password ni sahihi
    if not verify_password(
        form_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )

    # Tengeneza JWT token
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "email": user.email
        }
    )

    # Return token + user information
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.firstname
        }
    }

@router.put("/change_password")
async def change_password(
    request: ChangePasswordRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # -----------------------------------
    # 1. Hakikisha password mpya zinafanana
    # -----------------------------------

    if request.new_password != request.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirm password do not match"
        )

    # -----------------------------------
    # 2. Hakikisha current password ni sahihi
    # -----------------------------------

    if not verify_password(
        request.current_password,
        current_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # -----------------------------------
    # 3. Zuia password mpya kuwa sawa
    #    na password ya zamani
    # -----------------------------------

    if verify_password(
        request.new_password,
        current_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password"
        )

    # -----------------------------------
    # 4. Hash password mpya
    # -----------------------------------

    current_user.password = hash_password(
        request.new_password
    )

    # -----------------------------------
    # 5. Save database
    # -----------------------------------

    await db.commit()

    # -----------------------------------
    # 6. Response
    # -----------------------------------

    return {
        "message": "Password changed successfully"
    }

@router.delete("/delete/{id}", status_code=200)
async def delete_user(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.id == id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User with that id is not found")

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}




