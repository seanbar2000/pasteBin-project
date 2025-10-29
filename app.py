from fastapi import Depends, FastAPI
from api_handlers.url_api_handler import router as paste_bin_handler_router
import uvicorn
from dependency_injector.wiring import Provide, inject

from container import Container
from repositories.mongo_repository import MongoRepository
import services.paste_bin_payload_service as service_modlule
app = FastAPI()
@app.get("/todo")
@inject
def shorten_url(default_query: str = Depends(Provide[Container.test_var])):
    print(default_query)      
    return "test worked"

def start_server():
    print('Starting Server...')       
    #container.wire(modules=["api_handlers.url_api,handler"])
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="debug",
    )
    
if __name__ == "__main__":
    container = Container()
    app.container = container
    app.include_router(paste_bin_handler_router, prefix="/paste_bin", tags=["url"])
    container.wire(modules=["api_handlers.url_api_handler", __name__]) # added name of api_handler
    start_server()