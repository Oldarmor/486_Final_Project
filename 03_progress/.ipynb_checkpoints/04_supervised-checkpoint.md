# Supervised Learning Results

## Problem Context

The goal of this analysis is to see how a players play style influences their effeciency and win shares across a season. The purpose of the supervised models was to take the clustering results from the unsupervised component and a select few other predictor variables to try to predict players Win Shares and Efficiency and compare predicted values to true values to find under and over performers.

## Supervised Models Implemented

There were two supervised models implemented and compared to predict Win Shares and PER, linear regression and a random forest regressor. To be clear, a linear regression model was fit to predict Win Shares and PER, and a random forest regressor model was fit to predict both Win Shares and PER. In order to compare the models a 80/20 train and test split was done on the data, then RMSE was calculated on both the train set and the test set to compare. The predictor variables passed into the models were always the same: 2PA per minute, FTA per minute, USG%, PF per minute, 3PA per minute, TOV%, 3PAr, and the cluster label created from the clustering analysis. It is important to note that each cluster label was given it's own indication as opposed to comparing cluster labels to a base line group, which does introduce some slight multicolinearity into the model, but we decided that it would be negligible. Also all of the predictor variables were scaled using a Standard Scaler.

The linear regression model didn't have any hyper parameter tuning needed. To tune the random forest regressor a 5 fold grid search cross validation was used to experiment with different numbers of estimators, max depth, minimum samples per split, and minimum samples per leaf. This was run for both the PER and WS model. After running the cross validation, the hyper parameters for the PER model are: max depth of 7, 1 minimum samples per leaf, 5 minimum samples per split, and 200 estimators. The hyper parameters for the WS model are: max depth of 5, 5 minimum samples per leaf, 20 minimum samples per split, and 100 estimators.

Finally, we wanted to predict a players PER and Win Shares using the models created, but it was imperative that the predictions came from a model that hasn't already seen and been trained on the player. So, while a train and test split was used to get some model metrics and used to compare the models, in order to get the predicted values a cross validation prediction function was used.

## Model Comparison and Selection

After fitting and comparing the models, it became clear that the Random Forest Regressor was really prone to overfitting the data. In fact, the initial 5 fold cross validation grid search needed to be adjusted to include more values for maximum depth, minimum samples per split, and minimum samples per leaf and run again because the initial parameters overfit the data far too much. The Grid Search also took a long time to run, about 7-8 minutes per model, making it hard to test many different combinations of hyperparameters. After the final hyper parameters were found though, the random forest actually didn't significantly out perform the linear regression model. In fact, the linear regression model performed slightly better than the random forest for predicting PER and the linear models PER prediction is what we used to decide if a player is an under or over performer. Below are the RMSE scores for both the linear regression model and the random forest regression model:

### Model Summary Table

| Model             | Target | Key Hyperparameters                                                     | Train RMSE        | Test RMSE              |
| ----------------- | ------ | ----------------------------------------------------------------------- | ----------------- | ---------------------- |
| Linear Regression | PER    | None                                                                    | 2.720265258497129 | 3.448246487553878      |
| Random Forest     | PER    | max_depth=7, min_samples_leaf=1, min_samples_split=5, n_estimators=200  | 1.873763155736009 | 3.4797077688014078     |
| Linear Regression | WS     | None                                                                    | 2.040884277285756 | 2.629175443839345      |
| Random Forest     | WS     | max_depth=5, min_samples_leaf=5, min_samples_split=20, n_estimators=100 | 1.7877162450070447| 2.6083879757447757     |


## Explainability

To really understand the effect of a players play style we looked at the shap values from the random forest regressor. Below are the beeswarm plots for both the PER and the Win Shares model:

![Beeswarm PER](plots/shap_beeswarm_per.png)

![Beeswarm WS](plots/shap_beeswarm_ws.png)

Interestingly on the Win Shares beeswarm plot you can see that the cluster labels designed to motch player archetypes had very little to no impact at all on the predicted value. The most impactful label being the cluster label 3, which corresponds to primary offensive engines. For efficiency though it's a slightly different story. Looking at the PER bee swarm plot you can see that being labeled in the 4th or 5th cluster (low usage floor spacers and balanced role players) would actively bring down a players predicted PER.

Finally to evaluate if a player is an under performer or an over performer we looked at the residuals from the cross validated predicted values. Since the Linear Model had a slightly better performance on PER we compared the residuals from the linear model for PER vs a players actual PER, and the residuals from the Random Forest Win Shares to a players actual Win Shares. From there players were placed into three different groups: under performers, as expected performers, and over performers. If the residual from the predicted value (actual - predicted) was larger than the respective models RMSE, then player was classified as an over performer, if the residual was negative but the absolute value was larger than the respective models RMSE then a player was classified as an under performer. All else were classified as an as expected performer.

## Final Takeaways

In conclusion, we found that play style (as defined in this analysis) wasn't overly impactful in predicting a players success on the court. Play style has more of an effect on predicting a players PER, and a small impact on predicting Win Shares, but it really goes to show that any play style can be successful on the court. Additionally we were able to classify players as over and under performers based off of their predicted PER and Win Shares. Below is a table of every player and their classification as over or under performers.

|     | Player                   | Team   | cluster_9_label                     | perf_label_per   | perf_label_ws   |
|----:|:-------------------------|:-------|:------------------------------------|:-----------------|:----------------|
|   0 | Shai Gilgeous-Alexander  | OKC    | Interior Scoring Stars              | Overperformer    | Overperformer   |
|   1 | Giannis Antetokounmpo    | MIL    | Interior Scoring Stars              | Overperformer    | Overperformer   |
|   2 | Nikola Jokić             | DEN    | Interior Scoring Stars              | Overperformer    | Overperformer   |
|   3 | Luka Dončić              | DAL    | Primary Offensive Engines           | Overperformer    | As Expected     |
|   4 | Luka Dončić              | LAL    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|   5 | Anthony Edwards          | MIN    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|   6 | Jayson Tatum             | BOS    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|   7 | Kevin Durant             | PHO    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|   8 | Tyrese Maxey             | PHI    | Primary Offensive Engines           | As Expected      | Overperformer   |
|   9 | Cade Cunningham          | DET    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  10 | Jalen Brunson            | NYK    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  11 | Paolo Banchero           | ORL    | Interior Scoring Stars              | As Expected      | As Expected     |
|  12 | Devin Booker             | PHO    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  13 | LaMelo Ball              | CHO    | Primary Offensive Engines           | As Expected      | As Expected     |
|  14 | Damian Lillard           | MIL    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|  15 | Anthony Davis            | LAL    | Interior Scoring Stars              | Overperformer    | Overperformer   |
|  16 | Anthony Davis            | DAL    | Interior Scoring Stars              | As Expected      | As Expected     |
|  17 | Kyrie Irving             | DAL    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  18 | Zion Williamson          | NOP    | Interior Scoring Stars              | As Expected      | As Expected     |
|  19 | Stephen Curry            | GSW    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|  20 | LeBron James             | LAL    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|  21 | Karl-Anthony Towns       | NYK    | Interior Scoring Stars              | Overperformer    | Overperformer   |
|  22 | Victor Wembanyama        | SAS    | Stretch Bigs                        | Overperformer    | Overperformer   |
|  23 | Franz Wagner             | ORL    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  24 | Trae Young               | ATL    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  25 | Donovan Mitchell         | CLE    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|  26 | Cam Thomas               | BRK    | Primary Offensive Engines           | As Expected      | As Expected     |
|  27 | Tyler Herro              | MIA    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|  28 | Joel Embiid              | PHI    | Interior Scoring Stars              | As Expected      | As Expected     |
|  29 | De'Aaron Fox             | SAC    | Primary Offensive Engines           | As Expected      | As Expected     |
|  30 | De'Aaron Fox             | SAS    | Primary Offensive Engines           | As Expected      | As Expected     |
|  31 | Zach LaVine              | CHI    | Primary Offensive Engines           | As Expected      | As Expected     |
|  32 | Zach LaVine              | SAC    | Primary Offensive Engines           | As Expected      | As Expected     |
|  33 | Ja Morant                | MEM    | Primary Offensive Engines           | As Expected      | As Expected     |
|  34 | James Harden             | LAC    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|  35 | Jaylen Brown             | BOS    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  36 | DeMar DeRozan            | SAC    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  37 | Brandon Ingram           | NOP    | Primary Offensive Engines           | As Expected      | As Expected     |
|  38 | Jaren Jackson Jr.        | MEM    | Interior Scoring Stars              | As Expected      | Overperformer   |
|  39 | Norman Powell            | LAC    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  40 | Jalen Williams           | OKC    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  41 | Kawhi Leonard            | LAC    | Primary Offensive Engines           | As Expected      | As Expected     |
|  42 | Jamal Murray             | DEN    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  43 | Trey Murphy III          | NOP    | Primary Offensive Engines           | As Expected      | As Expected     |
|  44 | RJ Barrett               | TOR    | Primary Offensive Engines           | As Expected      | As Expected     |
|  45 | CJ McCollum              | NOP    | Primary Offensive Engines           | As Expected      | As Expected     |
|  46 | Jalen Green              | HOU    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  47 | Brandon Miller           | CHO    | Primary Offensive Engines           | As Expected      | As Expected     |
|  48 | Darius Garland           | CLE    | Primary Offensive Engines           | Overperformer    | Overperformer   |
|  49 | Jordan Poole             | WAS    | Primary Offensive Engines           | As Expected      | As Expected     |
|  50 | Coby White               | CHI    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  51 | Miles Bridges            | CHO    | Primary Offensive Engines           | As Expected      | As Expected     |
|  52 | Austin Reaves            | LAL    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  53 | Pascal Siakam            | IND    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  54 | Kristaps Porziņģis       | BOS    | Stretch Bigs                        | Overperformer    | Overperformer   |
|  55 | Scottie Barnes           | TOR    | Interior Scoring Stars              | As Expected      | As Expected     |
|  56 | Anfernee Simons          | POR    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  57 | Desmond Bane             | MEM    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  58 | Domantas Sabonis         | SAC    | Interior Scoring Stars              | Overperformer    | Overperformer   |
|  59 | Alperen Şengün           | HOU    | Interior Scoring Stars              | As Expected      | Overperformer   |
|  60 | John Collins             | UTA    | Interior Scoring Stars              | As Expected      | As Expected     |
|  61 | Lauri Markkanen          | UTA    | Primary Offensive Engines           | As Expected      | As Expected     |
|  62 | Jalen Johnson            | ATL    | Interior Scoring Stars              | As Expected      | As Expected     |
|  63 | Cameron Johnson          | BRK    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  64 | Julius Randle            | MIN    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  65 | Tyrese Haliburton        | IND    | Secondary Playmakers                | Overperformer    | Overperformer   |
|  66 | Evan Mobley              | CLE    | Interior Scoring Stars              | Overperformer    | Overperformer   |
|  67 | Shaedon Sharpe           | POR    | Primary Offensive Engines           | As Expected      | As Expected     |
|  68 | Nikola Vučević           | CHI    | Stretch Bigs                        | Overperformer    | Overperformer   |
|  69 | Collin Sexton            | UTA    | Primary Offensive Engines           | As Expected      | As Expected     |
|  70 | Michael Porter Jr.       | DEN    | Balanced Role Players               | Overperformer    | Overperformer   |
|  71 | Bam Adebayo              | MIA    | Interior Scoring Stars              | As Expected      | Overperformer   |
|  72 | Andrew Wiggins           | GSW    | Primary Offensive Engines           | As Expected      | As Expected     |
|  73 | Andrew Wiggins           | MIA    | Primary Offensive Engines           | As Expected      | As Expected     |
|  74 | OG Anunoby               | NYK    | Balanced Role Players               | As Expected      | Overperformer   |
|  75 | Mikal Bridges            | NYK    | Secondary Playmakers                | As Expected      | Overperformer   |
|  76 | Jaden Ivey               | DET    | Primary Offensive Engines           | As Expected      | As Expected     |
|  77 | Jimmy Butler             | MIA    | Interior Scoring Stars              | As Expected      | As Expected     |
|  78 | Jimmy Butler             | GSW    | Interior Scoring Stars              | As Expected      | Overperformer   |
|  79 | Dejounte Murray          | NOP    | Primary Offensive Engines           | As Expected      | As Expected     |
|  80 | Malik Monk               | SAC    | Primary Offensive Engines           | As Expected      | As Expected     |
|  81 | Immanuel Quickley        | TOR    | Primary Offensive Engines           | As Expected      | As Expected     |
|  82 | De'Andre Hunter          | ATL    | Primary Offensive Engines           | As Expected      | As Expected     |
|  83 | De'Andre Hunter          | CLE    | Balanced Role Players               | As Expected      | As Expected     |
|  84 | Bradley Beal             | PHO    | Secondary Playmakers                | As Expected      | As Expected     |
|  85 | Deni Avdija              | POR    | Primary Offensive Engines           | As Expected      | Overperformer   |
|  86 | Keyonte George           | UTA    | Primary Offensive Engines           | As Expected      | As Expected     |
|  87 | Derrick White            | BOS    | High Volume Three Point Specialists | Overperformer    | Overperformer   |
|  88 | Malik Beasley            | DET    | High Volume Three Point Specialists | As Expected      | Overperformer   |
|  89 | Devin Vassell            | SAS    | High Volume Three Point Specialists | As Expected      | As Expected     |
|  90 | Jordan Clarkson          | UTA    | Primary Offensive Engines           | As Expected      | As Expected     |
|  91 | Paul George              | PHI    | Secondary Playmakers                | As Expected      | As Expected     |
|  92 | Jalen Suggs              | ORL    | Primary Offensive Engines           | As Expected      | As Expected     |
|  93 | Bennedict Mathurin       | IND    | Primary Offensive Engines           | As Expected      | As Expected     |
|  94 | Myles Turner             | IND    | Stretch Bigs                        | As Expected      | Overperformer   |
|  95 | Christian Braun          | DEN    | Balanced Role Players               | As Expected      | Overperformer   |
|  96 | Jonathan Kuminga         | GSW    | Interior Scoring Stars              | Underperformer   | As Expected     |
|  97 | Jared McCain             | PHI    | Primary Offensive Engines           | As Expected      | As Expected     |
|  98 | Mark Williams            | CHO    | Interior Scoring Stars              | Overperformer    | As Expected     |
|  99 | Kelly Oubre Jr.          | PHI    | Balanced Role Players               | As Expected      | As Expected     |
| 100 | Chet Holmgren            | OKC    | Stretch Bigs                        | As Expected      | As Expected     |
| 101 | Kyle Kuzma               | WAS    | Primary Offensive Engines           | Underperformer   | As Expected     |
| 102 | Kyle Kuzma               | MIL    | Balanced Role Players               | As Expected      | As Expected     |
| 103 | Stephon Castle           | SAS    | Primary Offensive Engines           | As Expected      | As Expected     |
| 104 | Aaron Gordon             | DEN    | Balanced Role Players               | Overperformer    | Overperformer   |
| 105 | P.J. Washington          | DAL    | Balanced Role Players               | As Expected      | As Expected     |
| 106 | Quentin Grimes           | DAL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 107 | Quentin Grimes           | PHI    | Primary Offensive Engines           | As Expected      | As Expected     |
| 108 | Josh Giddey              | CHI    | Secondary Playmakers                | Overperformer    | Overperformer   |
| 109 | Jakob Poeltl             | TOR    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 110 | Deandre Ayton            | POR    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 111 | Gradey Dick              | TOR    | Balanced Role Players               | As Expected      | As Expected     |
| 112 | Jerami Grant             | POR    | Balanced Role Players               | As Expected      | As Expected     |
| 113 | Payton Pritchard         | BOS    | High Volume Three Point Specialists | Overperformer    | Overperformer   |
| 114 | Naz Reid                 | MIN    | Stretch Bigs                        | As Expected      | Overperformer   |
| 115 | Dyson Daniels            | ATL    | Defensive Guards                    | As Expected      | Overperformer   |
| 116 | Tre Mann                 | CHO    | Primary Offensive Engines           | As Expected      | As Expected     |
| 117 | Amen Thompson            | HOU    | Traditional Interior Bigs           | As Expected      | Overperformer   |
| 118 | Fred VanVleet            | HOU    | Secondary Playmakers                | As Expected      | Overperformer   |
| 119 | Dillon Brooks            | HOU    | High Volume Three Point Specialists | As Expected      | Overperformer   |
| 120 | Klay Thompson            | DAL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 121 | Bobby Portis             | MIL    | Stretch Bigs                        | As Expected      | As Expected     |
| 122 | Tobias Harris            | DET    | Balanced Role Players               | As Expected      | Overperformer   |
| 123 | Josh Hart                | NYK    | Balanced Role Players               | Overperformer    | Overperformer   |
| 124 | Jarrett Allen            | CLE    | Traditional Interior Bigs           | Overperformer    | Overperformer   |
| 125 | Onyeka Okongwu           | ATL    | Traditional Interior Bigs           | As Expected      | Overperformer   |
| 126 | Russell Westbrook        | DEN    | Secondary Playmakers                | As Expected      | As Expected     |
| 127 | Naji Marshall            | DAL    | Balanced Role Players               | As Expected      | As Expected     |
| 128 | Dennis Schröder          | BRK    | Primary Offensive Engines           | As Expected      | As Expected     |
| 129 | Dennis Schröder          | GSW    | Secondary Playmakers                | Underperformer   | As Expected     |
| 130 | Dennis Schröder          | DET    | Secondary Playmakers                | As Expected      | As Expected     |
| 131 | Rui Hachimura            | LAL    | Balanced Role Players               | As Expected      | Overperformer   |
| 132 | Brook Lopez              | MIL    | Stretch Bigs                        | As Expected      | Overperformer   |
| 133 | Alex Sarr                | WAS    | Stretch Bigs                        | Underperformer   | Underperformer  |
| 134 | Moritz Wagner            | ORL    | Interior Scoring Stars              | As Expected      | As Expected     |
| 135 | Malcolm Brogdon          | WAS    | Primary Offensive Engines           | As Expected      | Underperformer  |
| 136 | Scoot Henderson          | POR    | Secondary Playmakers                | As Expected      | As Expected     |
| 137 | Keldon Johnson           | SAS    | Balanced Role Players               | As Expected      | As Expected     |
| 138 | D'Angelo Russell         | LAL    | Secondary Playmakers                | As Expected      | As Expected     |
| 139 | D'Angelo Russell         | BRK    | Primary Offensive Engines           | As Expected      | As Expected     |
| 140 | Zaccharie Risacher       | ATL    | Balanced Role Players               | As Expected      | As Expected     |
| 141 | Santi Aldama             | MEM    | Balanced Role Players               | Overperformer    | Overperformer   |
| 142 | Ty Jerome                | CLE    | Primary Offensive Engines           | Overperformer    | Overperformer   |
| 143 | Keegan Murray            | SAC    | Low Usage Floor Spacers             | As Expected      | Overperformer   |
| 144 | Lonnie Walker IV         | PHI    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 145 | Harrison Barnes          | SAS    | Balanced Role Players               | As Expected      | Overperformer   |
| 146 | Bilal Coulibaly          | WAS    | Balanced Role Players               | As Expected      | As Expected     |
| 147 | Ayo Dosunmu              | CHI    | Secondary Playmakers                | As Expected      | As Expected     |
| 148 | Jaden McDaniels          | MIN    | Balanced Role Players               | As Expected      | Overperformer   |
| 149 | Jabari Smith Jr.         | HOU    | Balanced Role Players               | As Expected      | Overperformer   |
| 150 | Caris LeVert             | CLE    | Secondary Playmakers                | As Expected      | As Expected     |
| 151 | Caris LeVert             | ATL    | Primary Offensive Engines           | As Expected      | As Expected     |
| 152 | Drew Timme               | BRK    | Balanced Role Players               | As Expected      | As Expected     |
| 153 | Tari Eason               | HOU    | Defensive Guards                    | Overperformer    | Overperformer   |
| 154 | Aaron Nesmith            | IND    | Balanced Role Players               | As Expected      | As Expected     |
| 155 | Aaron Wiggins            | OKC    | High Volume Three Point Specialists | As Expected      | Overperformer   |
| 156 | Khris Middleton          | MIL    | Secondary Playmakers                | Overperformer    | As Expected     |
| 157 | Khris Middleton          | WAS    | Secondary Playmakers                | As Expected      | As Expected     |
| 158 | Donte DiVincenzo         | MIN    | High Volume Three Point Specialists | Overperformer    | Overperformer   |
| 159 | Brandin Podziemski       | GSW    | Secondary Playmakers                | As Expected      | As Expected     |
| 160 | Corey Kispert            | WAS    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 161 | Jeremy Sochan            | SAS    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 162 | Toumani Camara           | POR    | Low Usage Floor Spacers             | As Expected      | Overperformer   |
| 163 | Isaiah Hartenstein       | OKC    | Traditional Interior Bigs           | As Expected      | Overperformer   |
| 164 | Buddy Hield              | GSW    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 165 | Jrue Holiday             | BOS    | Low Usage Floor Spacers             | As Expected      | Overperformer   |
| 166 | Walker Kessler           | UTA    | Traditional Interior Bigs           | Overperformer    | Overperformer   |
| 167 | Gary Trent Jr.           | MIL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 168 | Spencer Dinwiddie        | DAL    | Secondary Playmakers                | As Expected      | As Expected     |
| 169 | Tim Hardaway Jr.         | DET    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 170 | Duncan Robinson          | MIA    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 171 | Guerschon Yabusele       | PHI    | Balanced Role Players               | Overperformer    | As Expected     |
| 172 | Brice Sensabaugh         | UTA    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 173 | Bogdan Bogdanović        | ATL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 174 | Bogdan Bogdanović        | LAC    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 175 | Jordan Hawkins           | NOP    | High Volume Three Point Specialists | As Expected      | Underperformer  |
| 176 | Brandon Boston Jr.       | NOP    | Secondary Playmakers                | As Expected      | As Expected     |
| 177 | Nikola Jović             | MIA    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 178 | Grayson Allen            | PHO    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 179 | Keon Johnson             | BRK    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 180 | Terry Rozier             | MIA    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 181 | Obi Toppin               | IND    | Balanced Role Players               | Overperformer    | Overperformer   |
| 182 | Jonas Valančiūnas        | WAS    | Interior Scoring Stars              | As Expected      | As Expected     |
| 183 | Jonas Valančiūnas        | SAC    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 184 | Ochai Agbaji             | TOR    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 185 | Jaylen Wells             | MEM    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 186 | Grant Williams           | CHO    | Balanced Role Players               | As Expected      | As Expected     |
| 187 | Kevin Porter Jr.         | LAC    | Secondary Playmakers                | As Expected      | As Expected     |
| 188 | Kevin Porter Jr.         | MIL    | Primary Offensive Engines           | As Expected      | As Expected     |
| 189 | Jose Alvarado            | NOP    | Secondary Playmakers                | As Expected      | As Expected     |
| 190 | Nic Claxton              | BRK    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 191 | Herbert Jones            | NOP    | Defensive Guards                    | As Expected      | As Expected     |
| 192 | De'Anthony Melton        | GSW    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 193 | Isaiah Joe               | OKC    | High Volume Three Point Specialists | As Expected      | Overperformer   |
| 194 | Tyus Jones               | PHO    | Secondary Playmakers                | Overperformer    | Overperformer   |
| 195 | Trendon Watford          | BRK    | Primary Offensive Engines           | Underperformer   | As Expected     |
| 196 | Keion Brooks Jr.         | NOP    | Balanced Role Players               | As Expected      | As Expected     |
| 197 | Luguentz Dort            | OKC    | Low Usage Floor Spacers             | As Expected      | Overperformer   |
| 198 | Justin Edwards           | PHI    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 199 | Derrick Jones Jr.        | LAC    | Balanced Role Players               | As Expected      | Overperformer   |
| 200 | Ausar Thompson           | DET    | Defensive Guards                    | As Expected      | As Expected     |
| 201 | Chris Boucher            | TOR    | Stretch Bigs                        | As Expected      | As Expected     |
| 202 | Andrew Nembhard          | IND    | Secondary Playmakers                | As Expected      | As Expected     |
| 203 | Ziaire Williams          | BRK    | Balanced Role Players               | As Expected      | As Expected     |
| 204 | Kevin Huerter            | SAC    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 205 | Kevin Huerter            | CHI    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 206 | Georges Niang            | CLE    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 207 | Georges Niang            | ATL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 208 | Julian Champagnie        | SAS    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 209 | Scotty Pippen Jr.        | MEM    | Secondary Playmakers                | As Expected      | Overperformer   |
| 210 | Nick Smith Jr.           | CHO    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 211 | Bub Carrington           | WAS    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 212 | Moses Moody              | GSW    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 213 | Amir Coffey              | LAC    | Balanced Role Players               | As Expected      | As Expected     |
| 214 | Max Christie             | LAL    | Balanced Role Players               | As Expected      | As Expected     |
| 215 | Max Christie             | DAL    | Balanced Role Players               | As Expected      | As Expected     |
| 216 | Kyle Filipowski          | UTA    | Balanced Role Players               | As Expected      | As Expected     |
| 217 | Tosan Evbuomwan          | BRK    | Balanced Role Players               | As Expected      | As Expected     |
| 218 | Miles McBride            | NYK    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 219 | Jalen Wilson             | BRK    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 220 | Nickeil Alexander-Walker | MIN    | High Volume Three Point Specialists | As Expected      | Overperformer   |
| 221 | Cole Anthony             | ORL    | Primary Offensive Engines           | As Expected      | As Expected     |
| 222 | Anthony Black            | ORL    | Balanced Role Players               | As Expected      | As Expected     |
| 223 | Max Strus                | CLE    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 224 | Tristan Vukcevic         | WAS    | Stretch Bigs                        | As Expected      | As Expected     |
| 225 | Cam Whitmore             | HOU    | Primary Offensive Engines           | As Expected      | As Expected     |
| 226 | Nick Richards            | CHO    | Traditional Interior Bigs           | As Expected      | Underperformer  |
| 227 | Nick Richards            | PHO    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 228 | Kel'el Ware              | MIA    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 229 | Zach Edey                | MEM    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 230 | Wendell Carter Jr.       | ORL    | Balanced Role Players               | As Expected      | Overperformer   |
| 231 | Noah Clowney             | BRK    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 232 | Dalton Knecht            | LAL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 233 | A.J. Lawson              | TOR    | Balanced Role Players               | As Expected      | As Expected     |
| 234 | T.J. McConnell           | IND    | Secondary Playmakers                | As Expected      | As Expected     |
| 235 | Yves Missi               | NOP    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 236 | Royce O'Neale            | PHO    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 237 | Jared Butler             | WAS    | Primary Offensive Engines           | As Expected      | As Expected     |
| 238 | Jared Butler             | PHI    | Secondary Playmakers                | As Expected      | As Expected     |
| 239 | Marcus Smart             | MEM    | Secondary Playmakers                | As Expected      | As Expected     |
| 240 | Marcus Smart             | WAS    | Secondary Playmakers                | As Expected      | As Expected     |
| 241 | Draymond Green           | GSW    | Secondary Playmakers                | As Expected      | Overperformer   |
| 242 | Killian Hayes            | BRK    | Secondary Playmakers                | As Expected      | As Expected     |
| 243 | Al Horford               | BOS    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 244 | Julian Strawther         | DEN    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 245 | Patrick Williams         | CHI    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 246 | Jusuf Nurkić             | PHO    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 247 | Jusuf Nurkić             | CHO    | Interior Scoring Stars              | As Expected      | As Expected     |
| 248 | Clint Capela             | ATL    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 249 | Johnny Juzang            | UTA    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 250 | Luke Kennard             | MEM    | High Volume Three Point Specialists | Overperformer    | Overperformer   |
| 251 | Justin Champagnie        | WAS    | Low Usage Floor Spacers             | Overperformer    | As Expected     |
| 252 | Svi Mykhailiuk           | UTA    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 253 | Chris Paul               | SAS    | Secondary Playmakers                | Overperformer    | Overperformer   |
| 254 | Kelly Olynyk             | TOR    | Balanced Role Players               | As Expected      | As Expected     |
| 255 | Kelly Olynyk             | NOP    | Balanced Role Players               | As Expected      | As Expected     |
| 256 | Dorian Finney-Smith      | BRK    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 257 | Dorian Finney-Smith      | LAL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 258 | Oshae Brissett           | PHI    | Balanced Role Players               | As Expected      | As Expected     |
| 259 | Kentavious Caldwell-Pope | ORL    | Low Usage Floor Spacers             | As Expected      | Overperformer   |
| 260 | Isaiah Collier           | UTA    | Secondary Playmakers                | As Expected      | As Expected     |
| 261 | Danté Exum               | DAL    | Secondary Playmakers                | As Expected      | As Expected     |
| 262 | Kyshawn George           | WAS    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 263 | Jaden Hardy              | DAL    | Primary Offensive Engines           | Underperformer   | As Expected     |
| 264 | Tyrese Martin            | BRK    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 265 | Matas Buzelis            | CHI    | Stretch Bigs                        | As Expected      | As Expected     |
| 266 | Jaime Jaquez Jr.         | MIA    | Balanced Role Players               | As Expected      | As Expected     |
| 267 | Ja'Kobe Walter           | TOR    | Balanced Role Players               | As Expected      | As Expected     |
| 268 | Sam Hauser               | BOS    | High Volume Three Point Specialists | As Expected      | Overperformer   |
| 269 | Larry Nance Jr.          | ATL    | Low Usage Floor Spacers             | Overperformer    | As Expected     |
| 270 | Jared Rhoden             | TOR    | Balanced Role Players               | As Expected      | As Expected     |
| 271 | Jaylen Nowell            | NOP    | Balanced Role Players               | Underperformer   | Underperformer  |
| 272 | Cason Wallace            | OKC    | Low Usage Floor Spacers             | As Expected      | Overperformer   |
| 273 | Bruce Brown              | TOR    | Balanced Role Players               | As Expected      | Underperformer  |
| 274 | Bruce Brown              | NOP    | Balanced Role Players               | As Expected      | As Expected     |
| 275 | Dalano Banton            | POR    | Primary Offensive Engines           | As Expected      | As Expected     |
| 276 | Brandon Clarke           | MEM    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 277 | Keon Ellis               | SAC    | Low Usage Floor Spacers             | Overperformer    | Overperformer   |
| 278 | Brandon Williams         | DAL    | Primary Offensive Engines           | As Expected      | As Expected     |
| 279 | Mike Conley              | MIN    | Secondary Playmakers                | As Expected      | Overperformer   |
| 280 | Taurean Prince           | MIL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 281 | Jalen Smith              | CHI    | Stretch Bigs                        | As Expected      | As Expected     |
| 282 | Quinten Post             | GSW    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 283 | Peyton Watson            | DEN    | Balanced Role Players               | As Expected      | As Expected     |
| 284 | Davion Mitchell          | TOR    | Secondary Playmakers                | As Expected      | As Expected     |
| 285 | Davion Mitchell          | MIA    | Secondary Playmakers                | As Expected      | As Expected     |
| 286 | Caleb Martin             | PHI    | Balanced Role Players               | As Expected      | As Expected     |
| 287 | Caleb Martin             | DAL    | Balanced Role Players               | Underperformer   | As Expected     |
| 288 | Tyson Etienne            | BRK    | High Volume Three Point Specialists | Underperformer   | As Expected     |
| 289 | Day'Ron Sharpe           | BRK    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 290 | KJ Simpson               | CHO    | Secondary Playmakers                | Underperformer   | As Expected     |
| 291 | Terance Mann             | LAC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 292 | Terance Mann             | ATL    | Balanced Role Players               | As Expected      | As Expected     |
| 293 | Karlo Matković           | NOP    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 294 | AJ Johnson               | MIL    | Secondary Playmakers                | Underperformer   | As Expected     |
| 295 | AJ Johnson               | WAS    | Secondary Playmakers                | Underperformer   | As Expected     |
| 296 | Lonzo Ball               | CHI    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 297 | Garrison Mathews         | ATL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 298 | Matisse Thybulle         | POR    | Defensive Guards                    | Overperformer    | As Expected     |
| 299 | A.J. Green               | MIL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 300 | Josh Green               | CHO    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 301 | Richaun Holmes           | WAS    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 302 | Damion Baugh             | CHO    | Secondary Playmakers                | Underperformer   | As Expected     |
| 303 | Alec Burks               | MIA    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 304 | Ricky Council IV         | PHI    | Balanced Role Players               | As Expected      | Underperformer  |
| 305 | Andre Drummond           | PHI    | Traditional Interior Bigs           | As Expected      | Underperformer  |
| 306 | Tre Jones                | SAS    | Secondary Playmakers                | As Expected      | As Expected     |
| 307 | Tre Jones                | CHI    | Secondary Playmakers                | Overperformer    | As Expected     |
| 308 | Goga Bitadze             | ORL    | Traditional Interior Bigs           | As Expected      | Overperformer   |
| 309 | Tristan Da Silva         | ORL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 310 | GG Jackson II            | MEM    | Balanced Role Players               | As Expected      | As Expected     |
| 311 | Vít Krejčí               | ATL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 312 | Sam Merrill              | CLE    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 313 | Daeqwon Plowden          | ATL    | High Volume Three Point Specialists | Overperformer    | As Expected     |
| 314 | Nae'Qwan Tomlin          | CLE    | Interior Scoring Stars              | Underperformer   | Underperformer  |
| 315 | Josh Okogie              | PHO    | Defensive Guards                    | As Expected      | As Expected     |
| 316 | Josh Okogie              | CHO    | Defensive Guards                    | As Expected      | Underperformer  |
| 317 | Jalen Hood-Schifino      | PHI    | Secondary Playmakers                | Underperformer   | As Expected     |
| 318 | Jamison Battle           | TOR    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 319 | Alex Caruso              | OKC    | Defensive Guards                    | Overperformer    | As Expected     |
| 320 | Jamal Shead              | TOR    | Secondary Playmakers                | As Expected      | As Expected     |
| 321 | Jeff Dowtin Jr.          | PHI    | Secondary Playmakers                | As Expected      | As Expected     |
| 322 | Marcus Garrett           | CHO    | Secondary Playmakers                | Underperformer   | As Expected     |
| 323 | Jaylen Sims              | CHO    | Balanced Role Players               | As Expected      | As Expected     |
| 324 | Orlando Robinson         | SAC    | Balanced Role Players               | As Expected      | As Expected     |
| 325 | Orlando Robinson         | TOR    | Traditional Interior Bigs           | Underperformer   | Underperformer  |
| 326 | Jake LaRavia             | MEM    | Balanced Role Players               | As Expected      | As Expected     |
| 327 | Jake LaRavia             | SAC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 328 | Ryan Dunn                | PHO    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 329 | Jay Huff                 | MEM    | Stretch Bigs                        | Overperformer    | As Expected     |
| 330 | Cameron Payne            | NYK    | Secondary Playmakers                | As Expected      | As Expected     |
| 331 | Antonio Reeves           | NOP    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 332 | Cody Martin              | CHO    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 333 | Cody Martin              | PHO    | Defensive Guards                    | As Expected      | As Expected     |
| 334 | Bol Bol                  | PHO    | Stretch Bigs                        | As Expected      | As Expected     |
| 335 | Eric Gordon              | PHI    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 336 | Jaxson Hayes             | LAL    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 337 | Marcus Bagley            | PHI    | Low Usage Floor Spacers             | As Expected      | Underperformer  |
| 338 | DaQuan Jeffries          | CHO    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 339 | Lester Quiñones          | NOP    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 340 | Vasilije Micić           | CHO    | Secondary Playmakers                | Underperformer   | As Expected     |
| 341 | Precious Achiuwa         | NYK    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 342 | Trayce Jackson-Davis     | GSW    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 343 | Marcus Sasser            | DET    | Secondary Playmakers                | As Expected      | As Expected     |
| 344 | Vince Williams Jr.       | MEM    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 345 | Thomas Bryant            | MIA    | Stretch Bigs                        | As Expected      | As Expected     |
| 346 | Thomas Bryant            | IND    | Stretch Bigs                        | As Expected      | As Expected     |
| 347 | Donovan Clingan          | POR    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 348 | Seth Curry               | CHO    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 349 | Haywood Highsmith        | MIA    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 350 | Talen Horton-Tucker      | CHI    | Primary Offensive Engines           | As Expected      | As Expected     |
| 351 | Trey Lyles               | SAC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 352 | Ajay Mitchell            | OKC    | Secondary Playmakers                | As Expected      | As Expected     |
| 353 | Gary Payton II           | GSW    | Balanced Role Players               | Overperformer    | As Expected     |
| 354 | Zach Collins             | SAS    | Balanced Role Players               | As Expected      | As Expected     |
| 355 | Zach Collins             | CHI    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 356 | Kris Dunn                | LAC    | Low Usage Floor Spacers             | As Expected      | Overperformer   |
| 357 | Ron Holland              | DET    | Balanced Role Players               | As Expected      | As Expected     |
| 358 | KJ Martin                | PHI    | Balanced Role Players               | As Expected      | As Expected     |
| 359 | KJ Martin                | UTA    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 360 | Gabe Vincent             | LAL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 361 | Sandro Mamukelashvili    | SAS    | Stretch Bigs                        | Overperformer    | As Expected     |
| 362 | Jeremiah Robinson-Earl   | NOP    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 363 | Kenrich Williams         | OKC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 364 | Bones Hyland             | LAC    | Primary Offensive Engines           | As Expected      | As Expected     |
| 365 | Jonathan Mogbo           | TOR    | Balanced Role Players               | As Expected      | As Expected     |
| 366 | Ryan Rollins             | MIL    | Secondary Playmakers                | As Expected      | As Expected     |
| 367 | Dru Smith                | MIA    | Defensive Guards                    | As Expected      | As Expected     |
| 368 | Isaac Okoro              | CLE    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 369 | Jarace Walker            | IND    | Balanced Role Players               | As Expected      | As Expected     |
| 370 | Mouhamed Gueye           | ATL    | Stretch Bigs                        | As Expected      | As Expected     |
| 371 | Luke Kornet              | BOS    | Traditional Interior Bigs           | Overperformer    | Overperformer   |
| 372 | Isaiah Mobley            | PHI    | Secondary Playmakers                | As Expected      | As Expected     |
| 373 | Isaiah Stewart           | DET    | Traditional Interior Bigs           | As Expected      | Overperformer   |
| 374 | Isaiah Wong              | CHO    | Balanced Role Players               | Underperformer   | As Expected     |
| 375 | Cole Swider              | TOR    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 376 | Chuma Okeke              | PHI    | Low Usage Floor Spacers             | Overperformer    | As Expected     |
| 377 | Kyle Anderson            | GSW    | Secondary Playmakers                | As Expected      | As Expected     |
| 378 | Kyle Anderson            | MIA    | Balanced Role Players               | As Expected      | As Expected     |
| 379 | Simone Fontecchio        | DET    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 380 | Collin Gillespie         | PHO    | Secondary Playmakers                | Overperformer    | As Expected     |
| 381 | Tidjane Salaün           | CHO    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 382 | Jaylin Williams          | OKC    | Stretch Bigs                        | Overperformer    | As Expected     |
| 383 | Adem Bona                | PHI    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 384 | Quenton Jackson          | IND    | Defensive Guards                    | As Expected      | As Expected     |
| 385 | Robert Williams          | POR    | Traditional Interior Bigs           | Overperformer    | As Expected     |
| 386 | Moussa Diabaté           | CHO    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 387 | Dariq Whitehead          | BRK    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 388 | Landry Shamet            | NYK    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 389 | Jordan Goodwin           | LAL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 390 | Shake Milton             | BRK    | Secondary Playmakers                | As Expected      | As Expected     |
| 391 | Shake Milton             | LAL    | Balanced Role Players               | As Expected      | As Expected     |
| 392 | Aaron Holiday            | HOU    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 393 | Jeff Green               | HOU    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 394 | Jonathan Isaac           | ORL    | Stretch Bigs                        | As Expected      | As Expected     |
| 395 | Dean Wade                | CLE    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 396 | Keaton Wallace           | ATL    | Secondary Playmakers                | As Expected      | As Expected     |
| 397 | Kobe Bufkin              | ATL    | Balanced Role Players               | Underperformer   | Underperformer  |
| 398 | Jamal Cain               | NOP    | Balanced Role Players               | As Expected      | As Expected     |
| 399 | Pat Connaughton          | MIL    | Balanced Role Players               | As Expected      | As Expected     |
| 400 | Kevin Love               | MIA    | Stretch Bigs                        | As Expected      | As Expected     |
| 401 | Ben Sheppard             | IND    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 402 | Monte Morris             | PHO    | Secondary Playmakers                | As Expected      | As Expected     |
| 403 | Jabari Walker            | POR    | Balanced Role Players               | As Expected      | As Expected     |
| 404 | Javonte Green            | NOP    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 405 | Javonte Green            | CLE    | Defensive Guards                    | Underperformer   | As Expected     |
| 406 | Alex Reese               | PHI    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 407 | Kai Jones                | LAC    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 408 | Kai Jones                | DAL    | Traditional Interior Bigs           | Overperformer    | As Expected     |
| 409 | Malaki Branham           | SAS    | Primary Offensive Engines           | As Expected      | As Expected     |
| 410 | Neemias Queta            | BOS    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 411 | Jaylen Martin            | WAS    | Balanced Role Players               | As Expected      | As Expected     |
| 412 | Lindy Waters III         | GSW    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 413 | Trevelin Queen           | ORL    | Defensive Guards                    | As Expected      | As Expected     |
| 414 | Jock Landale             | HOU    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 415 | Colin Castleton          | TOR    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 416 | Colin Castleton          | PHI    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 417 | Taylor Hendricks         | UTA    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 418 | David Roddy              | ATL    | Balanced Role Players               | As Expected      | As Expected     |
| 419 | David Roddy              | HOU    | Balanced Role Players               | Underperformer   | Underperformer  |
| 420 | Drew Eubanks             | UTA    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 421 | Drew Eubanks             | LAC    | Traditional Interior Bigs           | As Expected      | Underperformer  |
| 422 | Pelle Larsson            | MIA    | Balanced Role Players               | As Expected      | As Expected     |
| 423 | Julian Phillips          | CHI    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 424 | Cody Williams            | UTA    | Low Usage Floor Spacers             | Underperformer   | As Expected     |
| 425 | Rob Dillingham           | MIN    | Secondary Playmakers                | As Expected      | As Expected     |
| 426 | Jett Howard              | ORL    | High Volume Three Point Specialists | Underperformer   | As Expected     |
| 427 | Kevon Looney             | GSW    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 428 | Mason Plumlee            | PHO    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 429 | Dalen Terry              | CHI    | Balanced Role Players               | As Expected      | As Expected     |
| 430 | Marvin Bagley III        | WAS    | Interior Scoring Stars              | As Expected      | Underperformer  |
| 431 | Marvin Bagley III        | MEM    | Traditional Interior Bigs           | Underperformer   | Underperformer  |
| 432 | Tony Bradley             | IND    | Traditional Interior Bigs           | Overperformer    | Underperformer  |
| 433 | Reggie Jackson           | PHI    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 434 | Reed Sheppard            | HOU    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 435 | Lamar Stevens            | MEM    | Stretch Bigs                        | As Expected      | As Expected     |
| 436 | Mo Bamba                 | LAC    | Stretch Bigs                        | As Expected      | As Expected     |
| 437 | Mo Bamba                 | NOP    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 438 | Jevon Carter             | CHI    | High Volume Three Point Specialists | As Expected      | Underperformer  |
| 439 | Micah Potter             | UTA    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 440 | Terrence Shannon Jr.     | MIN    | Balanced Role Players               | As Expected      | As Expected     |
| 441 | Daniel Theis             | NOP    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 442 | Torrey Craig             | CHI    | High Volume Three Point Specialists | Overperformer    | As Expected     |
| 443 | Torrey Craig             | BOS    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 444 | Wendell Moore Jr.        | DET    | Balanced Role Players               | As Expected      | As Expected     |
| 445 | Wendell Moore Jr.        | CHO    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 446 | Dominick Barlow          | ATL    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 447 | Kessler Edwards          | DAL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 448 | Oso Ighodaro             | PHO    | Traditional Interior Bigs           | Underperformer   | As Expected     |
| 449 | Kris Murray              | POR    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 450 | Duop Reath               | POR    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 451 | Cam Spencer              | MEM    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 452 | Maxwell Lewis            | BRK    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 453 | Jaylen Clark             | MIN    | Defensive Guards                    | As Expected      | As Expected     |
| 454 | Caleb Houstan            | ORL    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 455 | Jordan Miller            | LAC    | Balanced Role Players               | As Expected      | Underperformer  |
| 456 | Jalen Pickett            | DEN    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 457 | Paul Reed                | DET    | Defensive Guards                    | Overperformer    | As Expected     |
| 458 | Gui Santos               | GSW    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 459 | Jarred Vanderbilt        | LAL    | Defensive Guards                    | As Expected      | As Expected     |
| 460 | Colby Jones              | WAS    | Balanced Role Players               | As Expected      | As Expected     |
| 461 | Nicolas Batum            | LAC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 462 | Malachi Flynn            | CHO    | Defensive Guards                    | As Expected      | As Expected     |
| 463 | Ron Harper Jr.           | DET    | Stretch Bigs                        | Underperformer   | Underperformer  |
| 464 | Josh Richardson          | MIA    | Low Usage Floor Spacers             | Underperformer   | As Expected     |
| 465 | Steven Adams             | HOU    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 466 | Kyle Lowry               | PHI    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 467 | Olivier-Maxence Prosper  | DAL    | Balanced Role Players               | As Expected      | Underperformer  |
| 468 | Patty Mills              | UTA    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 469 | Patty Mills              | LAC    | High Volume Three Point Specialists | Overperformer    | As Expected     |
| 470 | Branden Carlson          | OKC    | Stretch Bigs                        | As Expected      | As Expected     |
| 471 | Devin Carter             | SAC    | Defensive Guards                    | Underperformer   | As Expected     |
| 472 | Ousmane Dieng            | OKC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 473 | Markieff Morris          | LAL    | High Volume Three Point Specialists | Underperformer   | As Expected     |
| 474 | Craig Porter Jr.         | CLE    | Balanced Role Players               | As Expected      | As Expected     |
| 475 | Jackson Rowe             | GSW    | Defensive Guards                    | As Expected      | As Expected     |
| 476 | Blake Wesley             | SAS    | Secondary Playmakers                | As Expected      | Underperformer  |
| 477 | JT Thor                  | WAS    | Balanced Role Players               | Underperformer   | Underperformer  |
| 478 | Baylor Scheierman        | BOS    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 479 | Jae'Sean Tate            | HOU    | Balanced Role Players               | As Expected      | As Expected     |
| 480 | Jaylon Tyson             | CLE    | Balanced Role Players               | As Expected      | As Expected     |
| 481 | Elfrid Payton            | NOP    | Secondary Playmakers                | As Expected      | Underperformer  |
| 482 | Luka Garza               | MIN    | Interior Scoring Stars              | As Expected      | As Expected     |
| 483 | Cory Joseph              | ORL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 484 | Doug McDermott           | SAC    | High Volume Three Point Specialists | As Expected      | As Expected     |
| 485 | Dario Šarić              | DEN    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 486 | Jamaree Bouyea           | MIL    | Defensive Guards                    | As Expected      | Underperformer  |
| 487 | Andre Jackson Jr.        | MIL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 488 | Isaac Jones              | SAC    | Traditional Interior Bigs           | As Expected      | Underperformer  |
| 489 | Kevin Knox               | GSW    | Stretch Bigs                        | As Expected      | Underperformer  |
| 490 | Damion Lee               | PHO    | Primary Offensive Engines           | Underperformer   | Underperformer  |
| 491 | Nate Williams            | HOU    | Secondary Playmakers                | Underperformer   | As Expected     |
| 492 | Elijah Harkless          | UTA    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 493 | Zeke Nnaji               | DEN    | Balanced Role Players               | As Expected      | As Expected     |
| 494 | Cam Reddish              | LAL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 495 | Delon Wright             | MIL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 496 | Delon Wright             | NYK    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 497 | Gary Harris              | ORL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 498 | Maxi Kleber              | DAL    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 499 | Taze Moore               | POR    | Defensive Guards                    | Underperformer   | As Expected     |
| 500 | Rayan Rupert             | POR    | Balanced Role Players               | As Expected      | As Expected     |
| 501 | Pete Nance               | PHI    | Low Usage Floor Spacers             | Underperformer   | As Expected     |
| 502 | Markelle Fultz           | SAC    | Secondary Playmakers                | Underperformer   | Underperformer  |
| 503 | Taj Gibson               | CHO    | Traditional Interior Bigs           | Underperformer   | As Expected     |
| 504 | Tyler Smith              | MIL    | Stretch Bigs                        | As Expected      | As Expected     |
| 505 | RayJ Dennis              | IND    | Defensive Guards                    | As Expected      | As Expected     |
| 506 | David Duke Jr.           | SAS    | Secondary Playmakers                | As Expected      | Underperformer  |
| 507 | Keshad Johnson           | MIA    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 508 | Reece Beekman            | BRK    | Defensive Guards                    | Underperformer   | As Expected     |
| 509 | Jae Crowder              | SAC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 510 | Josh Minott              | MIN    | Stretch Bigs                        | As Expected      | As Expected     |
| 511 | Hunter Tyson             | DEN    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 512 | Jaden Springer           | BOS    | Defensive Guards                    | As Expected      | As Expected     |
| 513 | Jaden Springer           | UTA    | Defensive Guards                    | As Expected      | As Expected     |
| 514 | Anthony Gill             | WAS    | Balanced Role Players               | As Expected      | As Expected     |
| 515 | Dillon Jones             | OKC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 516 | Pat Spencer              | GSW    | Secondary Playmakers                | As Expected      | As Expected     |
| 517 | Johnny Davis             | WAS    | Defensive Guards                    | Underperformer   | Underperformer  |
| 518 | Christian Koloko         | LAL    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 519 | John Konchar             | MEM    | Low Usage Floor Spacers             | Overperformer    | As Expected     |
| 520 | MarJon Beauchamp         | LAC    | Primary Offensive Engines           | As Expected      | As Expected     |
| 521 | Bronny James             | LAL    | Secondary Playmakers                | Underperformer   | As Expected     |
| 522 | Miles Norris             | BOS    | Low Usage Floor Spacers             | Underperformer   | Underperformer  |
| 523 | Drew Peterson            | BOS    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 524 | TyTy Washington Jr.      | PHO    | Secondary Playmakers                | Underperformer   | Underperformer  |
| 525 | Jordan McLaughlin        | SAC    | Defensive Guards                    | As Expected      | As Expected     |
| 526 | Jordan McLaughlin        | SAS    | Secondary Playmakers                | Overperformer    | As Expected     |
| 527 | JD Davison               | BOS    | Secondary Playmakers                | Underperformer   | As Expected     |
| 528 | Enrique Freeman          | IND    | Balanced Role Players               | Underperformer   | As Expected     |
| 529 | Johnny Furphy            | IND    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 530 | Dwight Powell            | DAL    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 531 | Tyler Kolek              | NYK    | Secondary Playmakers                | As Expected      | As Expected     |
| 532 | Kobe Brown               | LAC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 533 | Bobi Klintman            | DET    | Secondary Playmakers                | Overperformer    | As Expected     |
| 534 | Garrett Temple           | TOR    | Defensive Guards                    | Underperformer   | As Expected     |
| 535 | Adam Flagler             | OKC    | High Volume Three Point Specialists | Underperformer   | Underperformer  |
| 536 | Pacôme Dadiet            | NYK    | Low Usage Floor Spacers             | Underperformer   | Underperformer  |
| 537 | Alex Ducas               | OKC    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 538 | Tristan Thompson         | CLE    | Traditional Interior Bigs           | Underperformer   | Underperformer  |
| 539 | Alex Len                 | SAC    | Traditional Interior Bigs           | As Expected      | As Expected     |
| 540 | Alex Len                 | LAL    | Traditional Interior Bigs           | Underperformer   | As Expected     |
| 541 | Armel Traoré             | LAL    | Balanced Role Players               | Underperformer   | As Expected     |
| 542 | Jordan Walsh             | BOS    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 543 | Phillip Wheeler          | PHI    | Stretch Bigs                        | Underperformer   | Underperformer  |
| 544 | Sidy Cissoko             | POR    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 545 | Kevin McCullar Jr.       | NYK    | Traditional Interior Bigs           | Underperformer   | As Expected     |
| 546 | Spencer Jones            | DEN    | Low Usage Floor Spacers             | Underperformer   | As Expected     |
| 547 | Xavier Tillman Sr.       | BOS    | Low Usage Floor Spacers             | Underperformer   | As Expected     |
| 548 | Luke Travers             | CLE    | Low Usage Floor Spacers             | Underperformer   | As Expected     |
| 549 | Justin Minaya            | POR    | Low Usage Floor Spacers             | As Expected      | As Expected     |
| 550 | D.J. Carton              | TOR    | Low Usage Floor Spacers             | Underperformer   | As Expected     |