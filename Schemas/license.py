from pydantic import BaseModel
from datetime import date
# hii sababu ni pydentic ni tofauti na  Models.databae
class LicenseCreate(BaseModel):
    license_number: str
    control_number: str
    license_type: str
    issue_date: date
    expired_date: date
    user_id: int

class LicenseResponse(BaseModel):
    id: int
    license_number: str
    control_number: str
    license_type: str
    issue_date: date
    expired_date: date
    user_id: int
    status: str
