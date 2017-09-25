import pandas as pd
from sklearn.cluster import KMeans,DBSCAN
from bokeh import models
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.palettes import d3

data=pd.read_csv('d:/Wholesale customers data.csv')
data_columns=list(data.columns)
xaxisselect = models.Select(title="X axis:", value="Fresh", options=data_columns)
yaxisselect = models.Select(title="Y axis:", value="Milk", options=data_columns)
clusteringselect=models.Select(title="Clustering method",value="KMeans++",options=["KMeans++","DBSCAN"])
numclusterselect=models.Select(title="Number of clusters (KMeans++)",value='2',options=[str(x) for x in range(2,11)])
epstext = models.TextInput(value="2000", title="eps (DBSCAN)")
minsamplestext = models.TextInput(value="50", title="min_samples (DBSCAN)")
color=d3['Category20'][10]

def updateplot(attr,old,new):
	datatoplot=data[[xaxisselect.value,yaxisselect.value]]
	title=""
	pointcolor=[]
	if clusteringselect.value=="KMeans++":
		title="KMeans++ Clustering"+" "+numclusterselect.value+" clusters"
		kmeans=KMeans(n_clusters=int(numclusterselect.value),init='k-means++')
		kmeans.fit(datatoplot)
		pointcolor=[color[i] for i in kmeans.labels_]
	else:
		#dbscan
		title="DBSCAN Clustering (eps="+epstext.value+",min_samples="+minsamplestext.value+")"
		db = DBSCAN(eps=float(epstext.value),min_samples=float(minsamplestext.value))
		db.fit(datatoplot)
		pointcolor=[color[i] for i in db.labels_]
	newplot=figure(width=400,height=400)
	newplot.title.text=title
	newplot.title.align='center'
	newplot.xaxis.axis_label=xaxisselect.value
	newplot.yaxis.axis_label=yaxisselect.value
	source=models.ColumnDataSource(data=dict(xaxis=data[xaxisselect.value],yaxis=data[yaxisselect.value]))
	newplot.circle(source=source,x='xaxis',y='yaxis',color=pointcolor,size=5)
	newplot.add_tools(models.HoverTool(tooltips=[(xaxisselect.value,"@xaxis"),(yaxisselect.value,"@yaxis")]))
	layout.children.remove(layout.children[-1])
	layout.children.append(newplot)

xaxisselect.on_change('value',updateplot)
yaxisselect.on_change('value',updateplot)
clusteringselect.on_change('value',updateplot)
numclusterselect.on_change('value',updateplot)
epstext.on_change('value',updateplot)
minsamplestext.on_change('value',updateplot)


plot=figure(width=400,height=400)
plot.title.text="KMeans++ Clustering (1 cluster)"
plot.title.align='center'
plot.xaxis.axis_label="Fresh"
plot.yaxis.axis_label="Milk"

source=models.ColumnDataSource(data=dict(xaxis=data["Fresh"],yaxis=data["Milk"]))
plot.circle(source=source,x='xaxis',y='yaxis',color='red',size=5)
plot.add_tools(models.HoverTool(tooltips=[(xaxisselect.value,"@xaxis"),(yaxisselect.value,"@yaxis")]))

div1=models.Div(text="<h1>Homework 3</h1>",width=800)
div2=models.Div(text=r"""
<b>Discussion:</b>
Two clustring techniques are demonstrated in this project: KMeans++ and DBSCAN</br><br>
<p><b>KMeans++</b> has only one parameter, the number of clusters. This parameter is visually very straight forward for users of the visualization as the user can
immediately link this parameter to different colors illustrated in the visualization. When the user identify potential clusters, this parameter can be easily
adjusted to verify the user's idea on the visualization.
According to scikit-learn's documentation, the KMeans/KMeans++ method is a general purpose clustering technique and works best with even cluster size and flat geometry.
In this project users can select two dimensions from the dataset as x and y axis so it satisfies the use case of KMeans++ well but after trying different combinations
there seems to be not having very obvious clusters.
</p>
</p>The basic idea of <b>DBSCAN</b> is to seperate the dense areas from areas which are lense dense and it has two parameters:"eps" which is the maximun distance
allowed in the "dense" area and "min_samples" which is the minium number of samples for the area to be considered "dense". Unlike KMeans++, these two parameters
could not be linked directly to the visualization and the user easily end up with only one cluster so it is difficult for the user to make sense out of the visualization.
According to scikit-learn's documentation, DBSCAN's use cases are non-flat geometry and uneven cluster size which is the opposite of KMeans++.</br>
After trying different parameter combinations, the result does not look any better than KMeans++ technique.
</p><p>
Considering the difficulity to tune the parameters and the accessibility to link the parameters to the visualization. I think KMeans/KMeans++ are more proper
for visual exploration and analytics unless the parameters are all fine tuned(could not be changed by user) and visualization is used only as a way of presentation but
that will defeat the purpose of adding interactions to the visualization.</p>
""",width=800)
layout=layout([[div1],[div2],[xaxisselect,yaxisselect],[clusteringselect,numclusterselect],[epstext,minsamplestext],[plot]])
curdoc().add_root(layout)
