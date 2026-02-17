from fastapi import FastAPI
from services.file_handler import FileHandler
from services.questions import Questions
from services.users import Users
from routers import admin_services, user_services, auth_login
from loggers.logger import configure_logger

app = FastAPI(
    title="Quiz API",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    """
    Initialize shared resources once when the application starts.
    """
    try:
        fh = FileHandler()
        app.state.user_obj = await Users.create(fh)
        app.state.questions_obj = await Questions.create(fh)
        configure_logger()

    except FileNotFoundError as e:
        raise RuntimeError("Required data files not found during startup") from e

    except Exception as e:
        raise RuntimeError("Unexpected error during application startup") from e


# Register routers
app.include_router(admin_services.router)
app.include_router(user_services.router)
app.include_router(auth_login.router)
