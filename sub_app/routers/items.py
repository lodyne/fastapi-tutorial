from fastapi import APIRouter, status, Depends, HTTPException

from sub_app.dependecies import get_token_header


router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


fake_items_db = {"team": {"name": "Man United"}, "coach": {"name": "Ten Hag"}}


@router.get("/")
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "team":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you can only update item:team",
        )
    return {"item_id": item_id, "name": "Red Devils"}
