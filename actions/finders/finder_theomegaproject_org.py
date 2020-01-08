import threading
import re

from bs4 import BeautifulSoup
from actions.parser import *

def get_navpage_data(application, finder, parser, num, page):
    data = parser.find("div", "content").find_all("div", "white_picture")
    step = round(1.0/len(data), 3)

    i = 0.0

    for item in data:
        if finder.event.is_set() == False:
            return "Stop"

        link    = item.find("a")
        title   = link.attrs['title']
        gallery = link.attrs['href'][1:]
        status  = "unknown"
        span    = item.find("span", "info name")

        if span:
            name = span.find("a").attrs['title']
        else:
            name = "unknown"

        preview = item.find("img").attrs['src'][2:]

        url     = preview
        if url[:7] != "http://":
            url = "http://" + url

        find    = find_image(url)
        if find == False:
            for i in range(10):
                preview = preview.replace()
                url     = re.sub(r"content.", "content" + str(i), url)
                find    = find_image(url)
                if find == True:
                    break

            if find == False:
                application.event_print("Ошибка: изображение не найдено: \nСтраница: " + page + "\nГаллерея: " + title)
                return "Error"

        i = i + step

        if not application.database.select("find", [gallery, "theomegaproject.org", name]):
            result = application.database.insert(gallery, title, "theomegaproject.org", name, preview)
            if result != "Error":
                application.data.records_all  = application.data.records_all + 1
                application.data.records_main = application.data.records_main + 1

                application.event_info()
        application.event_progress(i)                
    application.event_print("Страница: " + str(num), "\r")

    return True

def get_navpage_next(parser):
    next_url = parser.find("div", "pager").find_all("a")[-1]
    if next_url.text == "next >>":
        return "https://www.theomegaproject.org/galleries" + next_url.attrs['href']
    else:
        return None

def start_find_galleries(application, finder):
    page   = "https://www.theomegaproject.org/galleries/galleries?from=1"
    parser = get_parser(application, page)
    if parser:
        num  = 1
        page = get_navpage_next(parser)

        result = get_navpage_data(application, finder, parser, str(num), page)
        if result == False:
            return None
                
        while page:
            if finder.event.is_set() == False:
                break

            application.event_print("Страница: " + str(num), "\r")

            parser = get_parser(application, page)
            if parser:
                result = get_navpage_data(application, finder, parser, str(num), page)
                if result == "Error":
                    break

                page = get_navpage_next(parser)
                num  = num + 1
            else:
                break