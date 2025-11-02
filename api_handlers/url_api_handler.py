from fastapi import APIRouter, Body, Depends, HTTPException, Header, Request, Response
from container import Container
from exception_types.wrong_password_exception import WrongPasswordException
from dependency_injector.wiring import Provide, inject
from services.paste_bin_payload_service import PasteBinPayloadService

#create unit tests using pytest and pytest-mock, testcontainers
#use conftest.py
#test_payload_service.py
#add test folder

router = APIRouter()

@router.post("/")
@inject
def shorten_url(service: PasteBinPayloadService = Depends(Provide[Container.paste_bin_payload_service]), payload: bytes = Body(embed=True, default=None), password: str|None = Header(None), should_burn: str|None = Header("123")):

    if payload is None:
        raise HTTPException(status_code=400, detail="bad request")
    
    if not password:
        password = None

    paste_bin_url = service.create_paste_bin(payload, password, should_burn)
    
    return paste_bin_url

@router.get("/{paste_bin_url}")
@inject
def get_original_payload(paste_bin_url: str, service: PasteBinPayloadService = Depends(Provide[Container.paste_bin_payload_service]), password: str|None = Header(None)):
    
    try:
        paste_bin = service.get_paste_bin(paste_bin_url, password)
        if paste_bin is None:
            raise HTTPException(status_code=404, detail="Item not found")
    
    except WrongPasswordException as e: #add not item exception
        raise HTTPException(status_code=401, detail="unauthorized")
    
    return Response(content=paste_bin.payload, media_type="application/octet-stream")
