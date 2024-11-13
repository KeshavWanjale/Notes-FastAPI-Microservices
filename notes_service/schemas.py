def note_entity(item):
    return {
        "id":str(item["_id"]),
        "title":item["title"],
        "description":item["description"],
        "color":item["color"],
        "user_id":item["user_id"]
    }

def note_entities(entity):
    return [note_entity(item) for item in entity]