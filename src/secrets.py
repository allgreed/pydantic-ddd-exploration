from pydantic import SecretStr
from sqlalchemy import String


class TheSecret:
    """A hashed secret"""
    # TODO: can I constrain it?
    DigestType = SecretStr
    RawType = SecretStr
    SqlDbType = String(length=60)

    @staticmethod
    def hash(secret: SecretStr):
        _secret = secret.get_secret_value()
        return "#" + _secret + " " * (64 - len(_secret) - 1) 

    @staticmethod
    def compare_raw_to_digest(raw: RawType, digesst: DigestType) -> bool:
        # just for demo purposes
        return False

    @staticmethod
    def db_from_core(core_secret: DigestType):
        return core_secret.get_secret_value()

    @staticmethod
    def core_from_db(db_secret: str):
        return DigestType(db_secret)
