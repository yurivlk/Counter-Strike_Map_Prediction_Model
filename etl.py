
#import needed libraries
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import time
import requests
from tqdm import tqdm
import re
from datetime import datetime

### Create DB conn
env_path = os.path.join('/Users/yurivelkis/Downloads/BootCamp/Counter-Strike_Match_Prediction_Model/','secrets.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

db_server = os.getenv('db_server')
user = os.getenv('user')
db_port = os.getenv('db_port')
password = os.getenv('password')
ip = os.getenv('ip')
db_name = os.getenv('db_name')

engine = create_engine(f'mysql+{db_server}://{user}:{password}@{ip}:{db_port}/{db_name}?charset=utf8')

#Code to test cron
#df = pd.DataFrame({'time':f'{datetime.now().strftime("%H %M %S")}'})
#df.to_sql('teste', con=engine.connect(), if_exists='append')

## Function to try connection with DB
def connection(x):
    try:
        conn = x.connect()
        return conn
    except:
        print('Conncection Fail')

## Function to create a list off all matches id already in the DB
def get_matches_in_database(engine):
    conn = connection(engine)
    sql = " SELECT match_id FROM matches_info "
    matches_scrapped2 = pd.read_sql(sql, con=conn)
    links = list(matches_scrapped2['match_id'])
    return links

## Function to iterate through the first 3 pages on hltv.org and get the matches not scraped
def match_links(engine):
    print('####Colecting matches wich is not in our DB already...')
    db_matches = get_matches_in_database(engine)
    match_links = []
    for x in range(900,1000,100):
        url = f'https://www.hltv.org/results?offset={x}&stars=2'
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        for i in range(len(soup.find_all('div', {'class':'result-con'}))):
            if re.findall('[0-9]{7}',soup.find_all('div', {'class':'result-con'})[i]('a')[0]['href'])[0] in db_matches:
                pass
            else:
                match_links.append(soup.find_all('div', {'class':'result-con'})[i]('a')[0]['href'])
        print('Done')
    return match_links

## Function to iterate through match_links and get map_details links
def matches_details_links(links_to_scrap):
    print('###Colecting link of matches details to extract info...')
    map_links = []
    for item in tqdm(links_to_scrap[:4]):
        url = f'https://www.hltv.org{item}'
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        if re.findall('\west of [0-9]',soup.find_all('div',{'class':'padding preformatted-text'})[0].text)[0] == 'Best of 5':
            pass
        else:
            try:
                #map1_link
                map_links.append(soup.find_all('div',{'class':'results-center-stats'})[0]('a')[0]['href'])
            except:
                print('ok')
            try:
                map_links.append(soup.find_all('div',{'class':'results-center-stats'})[1]('a')[0]['href'])
            except:
                print('no map2')
            try:
                map_links.append(soup.find_all('div',{'class':'results-center-stats'})[2]('a')[0]['href'])
            except:
                print('no map 2')
            pass
        print('Done, we are almost there...')    
    return map_links

## Function to extract info and create 
def extract_maps_info(map_links):
    print('Extracting match infos... This will take a bit longer, grab a coffee mate...')
    df_map_infos = []
    links_quebrados = []
    map_details = {
        'date' : [],
        'match_id' : [],
        'team_1' : [],
        'team_2' : [],
        'best_of' : [],
        'map': [],
        'score_t1' : [],
        'ct_side_t1': [],
        't_side_t1' : [],
        'score_t2' : [],
        'ct_side_t2' : [],
        't_side_t2' : [],
        'team_start_ct' : [],
        'team_1_rating':[],
        'team_2_rating':[],
        'team_1_first_kill' : [],
        'team_2_first_kill' : [],
        'team_1_clutches' : [],
        'team_2_clutches':[],
        'eco_t1' : [],
        'eco_t2' : [],
        'semi_eco_t1' : [],
        'semi_eco_t2' : [],
        'semi_buy_t1' : [],
        'semi_buy_t2' : [],
        'full_buy_t1' : [],
        'full_buy_t2' : [],    
    }

    for item in tqdm(map_links):
        url =f'https://www.hltv.org{item}'
        response = requests.get(url)
        if response.status_code == 200: 
            html = response.content
            soup = BeautifulSoup(html, "html.parser")
            try:
                #date
                date = (soup.find_all('div', {'class':'match-info-box'})[0]('span')[0].text)
                #match_id
                match_id = (re.findall('\d+',soup.find_all('a', {'class':'match-page-link button'})[0]['href'])[0])
                #team_1
                team_1 = (soup.find_all('div', {'class':'team-left'})[0]('img')[0]['title'])
                #team_2
                team_2 = (soup.find_all('div', {'class':'team-right'})[0]('img')[0]['title'])
                #map
                map_ = (soup.find('div', {'class':'small-text'}).next_sibling.strip())
                #score_t1
                score_t1 = (soup.find_all('div',{'class':'match-info-row'})[0]('span')[0].text)
                #score_t2
                score_t2 = (soup.find_all('div',{'class':'match-info-row'})[0]('span')[1].text)
                for i in range(2,6,2):
                    if soup.find_all('div',{'class':'match-info-row'})[0]('span')[i]['class'][0] ==  'ct-color':
                        ct_side_t1 = (soup.find_all('div',{'class':'match-info-row'})[0]('span')[i].text)
                    else:
                        t_side_t1 = (soup.find_all('div',{'class':'match-info-row'})[0]('span')[i].text)
                for i in range(3,6,2):
                    if soup.find_all('div',{'class':'match-info-row'})[0]('span')[i]['class'][0] ==  'ct-color':
                        ct_side_t2 = (soup.find_all('div',{'class':'match-info-row'})[0]('span')[i].text)
                    else:
                        t_side_t2 = (soup.find_all('div',{'class':'match-info-row'})[0]('span')[i].text)
                #team_start_ct
                if soup.find_all('div',{'class':'match-info-row'})[0]('span')[2]['class'][0] == 'ct-color':
                    team_starts_ct = (1)
                else:
                    team_starts_ct = (2)
                #best of
                try:
                    best_of = (soup.find_all('div', {'class':'stats-match-map-result-mapname dynamic-map-name-short'})[0].text)
                except:
                    best_of = ('bo1')
                #Team1_rating
                team1_rating = soup.find_all('div',{'class':'match-info-row'})[1]('div', {'class':'right'})[0].text.split()[0]
                #Team2_rating 
                team2_rating = soup.find_all('div',{'class':'match-info-row'})[1]('div', {'class':'right'})[0].text.split()[2]
                #Team 1 first kill
                team1_first_kill = soup.find_all('div',{'class':'match-info-row'})[2]('div', {'class':'right'})[0].text.split()[0]
                #Team 2 first kill
                team2_first_kill = soup.find_all('div',{'class':'match-info-row'})[2]('div', {'class':'right'})[0].text.split()[2]
                #t1_clutches
                team1_clutches = soup.find_all('div',{'class':'match-info-row'})[3]('div', {'class':'right'})[0].text.split()[0]
                #t2 Clutches
                team2_clutches = soup.find_all('div',{'class':'match-info-row'})[3]('div', {'class':'right'})[0].text.split()[2]
                tempurl2 = soup.find_all('div',{'class':'tabs'})[0]('a',{'class':'stats-top-menu-item stats-top-menu-item-link'})[1]['href']
                time.sleep(3)
                url2 =f'https://www.hltv.org{tempurl2}'
                response = requests.get(url2)
                html = response.content
                soup = BeautifulSoup(html)
                eco_t1 = soup.find_all('div',{'class':'col standard-box stats-rows'})[0]('span',{'title':'Played'})[0].text.split()[0]
                eco_t2 = soup.find_all('div',{'class':'col standard-box stats-rows'})[1]('span',{'title':'Played'})[0].text.split()[0]
                semi_eco_t1 = soup.find_all('div',{'class':'col standard-box stats-rows'})[0]('span',{'title':'Played'})[1].text.split()[0]
                semi_eco_t2 = soup.find_all('div',{'class':'col standard-box stats-rows'})[1]('span',{'title':'Played'})[1].text.split()[0]
                semi_buy_t1 = soup.find_all('div',{'class':'col standard-box stats-rows'})[0]('span',{'title':'Played'})[2].text.split()[0]
                semi_buy_t2 = soup.find_all('div',{'class':'col standard-box stats-rows'})[1]('span',{'title':'Played'})[2].text.split()[0]
                full_buy_t1 = soup.find_all('div',{'class':'col standard-box stats-rows'})[0]('span',{'title':'Played'})[3].text.split()[0]
                full_buy_t2 = soup.find_all('div',{'class':'col standard-box stats-rows'})[1]('span',{'title':'Played'})[3].text.split()[0]
                map_details['date'].append(date)            
                map_details['match_id'].append(match_id)
                map_details['team_1'].append(team_1)
                map_details['score_t1'].append(score_t1)
                map_details['ct_side_t1'].append(ct_side_t1)
                map_details['t_side_t1'].append(t_side_t1)
                map_details['team_2'].append(team_2)
                map_details['score_t2'].append(score_t2)
                map_details['ct_side_t2'].append(ct_side_t2)
                map_details['t_side_t2'].append(t_side_t2)
                map_details['map'].append(map_)
                map_details['best_of'].append(best_of)
                map_details['team_start_ct'].append(team_starts_ct)
                map_details['team_1_rating'].append(team1_rating)
                map_details['team_2_rating'].append(team2_rating)
                map_details['team_1_first_kill'].append(team1_first_kill)
                map_details['team_2_first_kill'].append(team2_first_kill)
                map_details['team_1_clutches'].append(team1_clutches)
                map_details['team_2_clutches'].append(team2_clutches)
                map_details['eco_t1'].append(eco_t1)
                map_details['eco_t2'].append(eco_t2)
                map_details['semi_eco_t1'].append(semi_eco_t1)
                map_details['semi_eco_t2'].append(semi_eco_t2)
                map_details['semi_buy_t1'].append(semi_buy_t1)
                map_details['semi_buy_t2'].append(semi_buy_t2)
                map_details['full_buy_t1'].append(full_buy_t1)
                map_details['full_buy_t2'].append(full_buy_t2)
            except:
                links_quebrados.append(url)
                print('quebrou')
                time.sleep(5)
                pass
        else:
            pass
    print('Enjoy...')
    df_map_infos.append(pd.DataFrame(map_details))
    return df_map_infos

##Simple data transformation

links_to_scrap = match_links(engine)

map_links = matches_details_links(links_to_scrap)

df = extract_maps_info(map_links)
df = pd.concat(df)

df['winner'] = df.apply(lambda x :1 if x['score_t1']>x['score_t2'] else 2, axis=1)

print(df)


#df.to_sql(con=connection(engine), name='matches_info', if_exists='append',index=False)    

