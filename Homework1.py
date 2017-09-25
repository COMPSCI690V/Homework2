
from bokeh.plotting import figure
from bokeh.models import Label,Button,Slider,ColumnDataSource,HoverTool,TapTool
from bokeh.layouts import layout
from bokeh.io import curdoc
import pandas as pd
import numpy as np


data=pd.read_excel('datasource.xlsx')


#get initial data
initial_data_raw=data['1948']
initial_dataframe=pd.DataFrame({'country':initial_data_raw.index,'interest':initial_data_raw.values})

#do plot
def SetMaxY(values):
    max_y=max(list(values))
    if max_y!=max_y:#check for nan
        max_y=10
    #return max_y
    return np.nanmax(values)
#do plot
plot=figure(x_range=list(initial_data_raw.index),y_range=(0,SetMaxY(initial_data_raw.values)),width=800,height=400,tools="tap")
plot.xaxis.major_label_text_font_size='0pt'#too many countries to show so hide
plot.yaxis.axis_label="Discount Rate"
plot.xaxis.axis_label="Countries"
plot.title.text="Indicator Discount Rate of Central Banks"
plot.title.align="center"
label=Label(x=0,y=5,text="1948",text_font_size='70pt')
plot.add_layout(label)


source=ColumnDataSource(initial_dataframe)
plot.vbar(source=source,x='country',top='interest',width=1,bottom=0)
plot.add_tools(HoverTool(tooltips=[("country","@country"),("interest rate","@interest%")]))



#will also be called when the trigger is button
def manual_update_plot(attrname,old,new):
    if attrname=='value':
        #value changed,do the update
        label.text=str(new)
        current_year_data_raw=data[str(new)]
        current_year_dataframe=dict({'country':current_year_data_raw.index,'interest':current_year_data_raw.values})
        source.data=current_year_dataframe
        plot.y_range.end=SetMaxY(current_year_data_raw.values)

slider=Slider(start=1948,end=2006,value=1948,step=1,title='Year')
slider.on_change('value',manual_update_plot)

#update_plot loops when button is in run state
def auto_update_plot():
    #get current slider value
    current_slider_value=slider.value
    if current_slider_value>2006:
        slider.value=1948
    else:
        slider.value=current_slider_value+1
        #print(slider.value)
    #set label text to be equal slider value
    label.text=str(slider.value)
#run executes when button is clicked
def run():
    if button.label=='run':
        curdoc().add_periodic_callback(auto_update_plot,400)
        button.label='stop'
    else:
        curdoc().remove_periodic_callback(auto_update_plot)
        button.label='run'

button=Button(label='run',width=60)
button.on_click(run)

layout=layout([[slider,button],[plot]])#,[label]])
curdoc().add_root(layout)



