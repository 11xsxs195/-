from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CURRENT_DIR = Path(__file__).resolve().parent
sys.path.append(str(CURRENT_DIR))
sys.path.append(str(CURRENT_DIR.parents[1]))

from analysis_common import CITY_NAME, configure_matplotlib, load_analysis_data
from kmeans import KMeansClassifier


configure_matplotlib(plt)


def loadDataset():
    """
    加载数据集(DataFrame格式),并转换成所需要的格式。
    最后将返回为一个numpy的数组类型
    """
    df = load_analysis_data()

    latlng_path = CURRENT_DIR.parent / "artifacts" / "latlng.csv"
    if not latlng_path.exists() or latlng_path.stat().st_size == 0:
        raise RuntimeError(f"坐标文件不存在或为空: {latlng_path}")
    df_latlng = pd.read_csv(latlng_path)
    df["id"] = df["id"].astype(str)
    df_latlng["id"] = df_latlng["id"].astype(str)
    df_merge = pd.merge(df,df_latlng,on="id")

    #选取所需要的数据
    data_cluster = df_merge[["id","total","unitPriceValue","jzmj","lat","lng"]]
    
    #剔除带有空值的行    
    data_cluster = data_cluster.dropna()

    #去除离散值
    data_cluster = data_cluster.loc[data_cluster["jzmj"] < 500] 
    data_cluster = data_cluster.loc[data_cluster["total"] < 3000]

    if data_cluster.empty:
        raise RuntimeError("聚类输入数据为空，请检查 latlng.csv 是否成功生成有效坐标")

    #转换为numpy数组类型
    arr_cluster = np.array(data_cluster).astype(float)
    return arr_cluster


"""1、加载数据"""
data_X = loadDataset()


"""2、根据sse值，选取合适的k值"""
k_values = [2,3,4,5,6,7,8,9,10]
sse_values = []
for k in k_values:
    clf = KMeansClassifier(k)
    clf.fit(data_X)
    cents = clf._centroids
    labels = clf._labels
    sse = clf._sse
    sse_values.append(sse)

sse_data = {"k":k_values,"sse":sse_values}
sse_df = pd.DataFrame(sse_data)
#重新定义索引
sse_df.set_index(sse_df["k"],inplace=True)
del sse_df["k"]

#绘制不同k值下的和方差折线图
sse_df.index.name = ""
fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot(111)
ax.set_ylabel("SSE",fontsize=14)
ax.set_title(f"{CITY_NAME}不同k值下的SSE(Sum of squared errors)平方误差和",fontsize=18)
sse_df.plot(kind="line",fontsize=12,grid=True,marker="o",ax=ax)


"""3、选定k值后，聚类分析，统计结果"""
#给定划分数量k
k = 5

#运行k-means算法    
clf = KMeansClassifier(k)
clf.fit(data_X)
cents = clf._centroids
labels = clf._labels
sse = clf._sse

#设置存储值
data_result = [] #聚类的原始样本集（numpy数组类型）
result_mean = []#各类样本集均值结果集
data_df = []#聚类的原始样本集（dataframe类型）
colors = ['b','g','r','k','c','m','y','#e24fff','#524C90','#845868']

#统计均值结果
for i in range(k):
    index = np.nonzero(labels==i)[0]#取出所有属于第i个簇的索引值
    data_i = data_X[index]    #取出属于第i个簇的所有样本点
    data_result.append(data_i)
    mean_data = data_i.mean(axis=0)
    mean_data = list(map(int,mean_data))
    result_mean.append(list(mean_data))

#变换数组结构
for i in range(k):
    data_temp = data_result[i]
    data = {"id":data_temp[:,0],
            "total":data_temp[:,1],
            "unitprice":data_temp[:,2],
            "jzmj":data_temp[:,3],
            "lat":data_temp[:,4],
            "lng":data_temp[:,5]}
    data_df_temp = pd.DataFrame(data,columns=["id","total","unitprice","jzmj","lat","lng"])
    data_df.append(data_df_temp)
    
#输出统计结果
gr = 0
print("                     k-means算法统计结果")
print(" 分组	总价（万）	单价（元/平米）  建筑面积（平米）   总计")
for i in result_mean:
    print(" "+str(gr)+"         "+str(i[1])+" 		"+str(i[2])+"   	"+str(i[3])+"\t\t"+str(len(data_df[gr])))
    gr = gr + 1
    

"""4、聚类结果：单价与建筑面积的散点图"""   
fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot(111)
ax.set_title(f"{CITY_NAME}单价与建筑面积散点图",fontsize=18)
data_df[0].plot(x="jzmj", y="unitprice", kind="scatter",label="0",color=colors[0],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
data_df[1].plot(x="jzmj", y="unitprice", kind="scatter",label="1",color=colors[1],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
data_df[2].plot(x="jzmj", y="unitprice", kind="scatter",label="2",color=colors[2],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
data_df[3].plot(x="jzmj", y="unitprice", kind="scatter",label="3",color=colors[3],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
data_df[4].plot(x="jzmj", y="unitprice", kind="scatter",label="4",color=colors[4],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
ax.set_xlabel("建筑面积(㎡)",fontsize=14)
ax.set_ylabel("单价(元/㎡)",fontsize=14)

"""5、聚类结果：总价价与建筑面积的散点图"""
fig = plt.figure(figsize=(12,7))
ax = fig.add_subplot(111)
ax.set_title(f"{CITY_NAME}总价与建筑面积散点图",fontsize=18)
data_df[0].plot(x="jzmj", y="total", kind="scatter",label="0",color=colors[0],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
data_df[1].plot(x="jzmj", y="total", kind="scatter",label="1",color=colors[1],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
data_df[2].plot(x="jzmj", y="total", kind="scatter",label="2",color=colors[2],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
data_df[3].plot(x="jzmj", y="total", kind="scatter",label="3",color=colors[3],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
data_df[4].plot(x="jzmj", y="total", kind="scatter",label="4",color=colors[4],fontsize=12,ax=ax,alpha=0.4,xticks=[0,50,100,150,200,250,300,400,500],xlim=[0,600])
ax.set_xlabel("建筑面积(㎡)",fontsize=14)
ax.set_ylabel("总价(万元)",fontsize=14)


"""6、生成地图文件"""
count = 0
result_dir = CURRENT_DIR / "result" / "map"
result_dir.mkdir(parents=True, exist_ok=True)
for data_map in data_df:
    out_map = result_dir / f"cluster{count}.js"
    with open(out_map,"w") as file_out:
        for lng,lat,price in zip(list(data_map["lng"]),list(data_map["lat"]),list(data_map["total"])):
            #out = str(lng)+","+str(lat)
            out='{\"lng\":'+str(lng)+',\"lat\":'+str(lat)+',\"count\":'+str(price)+'},'
            file_out.write(out)
            file_out.write("\n")
    count = count + 1
  