# Project Proposal
## The Use of AI
### Prompt and AI Information
The generative AI model used to help with project ideas is the most recent version of ChatGPT (as of 03/21/2026). Below is the exact initial prompt message sent to ChatGPT:

"Hey Chat! I am working on a senior level machine learning class project. It must involve both one supervised learning technique (like regression or classification) and one other Machine Learning technique such as clustering, anomaly detection, recommender systems, or reinforcement learning. For my data set I'm using NBA basketball player stats from the 2024-2025 season. Can you suggest different project ideas that would allow me to apply both types of techniques?"

I will not include the entire response from ChatGPT, as it is quite lengthy, but the whole exchange can be seen [here](https://chatgpt.com/share/69bf7c5b-62a4-8013-bc4c-c7e1e1b8a097). Needless to say, ChatGPT responded with many different project ideas that could be used.

### Proposed Ideas
Here are three different ideas that ChatGPT came up with:
1. Predict player success + Detect Outliers
    - Use a regression model to predict salary, points per game, or efficiency
    - Then use anomaly detection to try and find players who significantly underperform or over perform
2. All-Star Prediction + Clustering Validation
    - use a classifier to predict all-star selection
    - then cluster players to see if all-stars cluster together, or if there's a group that is overlooked
3. Player Similarity Engine
    - Build a recommender system that predicts players most similar to someone
    - then try to predict player performance based off of their neighbors
All of which were really cool ideas actually, but a different direction was chosen. Regardless, the insight given from ChatGPT encouraged us to look into adding a players advanced stats into their data and we could use their advanced stats as targets, or predictors, as opposed to just using a players per game box score stats. Additionally, it really opened our eyes of exactly how far and how useful generative AI can be in helping to propose good ideas.
## Proposal
The project we decided on was actually an idea initially proposed by ChatGPT, but refined. We will be using a players offensive and defensive per game box score stats to cluster players into groups. From there we will classify each group into player archetypes (shot creators, play makers, defenders, etc.) and try to see how different player archetypes contribute to things like winshares, PER (player efficiency rating), and team win percentage. The supervised component will train a model to predict a specific players winshares, PER, and team win percentage. Additionally we could also use the residuals to try and find underrated and overrated players in todays NBA. The question this analysis and project will try to answer is: which play style (or player archetype) is most efficient and leads to the most wins? 
