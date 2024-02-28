from fastapi import Header, status, HTTPException


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="token header invalid"
        )

async def get_query_token(token:str):
    if token != "jessy":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="token header invalid"
        )