# Unsupervised Learning Analysis

## Unsupervised Model

Since the clustering analysis is an integral part of the supervised learning component, the unsupervised clustering was done first. The main goal of this analysis was to identify distinct player archetypes and on-court play styles. To accomplish this, we used a k-means clustering model to group players based on their statistical profiles.

## Unsupervised Process

To ensure clustering reflected player play style rather than performance, the data was subset to a set of carefully selected statistics. The goal was not to cluster based on efficiency, but instead on attributes such as shot selection, defensive activity, rebounding, and offensive role. The features used included two-point attempts, three-point attempts, free throw attempts, points, assists, offensive rebounds, defensive rebounds, steals, blocks, three-point attempt rate, usage rate, and free throw rate.

All counting statistics were converted to per-minute values by dividing by minutes played per game. This ensured that players were compared based on their behavior on the court rather than total opportunity. Additionally, players with fewer than five minutes per game were excluded to reduce noise from low-sample observations.

To determine the number of clusters, both an elbow plot and silhouette score plot were examined (see them below). The elbow plot did not show a clear inflection point, suggesting that multiple values of k could be reasonable. The silhouette score peaked at k = 3, with a secondary increase around k = 9. As a result, clustering was evaluated at both k = 3 and k = 9 to balance clustering quality and interpretability.
![Elbow Plot](plots/KMeans_elbow.png)
![Silhouette Scores](plots/KMeans_Silhouette.png)

## Results

The k = 3 clustering produced broad groupings: High Usage Offensive Players, Balanced Role Players, and Rebounding Bigs. While these clusters captured general player roles, they lacked specificity in describing distinct play styles.

In contrast, the k = 9 clustering produced more granular and interpretable archetypes. These included Interior Scoring Stars, Primary Offensive Engines, Secondary Scoring Options, High Volume Three Point Specialists, Low Usage Floor Spacers, Stretch Bigs, Traditional Interior Bigs, Defensive Guards, and Secondary Playmakers. These clusters better capture stylistic differences in scoring, shot selection, defensive activity, and playmaking.

## Conclusion

Overall, the unsupervised analysis demonstrates that NBA players can be effectively grouped into meaningful stylistic archetypes using statistical profiles. The k = 9 clustering provides the most useful representation of player roles and will be used in the supervised learning stage to evaluate player effectiveness within similar play styles.

## Plots and Tables

Below are the PCA Plots of the players after the clustering:
![PCA 3](plots/PCA_k=3.png)
![PCA 9](plots/PCA_k=9.png)

Below are the tables of the mean stats for each of the clusters. While showing the means of the opposite cluster is in each group, it is important to note that the opposite clusters labels were not passed into the cluster training:

Cluster 3 Means

|   cluster_3 |   2PA_per_min |   3PA_per_min |   FTA_per_min |   PTS_per_min |   AST_per_min |   ORB_per_min |   DRB_per_min |   STL_per_min |   BLK_per_min |     3PAr |    USG% |      FTr |   cluster_9 |
|------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|---------:|--------:|---------:|------------:|
|           0 |      0.292193 |     0.182564  |     0.140975  |      0.614543 |     0.148305  |     0.0360494 |      0.134506 |     0.0360557 |     0.0163681 | 0.384244 | 26.1458 | 0.299733 |     3.22137 |
|           1 |      0.146031 |     0.170345  |     0.0554415 |      0.370667 |     0.0935034 |     0.038047  |      0.112023 |     0.0363738 |     0.0157453 | 0.539744 | 16.508  | 0.178205 |     4.17949 |
|           2 |      0.231349 |     0.0626256 |     0.0898723 |      0.386073 |     0.0745063 |     0.0964797 |      0.195688 |     0.0318947 |     0.0395719 | 0.200287 | 16.2759 | 0.317463 |     5       |

Cluster 9 Means

|   cluster_9 |   2PA_per_min |   3PA_per_min |   FTA_per_min |   PTS_per_min |   AST_per_min |   ORB_per_min |   DRB_per_min |   STL_per_min |   BLK_per_min |     3PAr |    USG% |      FTr |   cluster_3 |
|------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|--------------:|---------:|--------:|---------:|------------:|
|           0 |      0.377979 |     0.0989073 |     0.182707  |      0.658725 |     0.127938  |     0.0804081 |     0.207429  |     0.0338243 |     0.0299327 | 0.206407 | 26.9185 | 0.383444 |    0.518519 |
|           1 |      0.120581 |     0.232788  |     0.0465033 |      0.422392 |     0.0834449 |     0.0260884 |     0.10146   |     0.0286183 |     0.0109377 | 0.662512 | 17.6631 | 0.13206  |    1        |
|           2 |      0.200932 |     0.198667  |     0.0854652 |      0.486833 |     0.0685242 |     0.0689698 |     0.193376  |     0.0281275 |     0.0505004 | 0.500733 | 20.6067 | 0.217933 |    1.26667  |
|           3 |      0.282341 |     0.207708  |     0.136311  |      0.631281 |     0.14866   |     0.0267899 |     0.118913  |     0.0335971 |     0.0119383 | 0.422729 | 26.8153 | 0.280847 |    0        |
|           4 |      0.107153 |     0.143809  |     0.0375885 |      0.278406 |     0.0682967 |     0.0519081 |     0.120508  |     0.0379184 |     0.0186046 | 0.578222 | 13.1111 | 0.151383 |    1.01235  |
|           5 |      0.193316 |     0.125025  |     0.086305  |      0.396313 |     0.0804143 |     0.0471048 |     0.129884  |     0.0330486 |     0.0172024 | 0.387989 | 17.1793 | 0.276805 |    1.1954   |
|           6 |      0.236354 |     0.028276  |     0.083444  |      0.364301 |     0.0704566 |     0.10927   |     0.206492  |     0.0269562 |     0.0439852 | 0.104583 | 14.86   | 0.3278   |    2        |
|           7 |      0.175122 |     0.130883  |     0.0811893 |      0.349849 |     0.0994434 |     0.0589872 |     0.120722  |     0.0736176 |     0.0192223 | 0.429107 | 16.8429 | 0.277571 |    1.14286  |
|           8 |      0.201174 |     0.146379  |     0.0673739 |      0.400503 |     0.173223  |     0.0259958 |     0.0991714 |     0.0416594 |     0.0129404 | 0.424754 | 18.9217 | 0.195812 |    0.782609 |