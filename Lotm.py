import requests
import bs4
import help

def aliases(name: str):
    name = help.capitalize_except_unwanted_words(name).replace(" ", "_")
    print(name.split())
    url = f"https://lordofthemysteries.fandom.com/wiki/{name}"
    print(url)
    r = requests.get(url)
    print(r)
    x = bs4.BeautifulSoup(r.text , 'html.parser')
    aliases = []
    for head in x.find_all("h3"):
        if head.text == "Aliases":
                for li in head.parent.find_all("li"):
                    print(li.text)
                    try:
                        text = li.text[:li.text.index("[")]
                    except ValueError:
                        text = li.text
                    aliases.append(text)
    print(aliases)
    if len(aliases) == 0:
        return None
    return aliases

def pathways(name : str):
    name = help.capitalize_except_unwanted_words(name).replace(" ", "_")
    print(name)
    url = f"https://lordofthemysteries.fandom.com/wiki/{name}"
    r = requests.get(url)
    x = bs4.BeautifulSoup(r.text , 'html.parser')
    pathways = []
    head = x.find("h3" , string = 'Pathway(s)')
    for a in head.parent.find_all("a"):
        if not a.text == '':
            text = a.text[:a.text.index("[")]
            pathways.append(text)
        if "[" not in a.text:
            pathways.append(a.text)
    if len(pathways) == 0:
        return None
    return pathways

def authorities(name : str):
    name = help.capitalize_except_unwanted_words(name).replace(" ", "_").strip()
    print(name)
    url = f"https://lordofthemysteries.fandom.com/wiki/{name}"
    r = requests.get(url)
    x = bs4.BeautifulSoup(r.text , 'html.parser')
    authorities = []
    head = x.find("h3" , string = 'Authorities')
    for a in head.parent.find_all("a"):
        if not a.text == '':
            text = a.text[:a.text.index("[")]
            pathways.append(text)
        if "[" not in a.text:
            pathways.append(a.text)
    print(authorities)
    if len(authorities) == 0:
        return None
    return authorities