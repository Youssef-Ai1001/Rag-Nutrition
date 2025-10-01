from helpers.config import get_settings

class BaseDataModel():
    
    def __init__(self, db_client: str):
        self.db_client = db_client
        self.app_setting = get_settings()