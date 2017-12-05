# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 10:12:01 2017

@author: mdarq
"""

import math

import itertools

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class Player:
    """ A voir plus tard """
    def __init__(self, name="", attaque=0):
        self.name = name
        self.attaque = attaque
        
    def create_player(self, name, attaque):
        """ Create new player """
        self.name = name
        self.attaque = attaque
        return self
    
    
Joueurs = pd.DataFrame()
Joueurs["Name"] = "Denis", "Romain", "Mouhsin", "Paul", "Coco", "Theo","Fabien"\
, "Ben", "Erwan", "PierreHub", "Laurent", "Moustapha", "Hector"
Joueurs["Attaque"] =    55, 42, 69, 70, 40, 48, 50, 52, 65, 60, 40, 69, 65
Joueurs["Defense"] =    65, 73, 64, 62, 60, 62, 60, 62, 68, 58, 72, 64, 60
Joueurs["Technique"] =  45, 20, 90, 80, 20, 38, 30, 40, 40, 50, 20, 90, 75
Joueurs["Rapidite"] =   58, 56, 55, 88, 50, 60, 50, 53, 70, 85, 59, 55, 55
Joueurs["Lecture jeu"]= 65, 69, 88, 75, 45, 59, 60, 61, 69, 60, 65, 88, 60
Joueurs["Endurance"] =  62, 65, 60, 70, 60, 65, 65, 61, 65, 75, 65, 60, 65
Joueurs["Total"] = Joueurs.sum(axis=1)    
Equipes = pd.DataFrame(columns = ["Team_A_Score", "Team_B_Score", 
                                  "Raw_score_difference"])


#Select 10 players among the available names
selection = ["Romain", "Denis", "Ben", "Fabien", "Erwan", "Mouhsin", 
             "PierreHub", "Laurent", "Moustapha", "Hector"]

selection_idx = Joueurs.loc[Joueurs["Name"].isin(selection)].index.values
Joueurs_selection = Joueurs.iloc[selection_idx]

#%%Create random teams
#List of possible combinations (2x5 out of 10)
idx_combined = itertools.combinations(np.arange(0,10,1),5)
#Create a list from the generator
teams_list = list(idx_combined)
#All players indexes
All = set(range(len(Joueurs_selection)))
A = np.array([])
#for t in teams_list/2:
for t in teams_list[:int(len(teams_list)/2)]:
    _ = set(t)
    team_A = set(t)
    team_B = All^team_A
    
    sum_A = Joueurs_selection["Total"].iloc[list(team_A)].sum()
    sum_B = Joueurs_selection["Total"].iloc[list(team_B)].sum()
#    print(team_A, A, team_B)
    Equipes = Equipes.append({"Team_A_Score":sum_A, "Team_B_Score":sum_B,
                              "Raw_score_difference":abs(sum_B-sum_A)},
                                ignore_index=True)
    A = np.append(A,abs(sum_B-sum_A))

idx_min = np.argmin(A)

team_A = set(teams_list[idx_min])
team_B = team_A^All

team_A_names = np.array(Joueurs_selection["Name"].iloc[list(team_A)])
team_B_names = np.array(Joueurs_selection["Name"].iloc[list(team_B)])

print("L'opposition la plus équilibrée est:\n Equipe A : {0}\n Equipe B:{1}"
      .format(team_A_names, team_B_names))

print(Joueurs_selection.iloc[list(team_A)])
print(Joueurs_selection.iloc[list(team_B)])

#%%
   
Equipes["Raw_score_difference"].sort_values(ascending=False)

 
#%% PLOT SKILLS ON A RADAR CHART

#Player to plot
name = "Romain"
idx = Joueurs.index[Joueurs["Name"]==name]

categories = list(Joueurs)[1:-1]
n = 6 #Number of skills
#Repeat first value to close the circular graph
values = Joueurs.loc[idx[0]].drop('Name').drop('Total').values.flatten().tolist()
values += values[:1]

#Angle of each axis
angles = [n_ / float(n) * 2 * math.pi for n_ in range(n)]
angles += angles[:1]

#initialise spider plot
ax = plt.subplot(111, polar=True)

#Draw one axis per variable and add labels
plt.xticks(angles[:-1], categories, color='grey', size=10)

#Draw ylabels
#Set ylabels on horizontal axis
ax.set_rlabel_position(0)
plt.yticks([25, 50, 75], ["25", "50", "75"], color="grey" ,size=7)
plt.ylim(0,100)

#Plot data
ax.plot(angles, values, linewidth=1, linestyle='solid')

#Fille area
ax.fill(angles, values, 'r', alpha=.4)
plt.title(Joueurs["Name"].loc[idx[0]])