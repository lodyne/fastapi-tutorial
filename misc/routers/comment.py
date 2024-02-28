from fastapi import APIRouter, FastAPI, HTTPException, Path


router = APIRouter(
    prefix="/comment",
    tags=["comment"],
)


@router.get("/")
async def read_comments():
    return {"comment": "comment"}


@router.get("/{comment_id}")
async def read_single_comment(comment_id: str = Path(...)):
    if comment_id is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"comment": comment_id}
