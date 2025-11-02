import pymongo
import os
from dotenv import load_dotenv
from repositories.mongo_repository import MongoRepository
from services.paste_bin_payload_service import PasteBinPayloadService
from dependency_injector import containers, providers

load_dotenv()

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    db_client = providers.Singleton(
        pymongo.MongoClient,
        os.getenv("DBCLIENTURL"),
    )

    repository = providers.Singleton(
        MongoRepository,
        db_client= db_client
    )
    paste_bin_payload_service = providers.Singleton(
        PasteBinPayloadService,
        repository=repository,
    )
    test_var = providers.Factory(str, "Hello from DI!")
