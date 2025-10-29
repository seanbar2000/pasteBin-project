from fastapi import APIRouter, Body, Depends, HTTPException, Header, Request, Response
from container import Container
from exception_types.wrong_password_exception import WrongPasswordException
from dependency_injector.wiring import Provide, inject
from services.paste_bin_payload_service import PasteBinPayloadService


router = APIRouter()

@router.post("/")
@inject
def shorten_url(service: PasteBinPayloadService = Depends(Provide[Container.paste_bin_payload_service]), payload: bytes = Body(embed=True, default=None), password: str|None = Header(None), should_burn: bool|None = Header(None)):

    if payload is None:
        raise HTTPException(status_code=400, detail="bad request")
    
    paste_bin_url = service.create_paste_bin(payload, password, should_burn)
    
    return paste_bin_url

#change bool to is_--- or should_--- like should_burn or is_locked
@router.get("/{paste_bin_url}")
@inject
def get_original_payload(paste_bin_url: str, service: PasteBinPayloadService = Depends(Provide[Container.paste_bin_payload_service]), password: str|None = Header(None)):
    
    try:
        paste_bin = service.get_paste_bin(paste_bin_url, password)
        if paste_bin is None:
            raise HTTPException(status_code=404, detail="Item not found")
    
    except WrongPasswordException as e:
        raise HTTPException(status_code=401, detail="unauthorized")
    
    return Response(content=paste_bin.payload, media_type="application/octet-stream")
