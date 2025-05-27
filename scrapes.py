import time
import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium

# Older method using pd.read_html -- prone to 429 responses
def MLS_gk_scrape_per_table():

    delay = 20   # Avoid 429
    baseurl = "https://fbref.com/en/squads/"
    teamIDs = [
        "cb8b86a2/Inter-Miami-Stats",
        "529ba333/Columbus-Crew-Stats",
        "e9ea41b2/FC-Cincinnati-Stats",
        "46ef01d0/Orlando-City-Stats",
        "eb57545a/Charlotte-FC-Stats",
        "64e81410/New-York-City-FC-Stats",
        "69a0fb10/New-York-Red-Bulls-Stats",
        "fc22273c/CF-Montreal-Stats",
        "1ebc1a5b/Atlanta-United-Stats",
        "44117292/DC-United-Stats",
        "130f43fa/Toronto-FC-Stats",
        "46024eeb/Philadelphia-Union-Stats",
        "35f1b818/Nashville-SC-Stats",
        "3c079def/New-England-Revolution-Stats",
        "f9940243/Chicago-Fire-Stats",
        "81d817a3/Los-Angeles-FC-Stats",
        "d8b46897/LA-Galaxy-Stats",
        "f7d86a43/Real-Salt-Lake-Stats",
        "6218ebd4/Seattle-Sounders-FC-Stats",
        "0d885416/Houston-Dynamo-Stats",
        "99ea75a6/Minnesota-United-Stats",
        "415b4465/Colorado-Rapids-Stats",
        "ab41cb90/Vancouver-Whitecaps-FC-Stats",
        "d076914e/Portland-Timbers-Stats",
        "b918956d/Austin-FC-Stats",
        "15cf8f40/FC-Dallas-Stats",
        "bd97ac1f/St-Louis-City-Stats",
        "4acb0537/Sporting-Kansas-City-Stats",
        "ca460650/San-Jose-Earthquakes-Stats"
    ]
    
    gklist = []

    print("Retreiving MLS GK stats from 2024...")

    for i in range(len(teamIDs)):
        time.sleep(delay)

        # Retrieve GA and SoTA
        sotadf = pd.read_html(baseurl + teamIDs[i], attrs={"id":"stats_keeper_22"})[0]
        sotadf = sotadf.droplevel(0, axis=1)
        sotadf = sotadf.drop(sotadf[(sotadf.Player == 'Squad Total')].index)
        sotadf = sotadf.drop(sotadf[(sotadf.Player == 'Opponent Total')].index)
        sotadf = sotadf.loc[:, ['Player', 'GA', 'SoTA']]

        time.sleep(delay)

        # Retrieve PSxG
        psxgdf = pd.read_html(baseurl + teamIDs[i], attrs={"id":"stats_keeper_adv_22"})[0]
        psxgdf = psxgdf.droplevel(0, axis=1)
        psxgdf = psxgdf.drop(psxgdf[(psxgdf.Player == 'Squad Total')].index)
        psxgdf = psxgdf.drop(psxgdf[(psxgdf.Player == 'Opponent Total')].index)
        psxgdf = psxgdf.loc[:, ['PSxG']]

        # Concatenate
        team_gk_df = pd.concat([sotadf, psxgdf], axis = 1)

        for row in team_gk_df.values.tolist():
            gklist.append(row)
    
    full_gk_df = pd.DataFrame(gklist)
    full_gk_df.columns = ['Player', 'GA', 'SoTA', 'PSxG']

    return full_gk_df

def mls_gk_scrape(filename):

    delay = 10   # Avoid 429
    baseurl = "https://fbref.com/en/squads/"
    teamids = [
        "cb8b86a2/Inter-Miami-Stats",
        "529ba333/Columbus-Crew-Stats",
        "e9ea41b2/FC-Cincinnati-Stats",
        "46ef01d0/Orlando-City-Stats",
        "eb57545a/Charlotte-FC-Stats",
        "64e81410/New-York-City-FC-Stats",
        "69a0fb10/New-York-Red-Bulls-Stats",
        "fc22273c/CF-Montreal-Stats",
        "1ebc1a5b/Atlanta-United-Stats",
        "44117292/DC-United-Stats",
        "130f43fa/Toronto-FC-Stats",
        "46024eeb/Philadelphia-Union-Stats",
        "35f1b818/Nashville-SC-Stats",
        "3c079def/New-England-Revolution-Stats",
        "f9940243/Chicago-Fire-Stats",
        "81d817a3/Los-Angeles-FC-Stats",
        "d8b46897/LA-Galaxy-Stats",
        "f7d86a43/Real-Salt-Lake-Stats",
        "6218ebd4/Seattle-Sounders-FC-Stats",
        "0d885416/Houston-Dynamo-Stats",
        "99ea75a6/Minnesota-United-Stats",
        "415b4465/Colorado-Rapids-Stats",
        "ab41cb90/Vancouver-Whitecaps-FC-Stats",
        "d076914e/Portland-Timbers-Stats",
        "b918956d/Austin-FC-Stats",
        "15cf8f40/FC-Dallas-Stats",
        "bd97ac1f/St-Louis-City-Stats",
        "4acb0537/Sporting-Kansas-City-Stats",
        "ca460650/San-Jose-Earthquakes-Stats"
    ]

    all_data_ls = []

    # len(teamids)

    for i in range(len(teamids)):

        print(f"Retrieving '{teamids[i]}'...")

        # Retrieve page and tables
        page = requests.get(baseurl + teamids[i]).text
        soup = BeautifulSoup(page, 'html.parser')
        gktable = soup.find('table', id='stats_keeper_22')
        agktable = soup.find('table', id='stats_keeper_adv_22')

        # Exclude unnecessary top and bottom rows
        gkrows = gktable.find_all('tr')[2:-2]
        agkrows = agkrows = agktable.find_all('tr')[2:-2]

        # Retrieve stats from goalkeeping table
        for i in range(len(gkrows)):
            row_ls = []
            
            # Player name
            row_ls.append(gkrows[i].find('th').text)

            # Rest of player data
            for td in gkrows[i].find_all('td')[:-1]:
                row_ls.append(td.text.replace(",", ""))

            # Retrieve PSxG from advanced goalkeeping table
            row_ls.append(agkrows[i].find_all('td')[9].text)
            
            all_data_ls.append(row_ls)

        time.sleep(delay)

    # Make df
    df = pd.DataFrame(all_data_ls)
    df.columns = [
        'Player', 'Nation', 'Pos', 'Age', 'MP', 'Starts', 'Min', '90s', 'GA', 'GA90', 'SoTA', 'Saves', 
        'Save%', 'W', 'D', 'L', 'CS', 'CS%', 'PKatt', 'PKA', 'PKsv', 'PKm', 'Save%', 'PSxG'
    ]

    # Drop unnecessary rows
    # Edit this to keep whichever stats you want
    df = df.loc[:, ['Player', 'Min', '90s', 'GA', 'SoTA', 'PSxG']]

    df['Min'] = df['Min'].astype(int)
    df['90s'] = df['90s'].astype(float)
    df['GA'] = df['GA'].astype(int)
    df['SoTA'] = df['SoTA'].astype(int)
    df['PSxG'] = df['PSxG'].astype(float)

    # Add some custom metrics
    df['GSAA'] = (round(df['PSxG'] - df['GA'], 3))
    df['GSAA%'] = (round((df['GSAA'] / df['SoTA']) * 100, 3))

    # Write
    df.to_csv(filename, index=False)

    return

def validate_chromedriver():
    # Validates that the directory containing the Chrome Driver exists and if so, returns the path
    if not os.path.exists('./DRIVERPATH.txt'):
        print('Error: DRIVERPATH.txt could not be found.')
        return None
    
    with open('./DRIVERPATH.txt', 'r') as file:
        driverpath = file.readline()

        if not driverpath:
            print('Error: DRIVERPATH.txt is empty.')
            return None
        else:
            return driverpath

def fotmob_prem_gk_urls():
    # This method writes the GK URLs to a text file to minimize the number of scrapes that
    # need to be done -- they take a while because of the added delays

    # Choose the league URL
    league_url = 'https://www.fotmob.com/leagues/47/overview/premier-league'
    base_team_url = 'https://www.fotmob.com/teams/'
    
    # Set up chromium driver
    driverpath = validate_chromedriver()
    if not driverpath:
        print("ERROR")
        return

    service = Service(executable_path=f'{driverpath + '/chromedriver.exe'}')
    driver = webdriver.Chrome(service=service)
    driver.get(league_url)
    driver.implicitly_wait(5)

    # Find each team in league, and then find the keeper
    teams = driver.find_elements(By.CLASS_NAME, "eo46u7w1")

    team_urls = []
    gk_urls = []

    # Isolate the url for each team
    for i in range(len(teams)):
        team_urls.append(teams[i].get_attribute('href')[29:])

    # On each team page retrieve GK
    for url in team_urls:
        driver.get(base_team_url + url)
        gk_div = driver.find_elements(By.CLASS_NAME, "ejpepe01")[-1]
        gk_urls.append(gk_div.find_element(By.TAG_NAME, 'a').get_attribute('href'))
        time.sleep(3)

    driver.quit()

    with open('./fotmob_prem_gk_urls.txt', 'w') as file:
        file.write(gk_urls[0])
        for i in range(1, len(gk_urls)):
            file.write(f'\n{gk_urls[i]}')
    return

def fotmob_prem_gk_stats():
    # This method uses the text file output of the fotmob_pl_gk_urls() method

    # Check that file exists
    if not os.path.exists('./fotmob_prem_gk_urls.txt'):
        print('ERROR: fotmob_prem_gk_urls.txt could not be found.')
        print('Try running the fotmob_prem_gk_urls method first.')
        return

    # Read in the URLs from the file
    gk_urls = []
    with open('./fotmob_prem_gk_urls.txt', 'r') as file:
        while(True):
            url = file.readline()
            if not url:
                break
            gk_urls.append(url.strip('\n'))

    # Will use BeautifulSoup for scraping player stats

    # First row will be complete set of stat names -- some players are missing stats
    complete_stats = ['Name', 'Saves','Save percentage','Goals conceded','Goals prevented',
                       'Clean sheets','Penalties faced','Penalty goals conceded','Penalty saves',
                       'Error led to goal','Acted as sweeper','High claim','Pass accuracy',
                       'Accurate long balls','Long ball accuracy','Assists','Yellow cards','Red cards']
    all_gk_bs_data = []
    

    for i in range(len(gk_urls)):
        # Loop for each player
        page = requests.get(gk_urls[i]).text
        soup = BeautifulSoup(page, 'html.parser')
        player_data = [0] * 18

        # Retrieve player name
        player_data[0] = (soup.find('h1', class_='e97um7g1').text)

        # Retrieve stat names and values
        stat_names = soup.find_all('div', class_ = 'e1uibvo11')
        stat_names = [data.text for data in stat_names]
        stat_values = soup.find_all('div', class_='e1uibvo12')
        stat_values = [data.text for data in stat_values]

        # For each name in stat_names, fill the corresponding column in player_data with the 
        # value in stat_values. All fields that do not get filled this way will default to a value
        # of 0, so we get a complete row of stats even if the player card on FotMob is incomplete
        for i in range(len(stat_names)):
            name = stat_names[i]
            lookup_index = complete_stats.index(name)

            # Type conversions
            if '.' in stat_values[i]:
                player_data[lookup_index] = float(stat_values[i].rstrip("%"))
            else:
                player_data[lookup_index] = int(stat_values[i])

        all_gk_bs_data.append(player_data)

    # Convert to dataframe and write to csv
    df = pd.DataFrame(all_gk_bs_data)
    df.columns = complete_stats

    df.to_csv('fotmob_prem_gk_stats.csv', index=False, encoding='utf-8-sig')

def transfermarkt_mls_transfers():

    baselink = "http://transfermarkt.com/major-league-soccer/transfers/wettbewerb/MLS1"
    
    # Set up chromium driver
    driverpath = validate_chromedriver()
    if not driverpath:
        print("ERROR")
        return

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3') # Suppress SSL errors from terminal
    chrome_options.add_argument('--block-new-web-content')

    service = Service(executable_path=f'{driverpath + '/chromedriver.exe'}')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(baselink)
    driver.maximize_window()
    
    # Switch iframes to close the ad popup that appears
    try:
        iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='sp_message_iframe_953358']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept & continue']"))).click()
    except:
        print("Error: Failed to locate the popup button.")

    # Step out of iframe
    driver.switch_to.default_content()
    
    # All clubs are contained in divs with class "box". Need to select only those divs that are clubs, exclude the rest
    large8  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "large-8")))
    all_div_box = large8.find_elements(By.CLASS_NAME, "box")
    
    # Exclude non-club elements
    all_club_elements = all_div_box[4:34]
    
    # More sophisticated method -- look at implementing later
    # for div in all_div_box:
    #     try:
    #         # The clubs contain a h2 tag
    #         div.find_element(By.TAG_NAME, "h2")
    #         clubs.append(div)
    #     except:
    #         continue

    # Define useful variables for scraping procedure
    original_window = driver.current_window_handle
    mapClubToLeague = dict()                        # Cache that will map a club to a league
    concat_dataframes = False                       # Global DF containing all stats will be created for first club, afterwards all other clubs will be concatenated

    # Table headers are shared for all clubs -- only need to retrieve once
    test_club = all_club_elements[0]
    data_table = test_club.find_element(By.CLASS_NAME, "responsive-table").find_element(By.TAG_NAME, 'table')
    table_headers_raw = data_table.find_element(By.TAG_NAME, "thead").find_element(By.TAG_NAME, "tr").find_elements(By.TAG_NAME, "th")
    table_headers_text = []
    for header in table_headers_raw:
        if not header.text: # Skip empty cell
            continue 
        table_headers_text.append(header.text)

    # Add Euro currency to table header and create new column for league that player left
    table_headers_text[4] += " (EUR)"
    table_headers_text[5] = "LeftClub"
    table_headers_text.insert(6, "LeftLeague")
    table_headers_text[7] += " (EUR)"
    table_headers_text[0] = "Name"
    table_headers_text.insert(0, "JoinedClub")
    
    # Now iterate through all clubs to retrieve table data
    for club in all_club_elements:
        club_data_list = [] # Array containing entire table of data for one club
        club_name = club.find_element(By.TAG_NAME, "h2").find_elements(By.TAG_NAME, "a")[1].text
        data_table = club.find_element(By.CLASS_NAME, "responsive-table").find_element(By.TAG_NAME, 'table')
        all_rows = data_table.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, 'tr')

        for row in all_rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            player_name = cells[0].find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "a").text
            age = int(cells[1].text)
            nat = cells[2].find_element(By.TAG_NAME, "img").get_attribute("title")
            pos = cells[3].text
            mv = cells[5].text

            # The 'left' column will be split into leftClub and leftLeague
            # The league will need to be retrieved with a further web scrape and stored in a cache to improve performance
            leftCell = cells[7].find_element(By.TAG_NAME, "a")
            leftClub = leftCell.get_attribute("title")

            if leftClub == "Without Club":
                leftLeague = ""
            elif leftClub in mapClubToLeague:
                leftLeague = mapClubToLeague[leftClub] # Used cached result, if available
            else:
                clubPageURL = leftCell.get_attribute("href")
                driver.switch_to.new_window('club page')
                driver.get(clubPageURL)

                try:
                    leagueElement = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "data-header__club-info")))
                    leftLeague = leagueElement.find_element(By.TAG_NAME, "span").find_element(By.TAG_NAME, "a").text.strip()
                except:
                    leftLeague = ""

                # Place the retrieved pairing in the dictionary
                mapClubToLeague[leftClub] = leftLeague

                driver.close()
                driver.switch_to.window(original_window)

            fee = cells[8].find_element(By.TAG_NAME, "a").text

            # Covert mv cell to numeric value
            if "k" in mv:
                mv_numeric = mv[re.search(r"\d", mv).span()[0]:].rstrip("k")
                mv_numeric = float(mv_numeric) * 1000
            elif "m" in mv:
                mv_numeric = mv[re.search(r"\d", mv).span()[0]:].rstrip("m")
                mv_numeric = float(mv_numeric) * 1000000
            
            # Convert fee cell to numeric value
            if "k" in fee:
                fee_numeric = fee[re.search(r"\d", fee).span()[0]:].rstrip("k")
                fee_numeric = float(fee_numeric) * 1000
            elif "m" in fee:
                fee_numeric = fee[re.search(r"\d", fee).span()[0]:].rstrip("m")
                fee_numeric = float(fee_numeric) * 1000000

            club_data_list.append([club_name, player_name, age, nat, pos, mv_numeric, leftClub, leftLeague, fee_numeric])

        if not concat_dataframes:
            # On first pass, simply create the global dataframe since there is nothing to concatenate
            all_mls_incoming_transfers = pd.DataFrame(club_data_list, columns=table_headers_text)
            concat_dataframes = True
        else:
            # For all remaining clubs, concatenate to the global dataframe
            club_data_df = pd.DataFrame(club_data_list, columns=table_headers_text)
            all_mls_incoming_transfers = pd.concat([all_mls_incoming_transfers, club_data_df], axis=0, ignore_index=True)

    all_mls_incoming_transfers.to_csv('./MLS-Incoming-Transfers-24-25.csv', index=False)

    driver.quit()
    return

def transfermarkt_mls_transfers_bs4():
    # Alternative to original transfermarkt_mls_transfers which exclusively uses Selenium -- performs very slowly
    # Introducing bs4 to improve performance

    baselink = "http://transfermarkt.com/major-league-soccer/transfers/wettbewerb/MLS1"
    
    # Set up chromium driver
    driverpath = validate_chromedriver()
    if not driverpath:
        print("ERROR")
        return

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('log-level=3') # Suppress SSL errors from terminal
    chrome_options.add_argument('--block-new-web-content')

    service = Service(executable_path=f'{driverpath + '/chromedriver.exe'}')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(baselink)
    driver.maximize_window()

    # Define useful variables for scraping procedure
    original_window = driver.current_window_handle
    mapClubToLeague = dict()                        # Cache that will map a club to a league
    concat_dataframes = False                       # Global DF containing all stats will be created for first club, afterwards all other clubs will be concatenated
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0"} # Avoid 403 using requests
    
    # Switch iframes to close the ad popup that appears
    try:
        iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='sp_message_iframe_953358']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept & continue']"))).click()
    except:
        print("Error: Failed to locate the popup button.")

    # Step out of iframe
    driver.switch_to.default_content()
    
    # All clubs are contained in divs with class "box". Need to select only those divs that are clubs, exclude the rest
    large8  = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "large-8")))
    large8bs = BeautifulSoup(large8.get_attribute("innerHTML"), "html.parser")
    all_clubs = large8bs.find_all("div", class_="box")[3:]

    table_headers = ["JoinedClub", "Age", "Name", "Nationality", "Position", "MarketValue (EUR)", "LeftClub", "LeftLeague", "Fee"]

    for club in all_clubs:
        club_data_ls = []
        club_name = club.find("h2").find_all("a")[1].string
        table = club.find("div", class_ = "responsive-table").find("table")
        all_rows = table.find("tbody").find_all("tr")

        for row in all_rows:
            cells = row.find_all("td")

            fee = cells[8].find("a").decode_contents()
        
            if ("free" in fee) or ("loan" in fee) or ("draft" in fee) or ("-" in fee):
                continue    # Skip rows that are not real transfers

            p_name = cells[0].find("div").find("span").find("a").string
            age = int(cells[1].string)
            nat = cells[2].find("img")['title']
            pos = cells[3].string
            mv = cells[5].string
            leftCell= cells[6].find("a")
            leftClub = leftCell['title']

            # Use hyperlink in "Left" cell to find the league of the club the player left
            if leftClub == "Without Club":
                leftLeague = ""
            elif leftClub in mapClubToLeague:
                leftLeague = mapClubToLeague[leftClub] # Used cached result, if available
            else:
                # driver.switch_to.new_window()
                # driver.get(f"https://www.transfermarkt.com{leftCell["href"]}")
                r = requests.get(f"https://www.transfermarkt.com{leftCell["href"]}", headers=headers)
                leagueSoup = BeautifulSoup(r.content, "html.parser")

                try:
                    leftLeague = leagueSoup.find("div", class_ = "data-header__box--big").find("span", class_="data-header__club").a.string.strip()
                except:
                    leftLeague = ""

                # Place the retrieved pairing in the dictionary
                mapClubToLeague[leftClub] = leftLeague
            
            # Covert mv cell to numeric value
            if "k" in mv:
                mv_numeric = mv[re.search(r"\d", mv).span()[0]:].rstrip("k")
                mv_numeric = float(mv_numeric) * 1000
            elif "m" in mv:
                mv_numeric = mv[re.search(r"\d", mv).span()[0]:].rstrip("m")
                mv_numeric = float(mv_numeric) * 1000000
            
            # Convert fee cell to numeric value
            if "k" in fee:
                fee_numeric = fee[re.search(r"\d", fee).span()[0]:].rstrip("k")
                fee_numeric = float(fee_numeric) * 1000
            elif "m" in fee:
                fee_numeric = fee[re.search(r"\d", fee).span()[0]:].rstrip("m")
                fee_numeric = float(fee_numeric) * 1000000

            club_data_ls.append([club_name, p_name, age, nat, pos, mv_numeric, leftClub, leftLeague, fee_numeric])

        if not concat_dataframes:
            # On first pass, simply create the global dataframe since there is nothing to concatenate
            all_mls_incoming_transfers = pd.DataFrame(club_data_ls, columns=table_headers)
            concat_dataframes = True
        else:
            # For all remaining clubs, concatenate to the global dataframe
            club_data_df = pd.DataFrame(club_data_ls, columns=table_headers)
            all_mls_incoming_transfers = pd.concat([all_mls_incoming_transfers, club_data_df], axis=0, ignore_index=True)

    all_mls_incoming_transfers.to_csv('./MLS-Incoming-Transfers-24-25.csv', index=False)

    return

