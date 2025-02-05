import pandas as pd

def MLS_gk_scrape():

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
    
    