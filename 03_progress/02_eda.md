# Exploratory Data Analysis
## Research Question, Data Set Overview, and Source Legitimacy
### Research Question
For later sections of the project, specifically for the supervised learning where we will try to find under and overperformers, we will be predicting both PER (Player Efficiency Rating) and player win shares. But PER and player win shares are also calculated with many of the variables in the data set, and so including those variables in the supervised learning aspect would be trivial because it would allow the machine learning model to almost replicate the exact formula. So, the research question is simple: what other variables (that aren't used in their respective calculations) relate to, and can help predict PER and player win shares?
### Data Set Overview
All the data for this analysis will be pulled from basketball-reference.com. It is a mixture of a players average per game stats across the 2024-2025 season (which can be found [here](https://www.basketball-reference.com/leagues/NBA_2025_per_game.html#per_game_stats)), with the players advanced stats across the 2024-2025 season (which can be found [here](https://www.basketball-reference.com/leagues/NBA_2025_advanced.html)). We pulled the data using a very basic web scraper, and merged it together. The pulled and merged data can be found in 00_data/player_data.csv. The notebook with the basic webscraper can be found in 00_data/data_collection.ipynb, Below is a data dictionary that describes the values in each of the columns in the data found in player_data.csv:
index: index of the rows
Rk_x: the ranking from one of the data pulls based off of a specific stat (unused in the EDA)
Player: the players name
Age: the players age in years
Team: the team that player played for
Pos: player's position
G: How many games that player played for that team in the 2024-2025 season
GS: How many games that player started for that team in the 2024-2025 season
MP_x : Average minutes per game that player played (both the box score stats and the advanced stats had minutes per game so it's duplicated in MP_x and MP_y)
FG: Average number of field goals that player made per game in the 2024-2025 season
FGA: Average number of field goals that player attempted per game in the 2024-2025 season
FG%: percentage of field goals made for that player in the 2024-2025 season
3P: average number of three pointers that player made per game in the 2024-2025 season
3PA: average number of three pointers attempted by that player per game in the 2024-2025 season
3P%: percentage of three pointers made by that player in the 2024-2025 season
2P: average number of two pointers made per game by that player in the 2024-2025 season
2PA: average number of two pointers attempted by that player per game in the 2024-2025 season
2P%: percentage of two pointers made by that player in the 2024-2025 season
eFG%: That players effective field goal percentage for the 2024-2025 season
FT: average number of free throws made by that player per game for the 2024-2025 season
FTA: average number of free throws attempted by that player per game for the 2024-2025 season
FT%: percentage of made free throws for that player in the 2024-2025 season
ORB: average number of offensive rebounds per game for that player in the 2024-2025 season
DRB: average number of deffensive rebounds per game for that player in the 2024-2025 season
TRB: average number of total rebounds per game for that player in the 2024-2025 season
AST: average number of assists for that player per game for the 2024-2025 season
STL: average number of steals per game for that player in the 2024-2025 season
BLK: average number of blocks per game for that player in the 2024-2025 season
TOV: average number of turnovers per game for that player in the 2024-2025 season
PF: average number of personal fouls per game for that player in the 2024-2025 season
PTS: average number of points per game for that player in the 2024-2025 season
Awards: what awards that player won in the 2024-2025 season
Team_Win: proportion of won games for that players team in the 2024-2025 season
Rk_y: left over ranking index that wasn't dropped when merging the two dataframes
MP_y: minutes per game for that player in the 2024-2025 season
PER: that players Player Efficiency Rating for the 2024-2025 season
TS%: true shooting percentage, a percentage of made shots taking into account two pointers, three pointers and free throws
3PAr: three point attempt rate, percentage of shot attempts that were three pointers
FTr: free throw attempt rate, number of FT attempts per FG attempt
ORB%: offensive rebound percentage, percentage of possible offensive rebounds obtained by the player
DRB%: deffensive rebound percentage, percentage of possible deffensive rebounds obtained by the player
TRB%: total rebound percentage, percentage of total possible rebounds obtained by the player
AST%: assist percentage, estimate of the percentage of teammate field goals player assisted while on the floor
STL%: steal percentage, estimate of the percentage of opponent posession ended with a steal by the player while they were on the floor
BLK%: block percentage, estimate of the percentage of opponent 2 point attempts blocked by the player while they were on the floor
TOV%: turnover percentage, estimate of number of turnovers by player made in 100 possessions
USG%: usage percentage, estimate of percentage of team plays used by a player while on the floor
OWS: offensive win shares, estimate of number of wins a player contributed based purely on offense
DWS: deffensive win shares, estimate of number of wins a player contributed base purely on defense
WS: win shares, estimate of number of wins contributed by a player
WS/48: win shares per 48 minutes, estimate of number of wins contributed by a player in 48 minutes (league average is ~ 0.1)
OBPM: offensive box plus minus, box score estimate of offensive points per 100 possesions a player contributed above a league average player on an average team
DBPM: deffensive box plus minus, box score estimate of deffensive points per 100 possesions a player contributed above a league average player on an average team
BPM: box plus minus, box score estimate of total points per 100 possesions a player contributed above a league average player on an average team
VORP: value over replacement player, box score estimate of total points per 100 team possesions that a player contributed above a replace player on an average team

It is important to note that if a player is traded to a different team during the season shows up as two different players in the data set and their stats for each team they were on are recorded on different rows. So, Luka Doncic for example shows up twice, once with his stats for the LA Lakers and another time for his stats for the Dallas Mavericks.
### Source Legitimacy
Basketball reference is the leading source of basketball statistics on players in the industry, so it's pretty reliabe. The robots.txt doesn't restrict the pages we scraped the tables off of, so there's no issue with pulling the data we pulled. Additionally all the data and numbers are readily and publicly available for everyone. Finally there isn't any legally significant information in the data so this analysis is perfectly legal.
## Variables, Target and Preprocessing
### Key and Target Variables
They key and target variables everything will be compared to will be a players PER and total win shares. We will also look at the distribution of win shares and PER. We will be looking at both the Pearson correlation and the Spearman correlation, that way we can get a good general idea of how each variabe correlates to PER and Win Shares. The Pearson correlation will give a good idea on if theres a linear relationship, and the Spearman measure monotonicity helping give me an idea if there is a strictly increasing or decreasing relationship even if it isn't strictly linear.
### Preprocessing
For preprocessing the data we simply cleaned out the excess and unimportant columns that were left over from pulling the data. Those columns include MP_y, Rk_x, Rk_y, Unnamed: 0, and index. Afterwards all rows with an NaN were dropped from the dataset, there were very few NaN's and while it did shrink the data set slightly, the size of the data set is still quite significant and so it was decided it would just be easiest to drop them. From there all of the non-numeric columns were stripped out and a quick eda (which is described in further detail below) was ran on the data to find the distributions of PER and WS and the correlations between all of the variables to get a good idea about which ones would be good to use in the supervised learning models. Finally to end we just created a the same purely numeric dataframe, but decided to keep player name, that way when a player is found to be a significant under or over performer we can know their exact name.
