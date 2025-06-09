Python 3.13.0 (tags/v3.13.0:60403a5, Oct  7 2024, 09:38:07) [MSC v.1941 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import ipaddress
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import whois
... from datetime import date
... 
... 
... class FeatureExtraction:
...     def _init_(self, url):
...         self.url = url
...         self.domain = ""
...         self.whois_response = None
...         self.urlparse = urlparse(url)
...         self.response = None
...         self.soup = None
... 
...         try:
...             self.response = requests.get(url, timeout=10)
...             self.soup = BeautifulSoup(self.response.text, 'html.parser')
...         except requests.RequestException:
...             self.response = None
...             self.soup = None
... 
...         try:
...             self.domain = self.urlparse.netloc
...             self.whois_response = whois.whois(self.domain)
...         except:
...             self.whois_response = None
... 
...     def UsingIp(self):
...         try:
...             ipaddress.ip_address(self.url)
...             return -1
...         except ValueError:
...             return 1
... 
...     def longUrl(self):
...         if len(self.url) < 54:
...             return 1
...         elif 54 <= len(self.url) <= 75:
...             return 0
...         return -1
... 
...     def shortUrl(self):
...         shorteners = (
...             "bit.ly", "goo.gl", "tinyurl.com", "ow.ly", "t.co", "bit.do", "cutt.ly", "is.gd", "v.gd", "shorte.st"
...         )
...         if any(shortener in self.url for shortener in shorteners):
...             return -1
        return 1

    def symbol(self):
        return -1 if "@" in self.url else 1

    def redirecting(self):
        return -1 if self.url.find("//", 7) != -1 else 1

    def prefixSuffix(self):
        return -1 if "-" in self.domain else 1

    def SubDomains(self):
        subdomains = self.domain.split(".")
        if len(subdomains) <= 2:
            return 1
        elif len(subdomains) == 3:
            return 0
        return -1

    def Hppts(self):
        return 1 if self.urlparse.scheme == "https" else -1

    def DomainRegLen(self):
        try:
            if self.whois_response and self.whois_response.expiration_date:
                expiration_date = (
                    self.whois_response.expiration_date[0]
                    if isinstance(self.whois_response.expiration_date, list)
                    else self.whois_response.expiration_date
                )
                if expiration_date:
                    reg_length = (expiration_date - date.today()).days
                    return 1 if reg_length >= 365 else -1
        except:
            pass
        return -1

    def Favicon(self):
        try:
            for link in self.soup.find_all('link', rel="icon", href=True):
                if self.domain in link['href']:
                    return 1
            return -1
        except:
            return -1

    def NonStdPort(self):
        return -1 if ":" in self.domain.split(":")[1:] else 1

    def HTTPSDomainURL(self):
        return -1 if "https" in self.domain else 1

    def RequestURL(self):
        try:
            total = len(self.soup.find_all(["img", "audio", "embed", "iframe"], src=True))
            external = sum(1 for tag in self.soup.find_all(["img", "audio", "embed", "iframe"], src=True)
                           if self.domain not in tag['src'])
            percentage = (external / total) * 100 if total else 0
            if percentage < 22:
                return 1
            elif percentage <= 61:
                return 0
            return -1
        except:
            return -1

    def AnchorURL(self):
        try:
            total = len(self.soup.find_all('a', href=True))
            unsafe = sum(1 for a in self.soup.find_all('a', href=True)
                         if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower())
            percentage = (unsafe / total) * 100 if total else 0
            if percentage < 31:
                return 1
            elif percentage <= 67:
                return 0
            return -1
        except:
            return -1

    def getFeaturesList(self):
        return [
            self.UsingIp(),
            self.longUrl(),
            self.shortUrl(),
            self.symbol(),
            self.redirecting(),
            self.prefixSuffix(),
            self.SubDomains(),
            self.Hppts(),
            self.DomainRegLen(),
            self.Favicon(),
            self.NonStdPort(),
            self.HTTPSDomainURL(),
            self.RequestURL(),
            self.AnchorURL(),
        ]

    def classify(self):
        # Get feature list
        features = self.getFeaturesList()
        # Calculate score (sum of features)
        score = sum(features)
        # Threshold for classification
        return "Not Phishing" if score > 0 else "Phishing"


if _name_ == "_main_":
    # Test URLs
    urls = [
        "https://mail.google.com",
        "http://bit.ly/3pZJdYN",
        "http://example.com@malicious.com",
        "http://phish-site.com",
        "http://192.168.1.1",
        "http://example.com",
        "http://example.com:8080"
    ]

    for url in urls:
        features = FeatureExtraction(url)
        print(f"URL: {url}")
        print(f"Features: {features.getFeaturesList()}")
        print(f"Classification: {features.classify()}")
