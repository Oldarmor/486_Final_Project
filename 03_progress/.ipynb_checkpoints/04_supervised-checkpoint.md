# Supervised Learning Results

## Problem Context

The goal of this analysis is to see how a players play style influences their effeciency and win shares across a season. The purpose of the supervised models was to take the clustering results from the unsupervised component and a select few other predictor variables to try to predict players Win Shares and Efficiency and compare predicted values to true values to find under and over performers.

## Supervised Models Implemented

There were two supervised models implemented and compared to predict Win Shares and PER, linear regression and a random forest regressor. To be clear, a linear regression model was fit to predict Win Shares and PER, and a random forest regressor model was fit to predict both Win Shares and PER. In order to compare the models a simple train and test split was done on the data, then RMSE was calculated on the test set to compare. The predictor variables passed into the models were always the same: 2PA per minute, FTA per minute, USG%, PF per minute, 3PA per minute, TOV%, 3PAr, and the cluster label created from the clustering analysis. It is important to note that each cluster label was given it's own indication as opposed to comparing cluster labels to a base line group, which does introduce some slight multicolinearity into the model, but we decided that it would be negligible. Also all of the predictor variables were scaled using a Standard Scaler.

The linear regression model didn't have any hyper parameter tuning needed. To tune the random forest regressor a 5 fold grid search cross validation was used to experiment with different numbers of estimators, max depth, minimum samples per split, and minimum samples per leaf. This was run for both the PER and WS model. After running the cross validation, the hyper parameters for the PER model are: max depth of 7, 1 minimum samples per leaf, 5 minimum samples per split, and 200 estimators. The hyper parameters for the WS model are: max depth of 5, 5 minimum samples per leaf, 20 minimum samples per split, and 100 estimators.

Finally, we wanted to predict a players PER and Win Shares using the models created, but it was imperative that the predictions came from a model that hasn't already seen and been trained on the player. So, while a train and test split was used to get some model metrics and used to compare the models, in order to get the predicted values a cross validation prediction function was used.

## Model Comparison and Selection

After fitting and comparing the models, it became clear that the Random Forest Regressor was really prone to overfitting the data. In fact, the initial 5 fold cross validation grid search needed to be adjusted to include more values for maximum depth, minimum samples per split, and minimum samples per leaf and run again because the initial parameters overfit the data far too much. The Grid Search also took a long time to run, about 7-8 minutes per model, making it hard to test many different combinations of hyperparameters. After the final hyper parameters were found though, the random forest actually didn't significantly out perform the linear regression model. In fact, the linear regression model performed slightly better than the random forest for predicting PER and the linear models PER prediction is what we used to decide if a player is an under or over performer. Below are the RMSE scores for both the linear regression model and the random forest regression model:

Linear Regression:

PER Train RMSE: 2.720265258497129, PER Test RMSE: 3.448246487553878, WS Train RMSE: 2.040884277285756, WS Test RMSE:2.629175443839345

Random Forest Regression:

PER Train RMSE: 1.873763155736009, PER Test RMSE: 3.4797077688014078, WS Train RMSE: 1.7877162450070447, WS Test RMSE:2.6083879757447757

## Explainability

To really understand the effect of a players play style we looked at the shap values from the random forest regressor. Below are the beeswarm plots for both the PER and the Win Shares model:

![Beeswarm PER](plots/shap_beeswarm_per.png)

![Beeswarm WS](plots/shap_beeswarm_ws.png)

Interestingly on the Win Shares beeswarm plot you can see that the cluster labels designed to motch player archetypes had very little to no impact at all on the predicted value. The most impactful label being the cluster label 3, which corresponds to primary offensive engines. For efficiency though it's a slightly different story. Looking at the PER bee swarm plot you can see that being labeled in the 4th or 5th cluster (low usage floor spacers and balanced role players) actively would bring down a players predicted PER.