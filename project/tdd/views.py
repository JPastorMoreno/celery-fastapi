import os

from fastapi import Depends, FastAPI, File, Form, UploadFile
from project.config import settings
from project.database import get_db_session
from project.tdd.models import Member
from project.tdd.tasks import generate_avatar_thumbnail
from sqlalchemy.orm import Session

from . import tdd_router


@tdd_router.post("/member_signup/")
def member_signup(
        username: str = Form(...),
        email: str = Form(...),
        upload_file: UploadFile = File(...),
        session: Session = Depends(get_db_session)
):
    """
    https://stackoverflow.com/questions/63580229/how-to-save-uploadfile-in-fastapi
    https://github.com/encode/starlette/issues/446
    """
    file_location = os.path.join(#type:ignore
        settings.UPLOADS_DEFAULT_DEST,
        upload_file.filename,#type:ignore
    )
    with open(file_location, "wb") as file_object:
        file_object.write(upload_file.file.read())

    try:
        member:Member = Member(
            username=username,#type:ignore
            email=email,#type:ignore
            avatar=upload_file.filename,#type:ignore
        )
        session.add(member)
        session.commit()
        member_id = member.id
    except Exception as e:
        session.rollback()
        raise

    generate_avatar_thumbnail.delay(member_id)#type:ignore
    return {"message": "Sign up successful"}