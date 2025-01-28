import strawberry

@strawberry.type
class Note:
    id: int
    content: str