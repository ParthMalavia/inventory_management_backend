from fastapi import Depends, HTTPException  # , status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.utils.auth import decode_access_token, oauth2_scheme


# Function to get the current user from the JWT token
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserResponse:
    # Decode the JWT token to extract the payload
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Extract username (subject) from the token payload
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Token has no user information")

    # Query the user from the database
    db_user = db.query(User).filter(User.username == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=401, detail="User not found")

    # Return the user details
    return db_user
