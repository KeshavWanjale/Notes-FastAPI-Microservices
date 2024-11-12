from fastapi import APIRouter, HTTPException, status
from config import user_collection
from .models import RegisterUser, LoginUser
from .utils import hash_password, verify_password

user_routes = APIRouter()

@user_routes.get("/")
def greet():
    return {"message": "Welcome to user service"}

@user_routes.post("/register")
def register_user(user: RegisterUser):
    try:
        existing_user = user_collection.find_one({"email":user.email})

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_password = hash_password(user.password)
        user_dict = dict(user)
        user_dict["password"] = hashed_password
        response = user_collection.insert_one(user_dict)
        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "Employee created successfully",
            "data": {"id": str(response.inserted_id)}
        }
    except Exception as e: 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {e}"
        )
    
@user_routes.post("/login")
def login_user(data: LoginUser):
    try:
        user = user_collection.find_one({"email": data.email})

        if user:
            if verify_password(data.password, user["password"]):
                return {"message": "Login successful", "status": "success"}
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Login Failed. Invalid Password"
            )
            
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid User Credentials"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {e}"
        )