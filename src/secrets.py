from pydantic import SecretStr


class TheSecret:
    # TODO: can I constrain it?
    # TODO: are those names the best?
    STORAGE_T = SecretStr
    INPUT_T = SecretStr

    @staticmethod
    def hash(secret: SecretStr):
        _secret = secret.get_secret_value()
        return "#" + _secret + " " * (64 - len(_secret) - 1) 

    @staticmethod
    def compare_input_to_digest() -> bool:
        # just for demo purposes
        return False
