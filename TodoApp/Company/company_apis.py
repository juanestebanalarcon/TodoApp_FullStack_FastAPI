from fastapi import APIRouter

router = APIRouter(prefix="/Companies",tags=["companies"],responses={418:{"description":"Internal use only"}})

@router.get("/")
async def get_company_name():
    return {"company_name":"JEAM"}
@router.get("/employees")
async def number_of_employees():
    return 600
