# Predicting League of Legends Player Division Based on Their In-game Performance

## Goal
To predict a player's division based on their game performance statistics using League of Legends dataset

## Introduction

### What is League of Legends?
League of Legends is currently one of the most played PC game in the world with a monthly active user of 81 million. 
It is a team-based video game consisting of a two 5 player teams where both team must defend their base while simultaneously trying to destroy the enemy team’s base. While in game, each player accumulates statistics based on their in-game performance. Furthermore, players have their own individual rank/division where they are placed on based on how well they perform in game and the amount of time they won.

### Player Rank Prediction 
For this project, I want to predict a player division based on their in-game performance. As a player myself I always wonder if there is a substantial difference between the statistics of a high division player vs a low division player. There is a total of seven divisions in League of Legends, but I would only be focusing on five of them since Master and Challenger make up only .07% of player division. Listed below are the division I would be using starting from low division rank to higher division.

1. Bronze
2. Silver
3. Gold
4. Platinum
5. Diamond

## Data Collection and Methods

### Data Collection 
Riot Games the creator of League of Legends providesdevelopersaccess to their own API where developers can access players match history including their statistics. I created my own python script that took 1000 players for each division that I am trying to classify and tooktheir last 20 rank match history and averagestheir stats. I would have liked to use more match history and more players for each division, but League API have rate limit that prevent me from constantly calling their API.As a result, I have a size of 5000 dataset.

### Feature Selection
Each player statistics contains 22 features.For this project, I took the key features that differentiate players. For instance, there are some features that does not contain any variation among the different divisions and adding this to our feature list would only create too much noise and decrease the accuracy. Thus, I selected 10 out of 22 features which I’ve listed below.

- Kills 
- Deaths
- Assists 
- longestTimeSpentLiving 
- TotalDamageDealtToChampions
- visionScore
- gold/min
- cs/min
- wins/lose
- division

![Image of Figure 1](https://github.com/Abanting00/Player-Rank-Prediction-ML/blob/master/Figures/figure1.PNG)

Figure1 visualize show kills vs other features are related. We can see that Bronze (Blue), Silver (Yellow) and Diamond (purple) players, are very visible suggesting there are more separation across these three divisions. While Platinum and Gold players are less visible because it is not linearly separable from the other 3 divisions.

## Result

### Model Selection 
My approach for this project was to try out different models and see which one performs best.Since I would be doing multiclassification I also added some muticlassifier models to see how well they perform. The different result I obtain from each model is listed below. 

![Image of Figure 1](https://github.com/Abanting00/Player-Rank-Prediction-ML/blob/master/Figures/figure2.PNG)

![Image of Figure 1](https://github.com/Abanting00/Player-Rank-Prediction-ML/blob/master/Figures/Figure3.PNG)

![Image of Figure 1](https://github.com/Abanting00/Player-Rank-Prediction-ML/blob/master/Figures/figure4.PNG)


## Conclusion

### Best Models
Figure 2 shows that SVM, Regression, and K-neighbor perform well with accuracy ranging from 64-66%.I was impressed by these results since I was expecting a much lower accuracy. For SVM, I used three different kernels, linear, rbf, and sigmoid. Out of all the three kernels,RBF performed the best and sigmoid performed the worst. As for the Tree Classifiers, I was surprised that they did not perform as well as the SVM machines.Figure 2 and 3 shows that as we increase the tree depth stays constant and does not approach 0.Additionally, I tried to also use Neutral Network but I was having trouble finding the correct hyper parameters. I’ve gotten a result of 40% which is the worst one out of all the models that I’ve used. When I first started with this project, I’ve only taken 1 match history from each player.The maximum prediction score that I was able to obtain was only 30%. I tried to fix this by increasing the numberof matches from individual players to 10 matches. I have noticed that it increased from 30% to 50%. Thus, I thought that increasing the matches Itake from the players also increases the accuracy score. Which is why for this project I used 20 matches history from each player. I would have wanted to take more matches,but the rate limit of the Riot API prevents me to make a lot of request to their server and taking the dataset with 20 matches history took about 4 hours. Additionally, If I want to continue down this path of increasing the matches, the most I can obtain is 100 matches because Riot API only stores 100 match histories of a player.

## Future Extensions
In the future, Iwant to increase the match history and see if I can achieve a maximum of 80-90% accuracy score. Additionally, insteadof classifying every player in a division I would be classifying them based on the role they play. For instance, in basketball, each player has a certain role. A player can be a point guard and another player be shooting guard. Similarly, in league of legends, there are a total of five distinct roles. Each role has different statistics. In the future, I want to separate the classification of division based on what role each player plays.I also want to continue working on Neural Network and hope that I can use it better.





