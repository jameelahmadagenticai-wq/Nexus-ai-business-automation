from fastapi import APIRouter

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.get("/")
async def get_agents():
    return {"message": "Agents route working"}