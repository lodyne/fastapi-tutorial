from fastapi import APIRouter, status, HTTPException, Path

from misc.models.comment import Comment


router = APIRouter(
    prefix="/comment",
    tags=["comment"],
)

comments = []


@router.get("/")
async def read_comments():
    return {"comment": comments}


@router.get("/{comment_id}")
async def read_single_comment(
    comment_id: int = Path(...),
):
    for comment in comments:
        if comment_id == comment.id:
            return {"comment": comment}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
    )


@router.post("/")
async def create_comments(comment: Comment):
    comments.append(comment)
    return {"comment": comment, "message": "Comment has been added"}
