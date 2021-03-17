import json
import requests
from bs4 import BeautifulSoup
from sportsreference.ncaab.teams import Teams

import unfound_teams

logo_urls = {}
unfound_teams = unfound_teams.get_teams()
teams = Teams()
URL = 'https://www.ncaa.com/schools/'

worked = 0
failed = 0

for team in teams:
    name = team.name
    formatted_name = name.replace(' ', '-').replace('.', '').replace('\'', '').lower()

    try:
        page = requests.get(URL + formatted_name)
        soup = BeautifulSoup(page.content, 'html.parser')

        results = soup.find(id='block-bespin-content')
        if not results:
            if formatted_name in unfound_teams:
                page = requests.get(URL + unfound_teams[formatted_name])
            elif formatted_name.find('&-') > -1:
                page = requests.get(URL + formatted_name.replace('&-', ''))
            elif formatted_name.find('&') > -1:
                page = requests.get(URL + formatted_name.replace('&', ''))
            elif formatted_name.find('state') > -1:
                page = requests.get(URL + formatted_name.replace('state', 'st'))
            elif formatted_name.find('(') > -1:
                page = requests.get(URL + formatted_name.replace('(', '').replace(')',''))
            elif formatted_name.find('florida') > -1:
                page = requests.get(URL + formatted_name.replace('florida', 'fla'))
            elif formatted_name.find('illinois') > -1:
                page = requests.get(URL + formatted_name.replace('illinois', 'ill'))
            elif formatted_name.find('kentucky') > -1:
                page = requests.get(URL + formatted_name.replace('kentucky', 'ky'))
            elif formatted_name.find('north-carolina') > -1:
                page = requests.get(URL + formatted_name.replace('north-carolina', 'unc'))
            elif formatted_name.find('-') > -1:
                i = formatted_name.find('-')
                page = requests.get(URL + formatted_name[:i+5])
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find(id='block-bespin-content')
        
        job_elems = results.find_all('div', class_='school-logo')

        for job_elem in job_elems:
            image = job_elem.find('img')
            # print(f'{formatted_name}: {image["src"]}')
            logo_urls[name] = image['src']
            worked += 1
    
    except:
        print(f'{formatted_name}: DID NOT WORK')
        failed += 1

with open("logos.json", "w") as write_file:
    json.dump(logo_urls, write_file, sort_keys=True, indent=4)

print(f'Worked: {worked}, Failed: {failed}')
