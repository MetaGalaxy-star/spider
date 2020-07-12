import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import cm
import jieba
from wordcloud import WordCloud

fig,ax = plt.subplots(1,2,figsize = (13,6))
plt.rcParams['font.sans-serif']=['SimHei'] 
data = pd.read_csv('data1.csv')

#��ͼһ
data_1 = data.groupby('tname')['tname'].count().sort_values(ascending=False)
data_deteal = data_1[data_1.values>=10]
data_1[data_1.values < 10 ].sum()
# data_deteal.append(data_1[data_1.values < 10 ].sum())
data_deteal['����']=data_1[data_1.values < 10 ].sum()
data_deteal=data_deteal.sort_values(ascending=False)
sizes=data_deteal.values
colors = cm.rainbow(np.arange(len(sizes))/len(sizes)) # colormaps: Paired, autumn, rainbow, gray,spring,Darks
ax[0].pie(data_deteal,labels=data_deteal.index,autopct='%.0f%%',textprops = {'fontsize':15, 'color':'k'},pctdistance=0.7,colors=colors)
ax[0].set_title('�ۿ���Ƶ��ƫ������ͳ��ͼ',pad=15,fontsize=20)
plt.rcParams['font.sans-serif']=['SimHei'] 
data = pd.read_csv('data1.csv')

#��ͼ��
str=''
for title in data.title:
    str = str + title
wordcloud = WordCloud(font_path="F:\\python project\\tff\\simsun.ttf",background_color="white",width=1500, height=900).generate(str)#font_path�������ص�������·�������������
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
ax[1].set_title('��¼��������Ƶ�������ݵĴ���ͼ',fontsize=20,pad=20)

plt.subplots_adjust(hspace =0.2)
plt.show()