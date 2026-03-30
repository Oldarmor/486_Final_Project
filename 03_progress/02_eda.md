# Exploratory Data Analysis
## Research Question and Data Set Overview
**Main research question:** what variables can be used to predict PER and Win Shares that aren't already used in the calculations of PER and Win Shares?
**Summary and Citing of Data:** All the data for this analysis will be pulled from basketball-reference.com. It is a mixture of a players average per game stats across the 2024-2025 season (which can be found [here](https://www.basketball-reference.com/leagues/NBA_2025_per_game.html#per_game_stats)), with the players advanced stats across the 2024-2025 season (which can be found [here](https://www.basketball-reference.com/leagues/NBA_2025_advanced.html)). At the bottom of this document is a variable dictionary that describes each variable in the dataset.
**Ethics and Legality:** There are no legal or ethical concerns as all the information in the data set is publicly available.
It is important to note that if a player is traded to a different team during the season shows up as two different players in the data set and their stats for each team they were on are recorded on different rows. So, Luka Doncic, for example, shows up twice: once with his stats for the LA Lakers and another time for his stats for the Dallas Mavericks.
## Data Description and Variables
**Key Variables and Target Variables:** The key variables in this analysis are going to be Player Efficiency Rating and Win Shares. Player Efficiency Rating is a metric that estimates how efficient a player is, and Win Shares is a metric that estimates how many wins that that player contributed to for their team. For more information on all the variables in the data set refer to the variable dictionary below.
**Preprocessing Steps:** Due to the size of the data set and minimal NA values, just all rows with an NA were dropped. Additionally many non-numeric columns (like awards and team for example) were also dropped because the purpose of the analysis is to find correlation between the key variables and the other variables. Finally, duplicate columns and useless columns were dropped as well.
## Summary Statistics
**Sample Size and Key Variable Statistics:** After dropping all the NA's sample size for all variables is 584. PER Mean: 13.424144, PER Standard Deviation: 5.088127. Win Shares Mean: 2.07226, Win Shares Standard Deviation: 2.43535. For mean and standard deviations for all numeric variables see the Variable Summaries below.
**Correlation Matrices:** Below are the both the Pearson (for linear relationships) and Spearman (for monotonic but non-linear relationships) correlation matrices between PER and other variables and Win Shares and other variables. Notice that many variables were removed when calculating the correlation matrices, this is because I wanted to remove any statistic that was directly used in the PER formula, or indirectly used in the PER formula.
PER Pearson Correlation Matrix:
|      |        PER |
|:-----|-----------:|
| PER  |  1         |
| 2PA  |  0.620589  |
| FTA  |  0.609264  |
| USG% |  0.431818  |
| GS   |  0.39014   |
| PF   |  0.339457  |
| G    |  0.269884  |
| BLK% |  0.266284  |
| 3PA  |  0.230728  |
| FT%  |  0.188875  |
| FTr  |  0.164542  |
| Age  |  0.158382  |
| STL% |  0.0369754 |
| TOV% | -0.173601  |
| 3PAr | -0.355315  |

PER Spearman Correlation Matrix:

|      |        PER |
|:-----|-----------:|
| PER  |  1         |
| 2PA  |  0.59234   |
| FTA  |  0.590339  |
| USG% |  0.459251  |
| FTr  |  0.403317  |
| GS   |  0.402002  |
| PF   |  0.319298  |
| BLK% |  0.263725  |
| G    |  0.255398  |
| Age  |  0.192941  |
| 3PA  |  0.16578   |
| FT%  |  0.154116  |
| STL% |  0.0368126 |
| TOV% | -0.10586   |
| 3PAr | -0.378342  |

Win Shares Pearson Correlation Matrix:

|      |          WS |
|:-----|------------:|
| WS   |  1          |
| FG   |  0.677359   |
| G    |  0.675633   |
| PTS  |  0.664464   |
| 2P   |  0.653952   |
| MP_x |  0.628787   |
| DRB  |  0.618051   |
| 2PA  |  0.602168   |
| TRB  |  0.598601   |
| FGA  |  0.595539   |
| FT   |  0.571623   |
| FTA  |  0.566889   |
| AST  |  0.530519   |
| STL  |  0.481733   |
| TOV  |  0.456335   |
| PF   |  0.432701   |
| 3P   |  0.425446   |
| TS%  |  0.421136   |
| ORB  |  0.417892   |
| FG%  |  0.387781   |
| 3PA  |  0.384216   |
| eFG% |  0.378118   |
| BLK  |  0.376511   |
| AST% |  0.281715   |
| USG% |  0.253008   |
| 2P%  |  0.249979   |
| DRB% |  0.193571   |
| Age  |  0.186925   |
| 3P%  |  0.179606   |
| FT%  |  0.17188    |
| TRB% |  0.155246   |
| BLK% |  0.095553   |
| FTr  |  0.0646177  |
| ORB% |  0.037817   |
| STL% | -0.00617285 |
| TOV% | -0.127358   |
| 3PAr | -0.165697   |

Win Shares Spearman Correlation Matrix:

|      |         WS |
|:-----|-----------:|
| WS   |  1         |
| G    |  0.773892  |
| FG   |  0.677726  |
| PTS  |  0.667608  |
| MP_x |  0.658633  |
| DRB  |  0.634193  |
| 2P   |  0.623     |
| TRB  |  0.618862  |
| TS%  |  0.611122  |
| FGA  |  0.591602  |
| eFG% |  0.579789  |
| 2PA  |  0.567215  |
| FT   |  0.53696   |
| STL  |  0.53664   |
| FG%  |  0.533329  |
| FTA  |  0.5285    |
| PF   |  0.51049   |
| AST  |  0.504031  |
| BLK  |  0.467892  |
| ORB  |  0.461266  |
| 3P   |  0.454114  |
| TOV  |  0.449342  |
| 2P%  |  0.39912   |
| 3PA  |  0.394969  |
| 3P%  |  0.356082  |
| Age  |  0.224044  |
| AST% |  0.192106  |
| FT%  |  0.179921  |
| DRB% |  0.167298  |
| BLK% |  0.155177  |
| FTr  |  0.133751  |
| USG% |  0.129639  |
| TRB% |  0.125545  |
| ORB% |  0.0451087 |
| STL% |  0.0382996 |
| 3PAr | -0.116322  |
| TOV% | -0.1602    |

**Interesting Insights:** It is extremely interesting to note that three point attempt rate has a negative correlation for both PER and Win Shares. Meaning players that shoot a higher percentage of three pointers actually tend to be less efficient and less impactful for a team. This is interesting because recently the NBA has gone through a "three point revolution" where now threes are being shot at a higher rate than ever before, but it actually seems to make a player less impactful and less efficient.

## Visual Exploration
Below is a plot showing the relationship between three point attempt rate (3PAr) and PER:
![3PAr vs PER](plots/3PAr_vs_PER.png)
This really shows a general downward trend for players that take a high percentage of three pointers. Keep in mind that mean PER is 13.424144, and looking at this chart it looks like majority of players that take over 50% of their shots beyond the three point line are below average on PER. It's also interesting to see how majority of players are right around that 50% mark on their three point attempt rate.

Below is a plot showing the relationship between field goals (FG) and Win Shares (WS):
![FG vs WS](plots/FG_vs_WS.png)

This plot is interesting because as field goals increase the variance also increases (leading to the cone shape). And while there is a general upward trend with increased field goals leading to increased win shares, there are still some players with high field goals per game, but essentially zero win shares. This supports the idea of "empty stats" or "empty points" where some players can put up a lot of points, but don't really contribute to helping their team win, which could be due to them playing poorly on the defensive end or having other issues hurting their team.

## Variable Dictionary:
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

## Variable Summaries
Below is a list of all the numeric variables in the data set, with their mean and standard deviation (in that order).

Age: 25.981164, 4.175973

G: 43.445205, 23.819585

GS: 20.431507, 25.041484

MP_x: 20.209932, 9.251792

FG: 3.399315, 2.326851

FGA: 7.432021, 4.823913

FG%: 0.448902, 0.088491

3P: 1.114726, 0.893845

3PA: 3.171233, 2.314381

3P%: 0.314269, 0.115827

2P: 2.285616, 1.831008

2PA: 4.261986, 3.294628

2P%: 0.529262, 0.104173

eFG%: 0.522075, 0.092367

FT: 1.414555, 1.359564

FTA: 1.818836, 1.660268

FT%: 0.755416, 0.139870

ORB: 0.927226, 0.728066

DRB: 2.718664, 1.760646

TRB: 3.642808, 2.327422

AST: 2.206849, 1.839771

STL: 0.701370, 0.419014

BLK: 0.401370, 0.389922

TOV: 1.138699, 0.833955

PF: 1.589384, 0.736496

PTS: 9.321062, 6.497875

Team_Win: 0.485596, 0.164010

TS%: 0.553505, 0.083791

3PAr: 0.435729, 0.192274

FTr: 0.244616, 0.155955

ORB%: 5.347432, 3.848338

DRB%: 14.676884, 6.089087

TRB%: 10.006678, 4.434483

AST%: 14.619521, 8.461719

STL%: 1.699144, 0.836793

BLK%: 1.887500, 1.635088

TOV%: 12.227568, 4.752265

USG%: 18.915753, 5.626163

OWS: 1.083048, 1.661512

DWS: 0.990068, 0.974250

WS/48: 0.080209, 0.080946

OBPM: -1.205479, 3.146574

DBPM: -0.170890, 1.559569

BPM: -1.376541, 3.888296

VORP: 0.496575, 1.154344
