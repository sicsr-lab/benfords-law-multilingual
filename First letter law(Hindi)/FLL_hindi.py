
import pandas as pd,numpy as np,matplotlib.pyplot as plt,seaborn as sn
import math,re,string

lst=[]
d={'अ': 0, 'आ': 0, 'इ': 0, 'ई': 0, 'उ': 0, 'ऊ': 0, 'ऋ': 0, 'ए': 0, 'ऐ': 0, 'ओ': 0, 'औ': 0, 'अं': 0, 'अः': 0, 'क': 0, 'ख': 0, 'ग': 0, 'घ': 0, 'ड़': 0, 'च': 0, 'छ': 0, 'ज': 0, 'झ': 0, 'ञ': 0, 'ट': 0, 'ठ': 0, 'ड': 0, 'ढ': 0, 'ण': 0, 'त': 0, 'थ': 0, 'द': 0, 'ध': 0, 'न': 0, 'प': 0, 'फ': 0, 'ब': 0, 'भ': 0, 'म': 0, 'य': 0, 'र': 0, 'ल': 0, 'व': 0, 'श': 0, 'ष': 0, 'स': 0, 'ह': 0, 'क्ष': 0, 'त्र': 0, 'ज्ञ': 0, 'श्र': 0, 'द्य': 0}
# length_of_each_letter=[(3, 'श्र'), (3, 'द्य'), (3, 'त्र'), (3, 'ज्ञ'), (3, 'क्ष'), (2, 'ड़'), (2, 'अः'), (2, 'अं'), (1, 'ह'), (1, 'स'), (1, 'ष'), (1, 'श'), (1, 'व'), (1, 'ल'), (1, 'र'), (1, 'य'), (1, 'म'), (1, 'भ'), (1, 'ब'), (1, 'फ'), (1, 'प'), (1, 'न'), (1, 'ध'), (1, 'द'), (1, 'थ'), (1, 'त'), (1, 'ण'), (1, 'ढ'), (1, 'ड'), (1, 'ठ'), (1, 'ट'), (1, 'ञ'), (1, 'झ'), (1, 'ज'), (1, 'छ'), (1, 'च'), (1, 'घ'), (1, 'ग'), (1, 'ख'), (1, 'क'), (1, 'औ'), (1, 'ओ'), (1, 'ऐ'), (1, 'ए'), (1, 'ऋ'), (1, 'ऊ'), (1, 'उ'), (1, 'ई'), (1, 'इ'), (1, 'आ'), (1, 'अ')]

#Reading and computing the frequency
with open("../bible_hindi", 'r') as f:
    content = f.read()

# Data cleaning
content = re.sub(r'\d+', '', content)  # removing digits from text

content = content.translate(str.maketrans('', '', string.punctuation))  # removing all punctuations
content = content.translate(str.maketrans('', '', string.ascii_letters))  # removing english letters
content = content.translate(str.maketrans('', '','ि'))  # Optional
#content = content.translate(str.maketrans('', '','्ःिंाँऀ'))  # Optional
#्ःिंाँऀ
#ँंःऀऻ़ािीुूृॄॅॆेैॉॊोौ्ॎॏ॒॑॓॔ॕॖ 	ॗ
#print(content)

for i in content.lower().strip().split():
            if(len(i)>=3 and i[:3] in d):
                 d[i[:3]]+=1
            elif(len(i)>=2 and i[:2] in d):
                 d[i[:2]]+=1
            else:
              if(i[0] in d):
                  d[i[0]]+=1
              else:
                  lst.append(i[0])         #just for checking

print(d)
# print(lst)   #To check/observe if any valid character is excluded

#Creating a dataframe to analyze the results.(Letters are sorted in descending order w.r.t to their frequency)
df=pd.DataFrame(d.items(),columns=['Letters','Count']).sort_values(by='Count',ascending=0).reset_index().drop(columns='index')
# df=df.sort_values(by='Count',ascending=0).reset_index()
#df=df.drop(columns='index')
x=len(df['Letters'])
df['Freq_percent']=df['Count']/sum(df['Count'])
# df['Predicted']=x-(x-1)*math.log(x-1,x)-(df.index+1)*math.log((df.index+1),x)+((df.index+1)-1)*math.log((df.index+1)-1,x)
b=0

#Predicting the prob of frequency based on first letter law
Predicted=[(1+x*math.log(x/(x-1),x))/(x*(x-1)*math.log(x/(x-1),x))]
# Predicted=[(x-((x-1)*math.log(x-1,x)))/(x*(x-1)*math.log(x/(x-1),x))]
Predicted+=[(x-(x-1)*math.log(x-1,x)-i*math.log(i,x)+((i-1))*math.log(i-1,x))/(x*(x-1)*math.log(x/(x-1),x))  for i in (df.index+1) if i!=1]
df['Predicted']=Predicted
print(df)


#Plotting results
plt.rc('font',family='Lohit Devanagari')
sn.scatterplot(x='Letters',y='Freq_percent',data=df,marker='o')
sn.scatterplot(x='Letters',y='Predicted',data=df,marker='X',color='r')
plt.legend(labels=['Observed','Predicted'])
plt.ylabel("Probability")

#Calculating MSE
from sklearn.metrics import mean_absolute_error,mean_squared_error
print("MAE : ",mean_absolute_error(df['Freq_percent'],df['Predicted']))
print("MSE : ",mean_squared_error(df['Freq_percent'],df['Predicted']))
print("RMSE : ",math.sqrt(mean_squared_error(df['Freq_percent'],df['Predicted'])))

print("Total number of words : ",sum(df['Count']))
plt.show()