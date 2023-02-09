from urllib.parse import urlparse
import re


def parse_host(ip, api):

    if not isinstance(ip, list):
        return api
    if not api:
        return api
    try:
        parts = urlparse(api["request"]["url"])
    except KeyError:
        parts = urlparse(api["request"]["base_url"])
    # 返回值是Host:port
    host = parts.netloc
    host = host.split(':')[0]
    if host:
        for content in ip:
            content = content.strip()
            if host in content and not content.startswith("#"):
                ip = re.findall(r'\b(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b', content)
                # ip = re.findall(
                # r'\b(?:25[0-5]\.|2[0-4]\d\.|[01]?\d\d?\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b:\d{0,5}', content)
                if ip:
                    if "headers" in api["request"].keys():
                        api["request"]["headers"]["Host"] = host
                    else:
                        api["request"].setdefault("headers", {"Host": host})
                    try:
                        api["request"]["url"] = api["request"]["url"].replace(host, ip[-1])
                    except KeyError:
                        api["request"]["base_url"] = api["request"]["base_url"].replace(host, ip[-1])
    return api
