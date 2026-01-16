from fastapi import APIRouter, HTTPException
from models.user import User, User_Response

router = APIRouter()


users = [
        User(id=1, username= "Alice", email= "alice@foo.com", full_name= "Alice Smith", is_active= True),
        User(id=2, username= "Bob", email= "boob@foo.com", full_name= "Bob Johnson", is_active= True)
        ]

@router.get("/")
def get_users():
    return users

@router.post("/", response_model=User_Response)
def create_user(user: User):
    for existing_user in users:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="User with this ID already exists")
    
    users.append(user)
    return User_Response(id=user.id, full_name=user.full_name)


@router.delete("/{id}", response_model=User_Response)
def delete_user(id: int):
    for idx, user in enumerate(users):
        if user.id == id:
            removed_user = users.pop(idx)
            return removed_user
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/{id}", response_model=User)
def get_user(id: int):
    for user in users:
        if user.id == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
