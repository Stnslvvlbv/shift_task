import uvicorn
from fastapi import APIRouter, FastAPI

from src.logger import error_middleware
from src.position.position_handlers import position_router
from src.salary.salary_handlers import salary_router
from src.user.user_handlers import user_router

app = FastAPI(title="SHIFT task salary service")


# Регистрируем middleware
app.middleware("http")(error_middleware)

main_api_router: APIRouter = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(position_router, prefix="/position", tags=["position"])
main_api_router.include_router(salary_router, prefix="/salary", tags=["salary"])


app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
