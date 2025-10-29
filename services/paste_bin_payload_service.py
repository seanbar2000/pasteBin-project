from models.item import Item
import time
import bcrypt
from exception_types.wrong_password_exception import WrongPasswordException
from repositories.mongo_repository import MongoRepository
#the convention says to raise a specific exception for the service and not httpexception or other exception
#so that the server that uses the service can be of any type and not only http
class PasteBinPayloadService:
    #repository should be with dependancy_injector (depends(provide))
    def __init__(self, repository: MongoRepository):
        self.repository = repository
        self.password_salt = bcrypt.gensalt()

    def create_paste_bin(self, payload: bytes, password: str|None, should_burn: bool|None)-> str:
        #we could raise exception for None password or assert password is not None, "Password! cannot be None"
        #we could catch in upper place or let it crash the app, someone needs to send a bad request exception
        hashed_password = password
        if password is not None:
            encoded_password = password.encode("utf-8")
            hashed_password = bcrypt.hashpw(encoded_password, self.password_salt)
        item = self.create_item(payload=payload, password=hashed_password, burn=should_burn)
        paste_bin_url = self.repository.add_paste_bin_to_db(item)
        return paste_bin_url

    def create_item(self, payload: bytes, password, should_burn: bool)-> Item:
        created_at = time.time()
        expiration = None if (should_burn == True) else created_at + 180.0
        paste_bin = Item(payload=payload, created_at=created_at, expiration=expiration, burn=should_burn, password=password)
        return paste_bin
    
    def get_paste_bin(self, paste_bin_url: str, password="")-> Item|None:
        #if you didn't manage to unlock the password:
        #1. get_paste_bin -> PasteBinResult (PasteBinResult.error_code PasteBinResult.error_text)
        #meaning encapsolate Item inside pasteBinResult which has item and error_code
        #2. throw exception (endpoint catches)
        #(1) raise fastapi.exceptions.NotFoundError
        #(2) raise MyNotFoundError("some details") (custom error with details)
        paste_bin = self.repository.get_paste_bin(paste_bin_url)
        #could assert paste_bin != None
        #
        if not paste_bin:
            return None #assert
        else:     
                   
            if paste_bin.password:
                if self.validate_password(password, paste_bin):
                    if paste_bin.burn or paste_bin.is_expired():
                        self.repository.delete_item(paste_bin_url)
                    return paste_bin
                else:
                    raise WrongPasswordException()
            else:
                if paste_bin.burn or paste_bin.is_expired():
                    self.repository.delete_item(paste_bin_url)
        return paste_bin
    
    def validate_password(self, password, paste_bin: Item)-> bool:
        encoded_password = password.encode("utf-8")
        return bcrypt.checkpw(encoded_password, paste_bin.password)