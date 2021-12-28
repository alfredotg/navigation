from users.types import Response

def raise_on_errors(response : Response):
    if response.status_code >= 200 and response.status_code <= 299:
        return
    raise Exception("API returned error: %d %s" % (response.status_code, str(response.content)))
