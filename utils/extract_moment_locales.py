from json import dumps
from os import walk
from os.path import dirname, isdir, join, abspath

moment_locale_directory = join(dirname(dirname(abspath(__file__))), "node_modules", "moment", "src", "locale")

long_date_format_parts = (
    r"LT : '",
    r'LT : "',
    r"LTS : '",
    r'LTS : "',
    r"L : '",
    r'L : "',
    r"LL : '",
    r'LL : "',
    r"LLL : '",
    r'LLL : "',
    r"LLLL : '",
    r'LLLL : "',
)

locales = {}

if isdir(moment_locale_directory):
    for root, dirs, files in walk(moment_locale_directory):
        for file in files:
            if file.endswith(".js"):
                with open(join(root, file), "r", encoding="utf-8") as locale:
                    long_date_format = {}
                    for line in locale.readlines():
                        for part in long_date_format_parts:
                            if line.strip().startswith(part):
                                line = line.strip()

                                if part.endswith('"'):
                                    key = part.rstrip(' :"')
                                    value = line.lstrip(part).rstrip('", ')
                                else:
                                    key = part.rstrip(" :'")
                                    value = line.lstrip(part).rstrip("', ")

                                long_date_format[key] = value

                        if long_date_format:
                            locale_name = file.replace(".js", "")
                            locales[locale_name] = long_date_format
                            if locale_name == "en-gb":
                                locales["en"] = long_date_format

with open(join(moment_locale_directory, "extracted.js"), "w", encoding="utf-8") as outfile:
    outfile.write("export const locales = " + dumps(locales, ensure_ascii=False, sort_keys=True, indent=4))
