# Imports
import pandas as pd
import numpy as np
import shap
from functions import *
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, silhouette_score
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_predict
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Helper Functions
# pull the data
def pull_data():
    tables = pd.read_html('https://www.basketball-reference.com/leagues/NBA_2025_per_game.html#per_game_stats')
    df_raw = tables[0]
    # making a dictionary of the teams win proportions
    dict_win = {'OKC': [0.829],
                'MIL': [0.585],
                'DEN': [0.610],
                'DAL': [0.476],
                'LAL': [0.610],
                'MIN': [0.598],
                'BOS': [0.744],
                'PHO': [0.439],
                'PHI': [0.293],
                'DET': [0.537],
                'NYK': [0.622],
                'ORL': [0.500],
                'CHO': [0.232],
                'NOP': [0.256],
                'GSW': [0.585],
                'SAS': [0.415],
                'ATL': [0.488],
                'CLE': [0.780],
                'BRK': [0.317],
                'MIA': [0.451],
                'SAC': [0.488],
                'CHI': [0.476],
                'MEM': [0.585],
                'LAC': [0.610],
                'TOR': [0.366],
                'HOU': [0.634],
                'WAS': [0.220],
                'IND': [0.610],
                'POR': [0.439],
                'UTA': [0.207]
    }
    df_win = pd.DataFrame(dict_win) # turning it into a data frame
    df_win = df_win.melt(var_name='Team') # making it long format for the merge
    df_stats = pd.merge(left=df_raw, right=df_win, how='left', left_on='Team', right_on='Team')
    dict_rename = {'value': 'Team_Win'} # renames the 'value' column to 'Team_Win'
    df_stats = df_stats.rename(dict_rename, axis=1)
    # drop the rows that don't have a team win
    df_stats = df_stats.dropna(subset=['Team_Win'])
    df_stats.reset_index(inplace=True) # resets the index after dropping
    tables = pd.read_html('https://www.basketball-reference.com/leagues/NBA_2025_advanced.html')
    df_advanced = tables[0]
    cols_drop = ['Age', 'Pos', 'G', 'GS', 'Awards']
    
    df_advanced = df_advanced.drop(cols_drop, axis=1)
    df_statsadvanced = pd.merge(left=df_stats, right=df_advanced, how='left', left_on=['Player', 'Team'], right_on=['Player', 'Team'])
    return df_statsadvanced

# preprocess the data
def preprocess(df):
    # drop players with less than 5 minutes per game
    df = df[df['MP_x'] > 5]
    
    # trimming the columns that aren't numeric
    df_numeric = df.select_dtypes(include='number')
    df_numeric['Player'] = df['Player']
    df_numeric['Team'] = df['Team']
    
    # dropping the index, rank, unnamed column
    df_numeric = df_numeric.drop(['index', 'Rk_x', 'Rk_y', 'MP_y'], axis=1)

    # drop na
    df_cleaned = df_numeric.dropna()

    ### make per minutes rates
    dict_perminute = {'Player': df_cleaned['Player'],
                      'Team': df_cleaned['Team'],
                     '2PA_per_min': df_cleaned['2PA'] / df_cleaned['MP_x'],
                     '3PA_per_min': df_cleaned['3PA'] / df_cleaned['MP_x'],
                     'FTA_per_min': df_cleaned['FTA'] / df_cleaned['MP_x'],
                     'PTS_per_min': df_cleaned['PTS'] / df_cleaned['MP_x'],
                     'AST_per_min': df_cleaned['AST'] / df_cleaned['MP_x'],
                     'ORB_per_min': df_cleaned['ORB'] / df_cleaned['MP_x'],
                     'DRB_per_min': df_cleaned['DRB'] / df_cleaned['MP_x'],
                     'STL_per_min': df_cleaned['STL'] / df_cleaned['MP_x'],
                     'BLK_per_min': df_cleaned['BLK'] / df_cleaned['MP_x'],
                     'PF_per_min': df_cleaned['PF'] / df_cleaned['MP_x'],
                     '3PAr': df_cleaned['3PAr'],
                     'USG%': df_cleaned['USG%'],
                     'FTr': df_cleaned['FTr'],
                     'TOV%': df_cleaned['TOV%'],
                     'PER': df_cleaned['PER'],
                     'WS': df_cleaned['WS'],
                     }
    df_perminute = pd.DataFrame(dict_perminute)
    
    return df_perminute

# clustering
def add_clustering(df):
    feature_cols = [
        '2PA_per_min', '3PA_per_min', 'FTA_per_min', 'PTS_per_min',
        'AST_per_min', 'ORB_per_min', 'DRB_per_min', 'STL_per_min',
        'BLK_per_min', '3PAr', 'USG%', 'FTr'
    ]

    df_clustering = df[feature_cols]

    #get the colnames
    colnames = df_clustering.columns
    
    # init the scalar
    scalar = StandardScaler()
    # fit the scalar and transform
    df_scaled = pd.DataFrame(
        scalar.fit_transform(df_clustering),
        columns=colnames,
        index=df_clustering.index
    )
    
    X = df_scaled[feature_cols].copy()
    
    kmeans_9 = KMeans(n_clusters=9, random_state=42, n_init=10)
    df_scaled['cluster_9'] = kmeans_9.fit_predict(X)
    
    kmeans_3 = KMeans(n_clusters=3, random_state=42, n_init=10)
    df_scaled['cluster_3'] = kmeans_3.fit_predict(X)
    
    df['cluster_3'] = df_scaled['cluster_3']
    df['cluster_9'] = df_scaled['cluster_9']

    cluster_map = {
        0: 'High Volume Offensive Stars',
        1: 'Balanced Role Players',
        2: 'Rebounding Bigs',
    }
    df['cluster_3_label'] = df['cluster_3'].map(cluster_map)

    cluster_map = {
        0: 'Interior Scoring Stars',
        1: 'High Volume Three Point Specialists',
        2: 'Stretch Bigs',
        3: 'Primary Offensive Engines',
        4: 'Low Usage Floor Spacers',
        5: 'Balanced Role Players',
        6: 'Traditional Interior Bigs',
        7: 'Defensive Guards',
        8: 'Secondary Playmakers'
    }
    df['cluster_9_label'] = df['cluster_9'].map(cluster_map)

    return df

# clustering graphs
def make_clustering_graphs(df):
    feature_cols = [
        '2PA_per_min', '3PA_per_min', 'FTA_per_min', 'PTS_per_min',
        'AST_per_min', 'ORB_per_min', 'DRB_per_min', 'STL_per_min',
        'BLK_per_min', '3PAr', 'USG%', 'FTr'
    ]

    df_clustering = df[feature_cols]

    #get the colnames
    colnames = df_clustering.columns
    
    # init the scalar
    scalar = StandardScaler()
    # fit the scalar and transform
    df_scaled = pd.DataFrame(
        scalar.fit_transform(df_clustering),
        columns=colnames,
        index=df_clustering.index
    )
    
    pca = PCA(n_components=2)
    df_pca = pca.fit_transform(df_scaled)
    
    sns.scatterplot(
        x=df_pca[:, 0],
        y=df_pca[:, 1],
        hue=df['cluster_9_label']
    )
    
    plt.title("PCA of Player Archetypes (k=9)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend(
        title="Player Archetypes (k=9)",
        bbox_to_anchor=(1.05, 1),
        loc='upper left'
    )
    plt.show()

    pca = PCA(n_components=2)
    df_pca = pca.fit_transform(df_scaled)
    
    sns.scatterplot(
        x=df_pca[:, 0],
        y=df_pca[:, 1],
        hue=df['cluster_3_label']
    )
    
    plt.title("PCA of Player Archetypes (k=3)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend(
        title="Player Archetypes(k=3) ",
        bbox_to_anchor=(1.05, 1),
        loc='upper left'
    )
    plt.show()

    df_means = df[['PER', 'WS', 'cluster_9_label']].groupby(by='cluster_9_label').mean()
    
    sns.scatterplot(data=df_means, x='WS', y='PER', hue='cluster_9_label')
    
    plt.title("Win Shares vs PER")
    plt.xlabel("Win Shares")
    plt.ylabel("PER")
    plt.legend(
        title="Player Archetypes",
        bbox_to_anchor=(1.05, 1),
        loc='upper left'
    )
    
    plt.show()

# split and prepare data for machine learning models
def split_and_prep(df):
    # subset to the columns we will be using
    X = df[['2PA_per_min', 'FTA_per_min', 'USG%', 'PF_per_min', '3PA_per_min', 'TOV%', '3PAr', 'cluster_9']].copy()
    y = df[['PER', 'WS']].copy()
    
    # encode the cluster labels
    X = pd.get_dummies(X, columns=['cluster_9'], drop_first=False)
    
    # train test split
    X_train_original, X_test_original, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # scale the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_original)
    X_test = scaler.transform(X_test_original)

    return X_train_original, X_train, X_test_original, X_test, y_train, y_test

# linear regression
def linear_regression(X_train, y_train, X_test, y_test, df):
    # per
    lin_mod_per = LinearRegression()
    lin_mod_per.fit(X_train, y_train['PER'])
    
    # ws
    lin_mod_ws = LinearRegression()
    lin_mod_ws.fit(X_train, y_train['WS'])
    
    # predict
    y_train_pred_per = lin_mod_per.predict(X_train)
    y_test_pred_per = lin_mod_per.predict(X_test)
    
    y_train_pred_ws = lin_mod_ws.predict(X_train)
    y_test_pred_ws = lin_mod_ws.predict(X_test)
    
    # score
    lin_per_train_mse = mean_squared_error(y_train['PER'], y_train_pred_per)
    lin_per_test_mse = mean_squared_error(y_test['PER'], y_test_pred_per)
    
    lin_ws_train_mse = mean_squared_error(y_train['WS'], y_train_pred_ws)
    lin_ws_test_mse = mean_squared_error(y_test['WS'], y_test_pred_ws)
    
    # to RMSE
    lin_per_train_rmse = np.sqrt(lin_per_train_mse)
    lin_per_test_rmse = np.sqrt(lin_per_test_mse)
    
    lin_ws_train_rmse = np.sqrt(lin_ws_train_mse)
    lin_ws_test_rmse = np.sqrt(lin_ws_test_mse)
    
    print(f'Linear PER Train RMSE: {lin_per_train_rmse}, Linear PER Test RMSE: {lin_per_test_rmse}, Linear WS Train RMSE: {lin_ws_train_rmse}, Linear WS Test RMSE:{lin_ws_test_rmse}')

    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('model', LinearRegression())
    ])

    X = df[['2PA_per_min', 'FTA_per_min', 'USG%', 'PF_per_min', '3PA_per_min', 'TOV%', '3PAr', 'cluster_9']].copy()
    y = df[['PER', 'WS']].copy()
    
    y_lin_pred_per = cross_val_predict(
        pipe,
        X,
        y['PER'],
        cv=5
    )
    
    y_lin_pred_ws = cross_val_predict(
        pipe,
        X,
        y['WS'],
        cv=5
    )
    
    # residuals
    df['lin_resid_per'] = y['PER'] - y_lin_pred_per
    df['lin_resid_ws'] = y['WS'] - y_lin_pred_ws
    
    df[['lin_resid_per', 'lin_resid_ws']]

# random forest
def rf_regression(X_train, y_train, X_test, y_test, df):
    # per
    rf_mod_per = RandomForestRegressor(random_state=42, max_depth=7, min_samples_leaf=1, min_samples_split=5, n_estimators=200)
    rf_mod_per.fit(X_train, y_train['PER'])
    
    # ws
    rf_mod_ws = RandomForestRegressor(random_state=42, max_depth=5, min_samples_leaf=5, min_samples_split=20, n_estimators=100)
    rf_mod_ws.fit(X_train, y_train['WS'])
    
    # predict
    y_train_pred_per = rf_mod_per.predict(X_train)
    y_test_pred_per = rf_mod_per.predict(X_test)
    
    y_train_pred_ws = rf_mod_ws.predict(X_train)
    y_test_pred_ws = rf_mod_ws.predict(X_test)
    
    # score
    rf_per_train_mse = mean_squared_error(y_train['PER'], y_train_pred_per)
    rf_per_test_mse = mean_squared_error(y_test['PER'], y_test_pred_per)
    
    rf_ws_train_mse = mean_squared_error(y_train['WS'], y_train_pred_ws)
    rf_ws_test_mse = mean_squared_error(y_test['WS'], y_test_pred_ws)
    
    # to RMSE
    rf_per_train_rmse = np.sqrt(rf_per_train_mse)
    rf_per_test_rmse = np.sqrt(rf_per_test_mse)
    
    rf_ws_train_rmse = np.sqrt(rf_ws_train_mse)
    rf_ws_test_rmse = np.sqrt(rf_ws_test_mse)
    
    print(f'RF PER Train RMSE: {rf_per_train_rmse}, RF PER Test RMSE: {rf_per_test_rmse}, RF WS Train RMSE: {rf_ws_train_rmse}, RF WS Test RMSE:{rf_ws_test_rmse}')

    X = df[['2PA_per_min', 'FTA_per_min', 'USG%', 'PF_per_min', '3PA_per_min', 'TOV%', '3PAr', 'cluster_9']].copy()
    y = df[['PER', 'WS']].copy()
    
    rf_pipe_per = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestRegressor(random_state=42, max_depth=7, min_samples_leaf=1, min_samples_split=5, n_estimators=200))
    ])
    
    rf_pipe_ws = Pipeline([
        ('scaler', StandardScaler()),
        ('model', RandomForestRegressor(random_state=42, max_depth=5, min_samples_leaf=5, min_samples_split=20, n_estimators=100))
    ])
    
    y_rf_pred_per = cross_val_predict(
        rf_pipe_per,
        X,
        y['PER'],
        cv=5
    )
    
    y_rf_pred_ws = cross_val_predict(
        rf_pipe_ws,
        X,
        y['WS'],
        cv=5
    )
    
    # residuals
    df['rf_resid_per'] = y['PER'] - y_rf_pred_per
    df['rf_resid_ws'] = y['WS'] - y_rf_pred_ws
    
    df[['rf_resid_per', 'rf_resid_ws']]

# classify players
def find_performance(df):
    lin_per_test_rmse = 3.448331424684772
    rf_ws_test_rmse = 2.6084469399871995
    
    df['perf_label_per'] = np.where(
        df['lin_resid_per'] > lin_per_test_rmse, 'Overperformer',
        np.where(df['lin_resid_per'] < -lin_per_test_rmse, 'Underperformer', 'As Expected')
    )
    
    df['perf_label_ws'] = np.where(
        df['rf_resid_ws'] > rf_ws_test_rmse, 'Overperformer',
        np.where(df['rf_resid_ws'] < -rf_ws_test_rmse, 'Underperformer', 'As Expected')
    )
    
    df_performance = df[['Player', 'Team', 'cluster_9_label', 'perf_label_per', 'perf_label_ws']]

    return df_performance

# make the beeswarm plots
def make_beeswarms(X_train, y_train, X_test, y_test, X_test_original):
    # per
    rf_mod_per = RandomForestRegressor(random_state=42, max_depth=7, min_samples_leaf=1, min_samples_split=5, n_estimators=200)
    rf_mod_per.fit(X_train, y_train['PER'])
    
    # ws
    rf_mod_ws = RandomForestRegressor(random_state=42, max_depth=5, min_samples_leaf=5, min_samples_split=20, n_estimators=100)
    rf_mod_ws.fit(X_train, y_train['WS'])

    explainer = shap.TreeExplainer(rf_mod_per)
    shap_values = explainer(X_test_original)
    
    shap.plots.beeswarm(
        shap_values,
        max_display=20,
        show=False
    )
    
    plt.title('Shap Values on PER')
    plt.show()

    explainer = shap.TreeExplainer(rf_mod_ws)
    shap_values = explainer(X_test_original)
    
    shap.plots.beeswarm(
        shap_values,
        max_display=20,
        show=False
    )
    
    plt.title('Shap Values on WS')
    plt.show()