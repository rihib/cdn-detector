from pathlib import Path
import dns.resolver
import json
import requests
import subprocess


BASE_DIR = Path(__file__).resolve().parent
CDNS_JSON = str(BASE_DIR.joinpath("cdns.json"))
REGEX = str(BASE_DIR.joinpath("regex.js"))

class JsRegex:
    def main(self, target, regex):
        result_byte = subprocess.check_output(
            [
                "node",
                REGEX,
                target,
                regex,
            ]
        )
        result = int(result_byte.decode().replace("\n", ""))
        return result

class GetData:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url)

    def get_dns(self, record_data_type):
        rdata_list = []
        url = self.url.replace("https://", "").replace("https://", "").split("/", 1)[0]
        try:
            answers = dns.resolver.resolve(url, record_data_type)
            for rdata in answers:
                rdata_list.append(str(rdata))
        except:
            pass
        return rdata_list

    def get_headers(self):
        headers = self.response.headers
        return headers

    def get_cookies(self):
        a_session = requests.Session()
        a_session.get(self.url)
        session_cookies = a_session.cookies
        cookies = session_cookies.get_dict()
        return cookies

class DetectCDN(GetData):
    def __init__(self, cdn_fields, cdn, url):
        self.js_regex = JsRegex()
        super().__init__(url)
        self.cdn_fields = cdn_fields
        self.cdn = cdn
        self.headers = super().get_headers()
        self.cookies = super().get_cookies()
        self.url = url

    def main(self):
        cdns_result_set = set()
        func_list = [
            self.detect_by_dns,
            self.detect_by_headers,
            self.detect_by_cookies,
            self.detect_by_url,
        ]
        for func in func_list:
            result = func()
            if result:
                cdns_result_set.add(result)
        return cdns_result_set

    def detect_by_dns(self):
        if "dns" in self.cdn_fields:
            dns_fields = self.cdn_fields["dns"]
            for dns_field in dns_fields:
                rdata_list = super().get_dns(dns_field)
                for rdata in rdata_list:
                    result = self.js_regex.main(
                        rdata,
                        dns_fields[dns_field],
                    )
                    if result:
                        return self.cdn

    def detect_by_headers(self):
        if "headers" in self.cdn_fields:
            headers_fields = self.cdn_fields["headers"]
            for headers_field in headers_fields:
                # headers属性はCaseInsensitiveDictという型．基本的には辞書（dict型）だが，大文字と小文字を区別しないという特徴がある．
                if headers_field in self.headers:
                    result = self.js_regex.main(
                        self.headers[headers_field],
                        headers_fields[headers_field],
                    )
                    if result:
                        return self.cdn

    def detect_by_cookies(self):
        if "cookies" in self.cdn_fields:
            cookies_fields = self.cdn_fields["cookies"]
            for cookies_field in cookies_fields:
                if cookies_field in self.cookies:
                    return self.cdn

    def detect_by_url(self):
        if "url" in self.cdn_fields:
            result = self.js_regex.main(self.url, self.cdn_fields["url"])
            if result:
                return self.cdn

def main(url):
    with open(CDNS_JSON) as f:
        cdns_json = json.load(f)
    cdns_result_sets = set()
    for cdn in cdns_json:
        cdn_fields = cdns_json[cdn]
        detect_cdn = DetectCDN(cdn_fields, cdn, url)
        cdns_result_set = detect_cdn.main()
        cdns_result_sets.update(cdns_result_set)
    cdns_result_list = list(cdns_result_sets)
    return cdns_result_list

if __name__ == "__main__":
    URL = input("Please enter URL: ")
    with open(CDNS_JSON) as f:
        cdns_json = json.load(f)
    cdns_result_sets = set()
    for cdn in cdns_json:
        cdn_fields = cdns_json[cdn]
        detect_cdn = DetectCDN(cdn_fields, cdn, URL)
        cdns_result_set = detect_cdn.main()
        cdns_result_sets.update(cdns_result_set)
        print("Please wait...")
    if len(cdns_result_sets) == 0:
        print("CDN is not detected.")
    else:
        print(', '.join(cdns_result_sets))
