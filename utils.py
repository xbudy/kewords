from tld import get_tld
import validators

def isUrl(string) -> bool:
    return validators.url(string)