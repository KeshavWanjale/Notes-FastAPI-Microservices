from fastapi import FastAPI, HTTPException, status
from config import notes_collection
from .models import NoteCreate, NoteUpdate
from .schemas import note_entities
from bson import ObjectId
import httpx


note_routes = FastAPI()

@note_routes.get("/greet")
def greet():
    return {"message": "Welcome to note service"}

@note_routes.post("/", status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate):
    response = httpx.get(url=f"http://localhost:8000/users?user_id={note.user_id}")
    print(response.status_code)
    if response.status_code == 200:
        note_data = dict(note)
        result = notes_collection.insert_one(note_data)
        return {
            "message": "Note created successfully",
            "id": str(result.inserted_id)
        }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@note_routes.get("/")
def get_notes():
    data = notes_collection.find()
    notes = note_entities(data)
    return {
        "status_code": status.HTTP_200_OK,
        "message": "Notes retrieved successfully",
        "data": notes
    }

@note_routes.put("/{id}")
def update_note(id: str, note: NoteUpdate):
    try: 
        note_id = ObjectId(id)
        update_result = notes_collection.update_one(
            {"_id": note_id},
            {"$set": dict(note)}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )
        return {
            "status_code": status.HTTP_200_OK,
            "message": "Notes updated successfully",
            "data": {"id": id}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {e}"
        )
    
@note_routes.delete("/{id}")
def delete_note(id: str):
    try:
        delete_result = notes_collection.delete_one({"_id": ObjectId(id)})
        
        if delete_result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found"
            )

        return {
            "status_code": status.HTTP_204_NO_CONTENT,
            "message": "Note deleted successfully",
            "data": {}
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred: {e}"
        )