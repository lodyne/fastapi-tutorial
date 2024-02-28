from fastapi import APIRouter, Body, status, HTTPException, Path

from misc.models.post import Post

router = APIRouter(prefix="/posts", tags=["post"])

posts = []


@router.get("/")
async def read_post():
    return {"post": "post"}


@router.get("/{post_id}")
async def read_single_post(post_id: int = Path(...)):
    if post_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return {"post": post_id}

@router.post("/")
async def create_post(post:Post=Body(...)):
    posts.append(post)
    return {"post":"Post have been added"}
    