from starkbank import Project
from app.core.config import settings


def get_user() -> Project:
    user = Project(
        environment=settings.PROJECT_ENV,
        id=settings.PROJECT_ID,
        private_key=settings.starkbank_private_key,
    )


    return user
# 