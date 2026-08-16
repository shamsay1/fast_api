from fastapi import APIRouter,Depends
from Models.database import AsyncSession,engine,get_db
from Models import License
from sqlalchemy import select,func,or_
from typing import List
from Models import User
from Auth.auth import get_current_user
from Schemas.license import LicenseCreate,LicenseResponse
router = APIRouter(prefix="/License",tags=['License'])

@router.get(
    "/all_license",
    response_model=List[LicenseResponse]
)
async def all_license(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    licenses = await db.execute(
        select(License)
    )

    result = licenses.scalars().all()

    return result
@router.get('/counting_expired')
async def counting_expired(db:AsyncSession= Depends(get_db)):
    active_query = await db.execute(select(func.count()).select_from(License).where(License.status=="active"))
    expired_query = await db.execute(select(func.count()).select_from(License).where(License.status=="expired"))
    active_license = active_query.scalar()
    expired_license = expired_query.scalar()
    return {'active': active_license,'expired' : expired_license}

@router.get('/search_license',response_model=List[LicenseResponse])
async def search(keyword: str,db:AsyncSession=Depends(get_db)):
    query = await db.execute(select(License).where(
        or_(
            License.license_number.ilike(f"%{keyword}%"),
            License.control_number.ilike(f"%{keyword}%")
        )

    ))
    license = query.scalars().all()
    return license


@router.post('/reg_license',response_model=LicenseResponse)
async def reg_license(request: LicenseCreate,db:AsyncSession=Depends(get_db)):
    new_license = License(
        license_number = request.license_number,
        control_number = request.control_number,
        license_type = request.license_type,
        issue_date = request.issue_date,
        expired_date = request.expired_date,
        user_id =request.user_id
    )
    db.add(new_license)
    await db.commit()
    await db.refresh(new_license)
    return new_license
@router.get('/one_license/{id}',response_model=LicenseResponse)
async def one_license(id: int,db: AsyncSession=Depends(get_db)):
    query = await db.execute(select(License).where(License.id == id))
    license = query.scalars().first()
    return license
