from urllib.parse import urljoin, quote_plus


def multi_urljoin(*parts):
    return urljoin(parts[0], "/".join(quote_plus(part.strip("/"), safe="/") for part in parts[1:]))
