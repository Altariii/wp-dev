import random
from urllib.request import Request, HTTPCookieProcessor, build_opener
from http.cookiejar import CookieJar

from ..constants import connection
from ..utils import console

def get_source(url: str) -> [str, str, str, str]:
    [response_code, source_code, response_headers, redirect_url] = get_raw_source(url, use_random_user_agent())
    return defy_browser_validation(url, response_code, source_code, response_headers, redirect_url)

def get_raw_source(url: str, user_agent: str) -> [str, str, str, str]:
    if url == "":
        return [connection.INVALID_URL, "Empty URL Provided", "", ""]
    
    try:
        request = Request(url, data = None, headers = { "User-Agent": user_agent } | connection.RAW_REQUEST_HEADERS)
        cookie_jar = CookieJar()
        opener = build_opener(HTTPCookieProcessor(cookie_jar))
        with opener.open(request, timeout=8) as response:
            source_code = response.read().decode("utf-8", "ignore")
            response_headers = str(response.info())
            redirect_url = response.geturl()
            return [connection.OK_RESPONSE, source_code, response_headers, redirect_url]
        
    except Exception as e:
        try:
            exception_code = str(e.code)
            exception_headers = str(e.info())
            return [connection.ERROR_RESPONSE, str(e), exception_code, exception_headers]
        
        except Exception as _:
            return [connection.ERROR_RESPONSE, str(e), "", ""]

def defy_browser_validation(url: str, response_code: str, source_code: str, exception_code: str, exception_headers: str) -> [str, str, str, str]:
    if connection.GOOGLE_HUMAN_RESPONSE in source_code or connection.GOOGLE_CKATTEMPT_RESPONSE in source_code:
        console.display.warning("Browser validation detected. Trying to evade...")
        [new_response_code, new_source_code, new_response_headers, new_redirect_url] = get_raw_source(url, connection.GOOGLEBOT_USER_AGENT)
        if connection.GOOGLE_CKATTEMPT_RESPONSE in new_source_code:
            console.display.error("Failed to evade Browser validation. Results might not be accurate!")
        else:
            console.display.success("Browser validation successfully evaded.")
        return [new_response_code, new_source_code, new_response_headers, new_redirect_url]

    if connection.AES_JS in source_code and connection.I_1 in source_code:
        console.display.warning("Browser validation detected. Trying to evade...")
        [new_response_code, new_source_code, new_response_headers, new_redirect_url] = get_raw_source(url, connection.GOOGLEBOT_USER_AGENT)
        if connection.AES_JS in new_source_code and connection.I_1 in new_source_code:
            console.display.error("Failed to evade Browser validation. Results might not be accurate!")
        else:
            console.display.success("Browser validation successfully evaded.")
        return [new_response_code, new_source_code, new_response_headers, new_redirect_url]
    
    if exception_code == connection.FORBIDDEN and (connection.BOT_UA_RESPONSE in exception_headers or connection.WARNING_199 in exception_headers):
        console.display.warning("User Agent validation detected. Trying to evade...")
        [new_response_code, new_source_code, new_exception_code, new_exception_headers] = get_raw_source(url, connection.GOOGLEBOT_USER_AGENT)
        if connection.BOT_UA_RESPONSE in new_exception_code or connection.WARNING_199 in new_exception_code:
            console.display.error("Failed to evade Browser validation. Results might not be accurate!")
        else:
            console.display.success("Browser validation successfully evaded.")
        return [new_response_code, new_source_code, new_exception_code, new_exception_headers]
    
    return [response_code, source_code, exception_code, exception_headers]

def use_random_user_agent() -> str:
    return random.choice(connection.USER_AGENTS)