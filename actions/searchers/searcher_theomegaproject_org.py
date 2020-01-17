import threading
import re

from bs4 import BeautifulSoup
from actions.parser import *

def get_page(application, searcher, url, gallery, index, name):
    if not searcher.event.is_set():
        return "Stop"

    parser = get_parser(application, url)

    image  = None
    links  = []
    find   = False

    if parser:
        for item in parser.find("h2", {"class": "info"}).find_all("a"):#, text="Full Size Image"):
            link = item.attrs['href']
            if link[-4:] == ".jpg":
                if link[:2] == "//":
                    link = link[2:]
                    link = "https://content0.fwwgo.com" + link[link.index("/"):]

                if not link in links:
                    if re.search(r".*orig_.*\.jpg", link):
                        image = link
                        find  = True
                        break
                    else:
                        links.append(link)

        if find == False:
            base_url = parser.find("div", {"class": "postholder"}).find("img", {"id": "big_picture"}).attrs['src']
            if base_url[:2] == "//":
                link = base_url[2:]
                link = "https://content0.fwwgo.com" + link[link.index("/"):]

            if not link in links:
                if re.search(r".*orig_.*\.jpg", link):
                    image = link
                else:
                    links.append(link)

        if not image and len(links) > 0:
            image = links[0]

        if image:
            if index < 10:
                index = "0" + str(index)
            else:
                index = str(index)

            if len(gallery) > 20:
                gallery = gallery[:20]

            if not searcher.event.is_set():
                return "Stop"

            result    = find_image(image)
            if result == True:
                return image
            elif result == False:
                for i in range(10):
                    image  = re.sub(r"content.", "content" + str(i), image)
                    result = find_image(image)
                    if result == True:
                        return image
                    
                if result == False:
                    application.event_print("Изображение не найдено: " + image)
                    return "Error"
        else:
            application.event_print("Изображение не найдено: " + image)
            return "Error"

def get_tags(parser):
    tags    = None
    taglist = parser.find(text=re.compile("Tags:.*")).parent.findAll("a")
    if len(taglist) > 0:
        for tag in taglist:
            if tags:
                tags = tags + ", #" + tag.text.replace(" ", "-")
            else:
                tags = "#" + tag.text.replace(" ", "-")

    return tags

def start_search_images(application, searcher, url, gallery, title, name):
    images  = None
    image   = ""
    index   = 0
    tags    = None
    parser  = get_parser(application, url)
    i = 0.0
    if parser:
        tags  = get_tags(parser)
        div   = parser.find("div", {"class" : "postholder"})
        if div:
            data = div.find_all("div", "picture", recursive=False)
            step = round(1.0/len(data), 3)
            for item in data:
                index  = index + 1
                page   = "https://www.theomegaproject.org" + item.find("a").attrs['href']
                image  = get_page(application, searcher, page, gallery, index, name)
                if image != "Error" and image != "Stop":
                    if images and type(images) == str and len(images) > 0:
                        images = images + " " + image
                    else:
                        images = image

                    application.event_progress(i)

                elif image == "Stop":
                    return "Stop"

                application.event_print("Найдено: " + name + " - " + title[:25] + "[" + str(index) + "]", "\r")
                i = i + step
        else:
            div = parser.find("div", {"class" : "omega-images"})
            if div:
                data = div.findAll("span")
                step = round(1.0/len(data), 3)
                for item in data:
                    index = index + 1
                    page  = "https://www.theomegaproject.org" + item.find("a").attrs['href']
                    image = get_parser(application, page).find("a").find("img").attrs['src']
                    path  = application.data.pathimgs + '/' + name
                    filename = image[image.rindex("/"):]

                    if image:
                        if image[:2] == "//":
                            image = "https:" + image

                        application.event_progress(i)
                        i = i + step

                        result = find_image(image)
                        if result == True:
                            if images and type(images) == str and len(images) > 0:
                                images = images + " " + image
                            else:
                                images = image
                            application.event_print("Найдено: " + name + " - " + title[:25] + "[" + str(index) + "]", "\r")
                        #else:
                        #    application.event_print("Найдено: "
                        
                    if not searcher.event.is_set():
                        return "Stop"
        
        if images:
            return [images, tags]
        else:
            return "Error"
