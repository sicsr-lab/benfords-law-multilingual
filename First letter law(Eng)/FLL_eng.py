import pandas as pd,numpy as np,matplotlib.pyplot as plt,seaborn as sn
import math,re,string

d={'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0}

#Reading text data
with open("../mahabharat", 'r') as f:
    content = f.read()


#Data cleaning
content = re.sub(r'\d+', '', content)     #removing digits from text
content = content.translate(str.maketrans('', '', string.punctuation))     #removing all punctuations

#Calculating frequency
for i in content.lower().strip().split():
    if(i.isalpha()):
        if(i[0] in d):
            d[i[0]]+=1


print(d)


#Creating a dataframe to analyze the results.(Letters are sorted in descending order w.r.t to their frequency)
df=pd.DataFrame(d.items(),columns=['Letters','Count']).sort_values(by='Count',ascending=0).reset_index().drop(columns='index')
# df=df.sort_values(by='Count',ascending=0).reset_index()
#df=df.drop(columns='index')
x=len(df['Letters'])
df['Freq_percent']=df['Count']/sum(df['Count'])
# df['Predicted']=x-(x-1)*math.log(x-1,x)-(df.index+1)*math.log((df.index+1),x)+((df.index+1)-1)*math.log((df.index+1)-1,x)



#Predicting the prob of frequency based on first letter law
Predicted=[(1+x*math.log(x/(x-1),x))/(x*(x-1)*math.log(x/(x-1),x))]
# Predicted=[(x-((x-1)*math.log(x-1,x)))/(x*(x-1)*math.log(x/(x-1),x))]
Predicted+=[(x-(x-1)*math.log(x-1,x)-i*math.log(i,x)+((i-1))*math.log(i-1,x))/(x*(x-1)*math.log(x/(x-1),x))  for i in (df.index+1) if i!=1]
df['Predicted']=Predicted
print(df)


#Plotting results
sn.scatterplot(x='Letters',y='Freq_percent',data=df,marker='o')
sn.scatterplot(x='Letters',y='Predicted',data=df,marker='X',color='r')
plt.legend(labels=['Observed','Predicted'])
plt.ylabel("Frequency")


#Calculating MSE
from sklearn.metrics import mean_absolute_error,mean_squared_error
print("MAE : ",mean_absolute_error(df['Freq_percent'],df['Predicted']))
print("MSE : ",mean_squared_error(df['Freq_percent'],df['Predicted']))
# print("RMSE : ",math.sqrt(mean_squared_error(df['Freq_percent'],df['Predicted'])))


# #Performing chi2 test for goodness of fit
# import scipy.stats
# np.seterr(divide='ignore', invalid='ignore')
#
# # observed=np.array(df['Count'])
# # observed[len(observed)-1]=1
# # predicted=np.array(df['Predicted']*sum(df['Count']))
# # predicted[len(predicted)-1]=1
#
# observed=np.array(df['Freq_percent']*100)
# predicted=np.array(df['Predicted']*100)
#
# print(observed,predicted)
#
# # s,p=scipy.stats.chisquare(f_obs=observed[:len(observed)-1],f_exp=predicted[:len(observed)-1])
# s,p=scipy.stats.chisquare(f_obs=observed[:len(observed)-1],f_exp=predicted[:len(observed)-1])
#
# print(s,p)
# if(p>0.05):
#     print("Follows First letter law")
# else:
#     print("Doesn't follow First letter law")
#





print("Total number of words : ",sum(df['Count']))
plt.show()


