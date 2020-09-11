#Testing Zipfs law on english text.
#We only care about the number of unique words in a script and not the total number of words in a text.

import pandas as pd,numpy as np,matplotlib.pyplot as plt,seaborn as sn
import math,re,string

d={}
#Reading text data
with open("../mahabharat", 'r') as f:
    content = f.read()

#Data cleaning
content = re.sub(r'\d+', '', content)     #removing digits from text
content = content.translate(str.maketrans('', '', string.punctuation))     #removing all punctuations

#Calculating frequency of each word
for i in content.lower().strip().split():
    if(i.isalpha()):
       if(i in d):
           d[i]+=1
       else:
           d[i]=1

print(d)


#Creating a dataframe to analyze the results.(Words are sorted in descending order w.r.t to their frequency)
df=pd.DataFrame(d.items(),columns=['Words','Count']).sort_values(by='Count',ascending=0).reset_index().drop(columns='index')

df['Freq_percent']=df['Count']/sum(df['Count'])   #Calculating relative frequency



#Predicting the frequency based on Zipfs law
s=[1/i for i in range(1,len(df['Words'])+1)]
# print(s)
c=1/sum(s)
# print(c)
Predicted=[c/(i) for i in df.index+1]    #Getting the predicted values of frequency w.r.t to their index.
# print(len(Predicted))
# print(c,Predicted)
df['Predicted']=Predicted

print("Displaying 20 most frequent words : ")
print(df.iloc[:20])

#Plotting results
sn.scatterplot(x='Words',y='Freq_percent',data=df.iloc[:20],marker='o')
sn.scatterplot(x='Words',y='Predicted',data=df.iloc[:20],marker='X',color='r')
plt.legend(labels=['Observed','Predicted'])
plt.ylabel("Frequency")
# plt.show()

#Plotting log(rank) vs log(Observed freq)
plt.figure(2)
index=[math.log(i) for i in df.index+1]
Observed_freq=[math.log(i) for i in df['Freq_percent']]
Predicted_freq=[math.log(i) for i in df['Predicted']]
sn.lineplot(x=index,y=Observed_freq)
sn.lineplot(x=index,y=Predicted_freq)
plt.legend(labels=['Observed',"Predicted"])
plt.xlabel('log(rank)');plt.ylabel('log(Frequency)')


#Calculating MSE/MAE
from sklearn.metrics import mean_absolute_error,mean_squared_error
print("MAE : ",mean_absolute_error(df['Freq_percent'],df['Predicted']))
print("MSE : ",mean_squared_error(df['Freq_percent'],df['Predicted']))



print("Number of words(unique) in text : ",len(df['Words']))
print("Total number of words in text : ",sum(df['Count']))
plt.show()