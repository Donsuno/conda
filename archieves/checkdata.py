from ipywidgets import widgets,interact, interact_manual
import numpy as np
import pandas as pd
from IPython.display import display,clear_output
from numpy import arange, sin, pi
import plotly.figure_factory as ff
import re 
import matplotlib.pyplot as plt
from IPython.display import Image

from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()
%matplotlib inline
def checkdata(b):
    clear_output()
    display(button0)
    print('Initial Data Condition:')
    checkdata = pd.read_excel('story_'+ story.value+'/story'+ story.value+'.xlsx', sheet_name='sample')
    checkdata
    def gantt_fig(checkdata):
        data3 = []
        for row in checkdata.itertuples():
            data3.append(dict(Task=str(row.MV), Start=str(row.Arrival_Date),
                          Finish=str(row.Departure_Date), Resource='Initial Plan'))
#             data3.append(dict(Task=str(row.MV), Start=str(row.FC_Start_Date_change),
#                           Finish=str(row.FC_End_Date_change), Resource='Resource2'))


        fig = ff.create_gantt(data3, index_col='Resource', title='Gantt Chart', show_colorbar = True, group_tasks = True , height=500, width=1300 )
        fig['layout'].update(legend=dict(traceorder='reversed'))
        return fig
    iplot(gantt_fig(checkdata))

    button0
    checkdata
    return button0, display(checkdata),checkdata

    # button0, display(checkdata),checkdata=checkdata(b)