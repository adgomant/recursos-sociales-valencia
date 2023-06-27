# -*- coding: utf-8 -*-

import lxml
import re
import json
import time
import requests as req
from bs4 import BeautifulSoup
from unidecode import unidecode

class SocialCentre:
    def __init__(self, url:str):
        """ """
        self.url = url
        self.content = None
        self.name = None
        self.descr = None
        self.address = None
        self.postalcode = None
        self.phone = None
        self.fax = None
        self.mail = None
        self.website = None
        
    def _get_info(self, soup):
        name = unidecode(soup.h2.text.lower().strip())
        descr = soup.find("div", attrs={"class":"listas-ckeditor"}).text
        return name, descr
    
    def _get_location(self, soup):
        items = soup.ul.find_all("li")
        if len(items) < 2:
            return '', ''
        p1, p2, *_ = items
        postcd, *city = re.sub("\s+", " ", p2.text).strip().split(", ")
        if city:
            city = city[0].capitalize()
        else:
            city = 'València'
        addr = ", ".join([p1.text.title(), postcd, city, "España"])
        return addr, postcd
        
    def _get_contact(self, soup):
        contact_info = unidecode(soup.ul.text.lower())
        phone = [ 
            re.sub("[\s\.]", "", p) 
            for p in re.findall("telefono?: (?:\+\d{2})?\s?((?:\d{2,3}[\s\.]?)+)", contact_info)
        ]
        mail = re.findall("corre[ou] electr\w+: (\S+)", contact_info)
        website = re.findall("\w+ web: (\S+)", contact_info)
        return phone, mail, website
        
    def scrape(self):
        resp = req.get(self.url)
        if resp.status_code // 100 != 2: return
        soup = BeautifulSoup(resp.content, 'lxml')
        content = soup.find("div", attrs={"class":"tab-content"})
        self.content = content.text
        general = soup.find("div", attrs={"id":"general"})
        self.name, self.descr = self._get_info(general)
        self.phone, self.mail, self.website = self._get_contact(general)
        self.address, self.postalcode = self._get_location(general)
        
    def to_dict(self):
        return {
            "name": self.name,
            "short_description": self.descr,
            "address": self.address,
            "postcode": self.postalcode,
            "phone": self.phone,
            "mail": self.mail,
            "website": self.website,
            "content": self.content,
        }


def crawler(save_path="../data/social_centres.json", verbose=True):
    sites, counter_id = {}, 0

    infociudad_url = "https://www.valencia.es"
    search_url = "https://www.valencia.es/web/guest/cas/infociudad/-/categories"

    start_url = search_url + "/37663"
    resp = req.get(start_url)
    if resp.status_code // 100 == 2:
        soup =  BeautifulSoup(resp.content, 'lxml')
        resources = soup.find_all("div", attrs={"class":"col-md-5 col-sm-12 recurso"})
        for resrc in resources:
            resrc_theme = unidecode(resrc.h3.text.lower())
            resrc_theme = re.sub(r"[\n\t]", "", resrc_theme)
            if verbose: print(f"crawling social resources for: {resrc_theme}")
            resrc_href = resrc.a.attrs["href"]
            if resrc_href.startswith("/-/"):
                sc_url = infociudad_url + resrc_href
                if verbose: print(sc_url)
                # create social centre object
                sc = SocialCentre(sc_url)
                # scrape web information
                sc.scrape()
                # save site
                sc_dict = sc.to_dict()
                sc_dict["id"] = counter_id
                counter_id += 1
                sc_dict["theme"] = ''
                sites[sc_url] = sc_dict
            else:
                resrc_url = search_url + "/" + resrc_href
                resrc_resp = req.get(resrc_url)
                if resrc_resp.status_code // 100 == 2:
                    rsrc_soup = BeautifulSoup(resrc_resp.content, 'lxml')
                    social_centres = rsrc_soup.find_all("div", attrs={"class":"col-md-5 col-sm-12 recurso"})
                    for scentre in social_centres:
                        #sc_name = unidecode(scentre.h3.text.lower())
                        #sc_name = re.sub(r"[\n\t]", "", sc_name)
                        sc_href = scentre.a.attrs["href"]
                        sc_url = infociudad_url + sc_href
                        if verbose: print(sc_url)
                        # create social centre object
                        sc = SocialCentre(sc_url)
                        # scrape web information
                        sc.scrape()
                        # save site
                        sc_dict = sc.to_dict()
                        sc_dict["id"] = counter_id
                        counter_id += 1
                        sc_dict["theme"] = resrc_theme
                        sites[sc_url] = sc_dict

        # save sites as json for further indexing
        with open(save_path, "w+", encoding="utf-8") as f:
            json.dump(sites, f, ensure_ascii=False, indent=4)


if __name__=="__main__":
    if len(sys.argv) > 1:
        crawler(sys.argv[1])
    else:
        crawler()
