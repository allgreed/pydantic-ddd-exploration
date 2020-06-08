from starlette.responses import Response


def status_204(f, *args, **kwargs):
    """
    Workaround for returning 204 with actual no content

    details: https://github.com/tiangolo/fastapi/issues/449
    """

    kwargs.update({
        "status_code": 204,
        "response_class": Response,
    })

    return f(*args, **kwargs)


def hash_password(raw: str) -> str:
    return "#" + raw


def compare_password_with_digest(raw: str, digest: str) -> bool:
    return hash_password(raw) == digest
