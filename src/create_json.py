import json
import os
from glob import glob

# Wappalyzer（https://www.wappalyzer.com/）のGitHub（https://github.com/AliasIO/wappalyzer）をcloneし、
# "wappalyzer/src/technologies/"下のJSONファイルからCDNをカテゴリー番号をもとに抽出した。
# カテゴリー番号は"wappalyzer/src/categories.json"に書いてある。

cdn_json = {}
par_dir_path = os.path.dirname(__file__)
absolute_path_of_json_dir = par_dir_path + "/wappalyzer/src/technologies/"
cdnsfile_path = par_dir_path + "/cdns.json"


jsonfiles_pathlist = glob(absolute_path_of_json_dir + "*.json")

for jsonfile_path in jsonfiles_pathlist:

    with open(jsonfile_path) as f:
        json_all = json.load(f)

    for key in json_all:
        service_val = json_all[key]
        if service_val["cats"] == [31]:
            cdn_json[key] = service_val

with open(cdnsfile_path, "w") as f:
    json.dump(
        cdn_json,
        f,
        ensure_ascii=False,
        indent=4,
        sort_keys=True,
        separators=(",", ": "),
    )
