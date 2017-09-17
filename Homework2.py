from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import Dropdown,ColumnDataSource,HoverTool,TextInput,Div
from bokeh.plotting import figure
import pandas as pd
import math
import numpy as np

data_nomissing=pd.read_csv("Wholesale customers data.csv")
data_missing=pd.read_csv("Wholesale customers data-missing.csv")
data_dropping=data_missing.dropna()
data_interpolation=data_missing.interpolate()

menu = [
    ("channel", "Channel"), 
    ("region", "Region"),
    ("fresh", "Fresh"),
    ("milk","Milk"),
    ("grocery","Grocery"),
    ("frozen","Frozen"),
    ("detergents and paper","Detergents_Paper"),
    ("delicassen","Delicassen")
    ]
option1 = Dropdown(label="X Axis", button_type="default", menu=menu)
option2 = Dropdown(label="Y Axis", button_type="default", menu=menu)
option3 = Dropdown(label="Size", button_type="default", menu=menu)

def updateplot():
    #check all options have values
    if option1.value is not None and option2.value is not None and option3.value is not None:
        source_scatter_nomissing.data=dict({'xaxis':data_nomissing[option1.value],'yaxis':data_nomissing[option2.value],'size':data_nomissing[option3.value]})
        source_scatter_missing.data=dict({'xaxis':data_dropping[option1.value],'yaxis':data_dropping[option2.value],'size':data_dropping[option3.value]})
        source_scatter_interpolate.data=dict({'xaxis':data_interpolation[option1.value],'yaxis':data_interpolation[option2.value],'size':data_interpolation[option3.value]})
        scatterplot_nomissing.add_tools(HoverTool(tooltips=[(option1.value,"@xaxis"),(option2.value,"@yaxis"),(option3.value,"@size")]))
        scatterplot_deleting.add_tools(HoverTool(tooltips=[(option1.value,"@xaxis"),(option2.value,"@yaxis"),(option3.value,"@size")]))
        scatterplot_interpolation.add_tools(HoverTool(tooltips=[(option1.value,"@xaxis"),(option2.value,"@yaxis"),(option3.value,"@size")]))

def option1_changed(attrname,old,new):
    option1.label="X Axis - "+menu[[i for i,v in enumerate(menu) if v[1]==new][0]][0]
    updateplot()
def option2_changed(attrname,old,new):
    option2.label="Y Axis - "+menu[[i for i,v in enumerate(menu) if v[1]==new][0]][0]
    updateplot()
def option3_changed(attrname,old,new):
    option3.label="Size - "+menu[[i for i,v in enumerate(menu) if v[1]==new][0]][0]
    updateplot()

option1.on_change('value',option1_changed)
option2.on_change('value',option2_changed)
option3.on_change('value',option3_changed)

scatterplot_nomissing=figure(width=400,height=400)
scatterplot_nomissing.title.text="Scatter Plot without Missing Data"
scatterplot_nomissing.title.align='center'
scatterplot_deleting=figure(width=400,height=400,x_range=scatterplot_nomissing.x_range,y_range=scatterplot_nomissing.y_range)
scatterplot_deleting.title.text="Scatter Plot with Missing Data (Dropping the records)"
scatterplot_deleting.title.align='center'
scatterplot_interpolation=figure(width=400,height=400,x_range=scatterplot_nomissing.x_range,y_range=scatterplot_nomissing.y_range)
scatterplot_interpolation.title.text="Scatter Plot with Missing Data (Linear Regression)"
scatterplot_interpolation.title.align='center'

source_scatter_nomissing=ColumnDataSource(data=dict(xaxis=[],yaxis=[],size=[]))
source_scatter_missing=ColumnDataSource(data=dict(xaxis=[],yaxis=[],size=[]))
source_scatter_interpolate=ColumnDataSource(data=dict(xaxis=[],yaxis=[],size=[]))

scatterplot_nomissing.circle(source=source_scatter_nomissing,x='xaxis',y='yaxis',size='size')
scatterplot_deleting.circle(source=source_scatter_missing,x='xaxis',y='yaxis',size='size')
scatterplot_interpolation.circle(source=source_scatter_interpolate,x='xaxis',y='yaxis',size='size')


binmenu = [
    ("channel", "Channel"), 
    ("region", "Region"),
    ("fresh", "Fresh"),
    ("milk","Milk"),
    ("grocery","Grocery"),
    ("frozen","Frozen"),
    ("detergents and paper","Detergents_Paper"),
    ("delicassen","Delicassen")
    ]


binoption = Dropdown(label="Select Column", button_type="default", menu=binmenu)
textn = TextInput(value="", title="Number of Bins")
barwidth=10

def transformColumn(sortedcolumn,n):
    barwidth=n*2
    width=math.ceil((sortedcolumn[-1]-sortedcolumn[0])/n)
    binedges=[sortedcolumn[0]]
    while (binedges[-1]+width)<=sortedcolumn[-1]:
        binedges.append(binedges[-1]+width)
    hist,bin_edges=np.histogram(sortedcolumn, bins = binedges)
    bin_edges=list(bin_edges)
    bin_edges.remove(bin_edges[-1])
    return dict({'xaxis':bin_edges,'yaxis':list(hist)})
def binoption_update(attrname,old,new):
    if binoption.value is not None:
        binoption.label="Column - "+binmenu[[i for i,v in enumerate(menu) if v[1]==new][0]][0]
        binplot_update('value',0,0)
def binplot_update(attrname,old,new):
        if binoption.value is not None and textn.value.isdigit()==True:
            datanomissingcolumn=list(data_nomissing[binoption.value].sort_values())
            datamissingcolumn=list(data_interpolation[binoption.value].sort_values())
            source_bin_nomissing.data=transformColumn(datanomissingcolumn,int(textn.value))
            source_bin_missing.data=transformColumn(datamissingcolumn,int(textn.value))

binoption.on_change('value',binoption_update)
textn.on_change('value',binplot_update)

binplot_nomissing=figure(width=400,height=400)
binplot_nomissing.title.text="Binning without Missing Data (Equal Width)"
binplot_nomissing.title.align='center'
binplot_missing=figure(width=400,height=400,x_range=binplot_nomissing.x_range,y_range=binplot_nomissing.y_range)
binplot_missing.title.text="Binning with Missing Data (Equal Width)"
binplot_missing.title.align='center'

source_bin_nomissing=ColumnDataSource(data=dict(xaxis=[],yaxis=[]))
source_bin_missing=ColumnDataSource(data=dict(xaxis=[],yaxis=[]))

binplot_nomissing.vbar(source=source_bin_nomissing,x='xaxis',top='yaxis',width=barwidth,bottom=0)
binplot_missing.vbar(source=source_bin_missing,x='xaxis',top='yaxis',width=barwidth,bottom=0)

p1 = Div(text="""Homework2""",
width=800)
p2 = Div(text="""This project illustrated the use of<ul> <li>dropping records</li><li>linear regression</li><li>binning(interpolation)</li></ul> in handling missing data.</br> Select the dropdown options to start.""",
width=800)

layout=layout([
    [p1],
    [p2],
    [option1,option2,option3],
    [scatterplot_nomissing,scatterplot_deleting],
    [scatterplot_interpolation],
    [binoption,textn],
    [binplot_nomissing,binplot_missing]
    ])
curdoc().add_root(layout)