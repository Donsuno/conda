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

def on_button_clicked(b):

    clear_output()
    display(button)
## UPLOADED INITIAL DATA
#     if mv.value !='':
#         try:

    data = pd.read_excel('story_'+ story.value+'/story'+ story.value+'.xlsx', sheet_name='sample')
    # data=data.drop(['FC_D','FC_E','FC_F'],axis=1)
    data['Departure_Date']=pd.to_datetime(data.Departure_Date)
    datadone=data[data.Departure_Date< pd.Timestamp(nowaday.value)]
    data=data[data.Departure_Date>= pd.Timestamp(nowaday.value)]
    ## 1. Sort by Arival Date and Priority
    data=data.sort_values(by=['Arrival_Date','Price'], ascending=[True,False])

    ## 2. Set Parameter and Constraint
    #Total Floating Crane
    a=1
    b=1
    c=1
    totfc = int(fcnumber.value)
    fclist=['FC_A','FC_B','FC_C']

    #### Create feature demanddays for 1 floating crane
    data['demanddays']= np.round(data.Demand_Qty/data.Loading_Rate)
    data['demandfc']=np.ceil(data['demanddays']/data.Laytime_Duration)
    data['demanddays_new']=np.ceil(data.Demand_Qty/(data.Loading_Rate*data['demandfc']))
    ## 3. Assign Floating Crane - Initial Plan
    # to get initial plan

    ### create initial first row
    import itertools
    a=[]
    for L in range(1, len(fclist)+1):
        for subset in itertools.combinations(fclist, L):
    #         print(subset)
            x=list(subset)
            a.append(x)
    a=[[1,0,0],
     [0,1,0],
     [0,0,1],
     [1,1,0],
     [1,0,1],
     [0,1,1],
    ]
    a=pd.DataFrame(a,columns=['FC_A', 'FC_B', 'FC_C'])

    if (data.loc[0,'demandfc']==1) == True:
        data.loc[0, 'FC_A'] = 1
        data.loc[0, 'FC_B'] = 0
        data.loc[0, 'FC_C'] = 0
    elif (data.loc[0,'demandfc']==2) == True :
        data.loc[0, 'FC_A'] = 1
        data.loc[0, 'FC_B'] = 1
        data.loc[0, 'FC_C'] = 0
    else:
        data.loc[0, 'FC_A'] = 1
        data.loc[0, 'FC_B'] = 1
        data.loc[0, 'FC_C'] = 1

    ### complete initial plan
    for i in range(1,data.shape[0]):

        if (data.loc[i,'demandfc'] == 1):
            data.loc[i, 'FC_A'] = 1
            data.loc[i, 'FC_B'] = 0
            data.loc[i, 'FC_C'] = 0
        elif (data.loc[i,'demandfc'] == 2) :

            for fc in range(a.shape[0]):
                if ((data.loc[i-1,'FC_A'])== (a.loc[fc,'FC_A'])) & ((data.loc[i-1,'FC_B'])== (a.loc[fc,'FC_B'])) & ((data.loc[i-1,'FC_C'])== (a.loc[fc,'FC_C'])): 
                    data.loc[i, 'FC_A'] = np.abs((a.loc[fc,'FC_A'])-1)
                    data.loc[i, 'FC_B'] = np.abs((a.loc[fc,'FC_B'])-1)
                    data.loc[i, 'FC_C'] = np.abs((a.loc[fc,'FC_C'])-1)
                    if ((data.loc[i, 'FC_A'] + data.loc[i, 'FC_B'] +data.loc[i, 'FC_C'] )==1) & (data.loc[i, 'FC_A']==0):
                        data.loc[i, 'FC_A']=1
                    elif ((data.loc[i, 'FC_A'] + data.loc[i, 'FC_B'] +data.loc[i, 'FC_C'] )==1) & (data.loc[i, 'FC_B']==0):
                        data.loc[i, 'FC_B']=1
                    elif ((data.loc[i, 'FC_A'] + data.loc[i, 'FC_B'] +data.loc[i, 'FC_C'] )==1) & (data.loc[i, 'FC_C']==0):
                        data.loc[i, 'FC_C']=1
                    else:continue
                else:continue
        else:
            data.loc[i, 'FC_A'] = 1
            data.loc[i, 'FC_B'] = 1
            data.loc[i, 'FC_C'] = 1  
    ## 4. Recalculate Departure Date
    #     based on real demanddays_new

    data['Arrival_Date_change']=pd.to_datetime(np.nan)
    data['Departure_Date_change']=pd.to_datetime(np.nan)
    data.loc['FC_gap_Date_change'] = pd.to_datetime(np.nan)


    data=data[['MV', 'ETA','Arrival_Date', 'Laytime_Duration', 'Departure_Date',
       'Demand_Qty', 'Loading_Rate', 'Price', 'Demurrage_Rate', 'demanddays',
       'demandfc', 'demanddays_new',
               'FC_A', 'FC_B', 'FC_C',
                   'FC_D','FC_E','FC_F',
       'Arrival_Date_change', 'Departure_Date_change']]
    datachange=pd.DataFrame([[mv.value,arvl.value]],columns=['MV','Arrival_Date_change_source'])
    datachange['Arrival_Date_change_source']=pd.to_datetime(datachange.Arrival_Date_change_source)
    data=pd.merge(data,datachange,how='left',on=['MV'])
    data['Arrival_Date']=pd.to_datetime(data.Arrival_Date)
    data['Departure_Date']=pd.to_datetime(data.Departure_Date)
    # data['Arrival_Date_change']=pd.to_datetime(data.Arrival_Date_change)
    data['Arrival_Date_change']=data['Arrival_Date_change_source']
    data['Est_Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta(data['demanddays_new'], unit='D')
    data['Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta(10, unit='D')

    # data['Departure_Date_change']=pd.to_datetime(data.Departure_Date_change)
    data.loc[data.Arrival_Date_change.isnull() ,'Arrival_Date_change']=data.loc[data.Arrival_Date_change.isnull()  ,'Arrival_Date']
    data['Est_Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta(data['demanddays_new'], unit='D')# data.loc[0, 'Arrival_Date_change']=pd.to_datetime(data.loc[0,'Arrival_Date_change_source'])
    # data.loc[0,'Departure_Date_change']=data.loc[0,'Arrival_Date_change']+pd.to_timedelta(data.loc[0,'demanddays_new'], unit='D')
    data['Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta(10, unit='D')

    data.drop('Arrival_Date_change_source',axis=1,inplace=True)
    x=datachange['MV'][0]

    ### 6. Check the next sequence Schedule
    #     If the departure date change is clash, so FC_start_date_change must be adjusted and check the potential demorage cost

    ## Sort by Arival Date Change and Priority (Price)
    data=data.sort_values(by=['Arrival_Date_change','Price'], ascending=[True,False])
    data=data.reset_index()
    data.drop('index',axis=1,inplace=True)
    data['FC_Start_Date_change']=data['Arrival_Date_change']
    data['FC_End_Date_change']=data['Est_Departure_Date_change']

#             data.loc[data.MV== x ,'FC_Start_Date_change']=data.loc[data.MV== x ,'Arrival_Date_change']
#             data.loc[data.MV== x ,'FC_End_Date_change']=data.loc[data.MV== x ,'Est_Departure_Date_change']
#             data.loc[(data.MV!= x) & (data.FC_Start_Date_change.isnull()),'FC_Start_Date_change']=data.loc[data.MV!= x ,'Arrival_Date_change']
#             data.loc[(data.MV!= x) & (data.FC_End_Date_change.isnull()),'FC_End_Date_change']=data.loc[data.MV!= x ,'Est_Departure_Date_change']


    # Calculate Demurage cost
    data.loc[0,'Demmurage_Day']=0
    data.loc[0,'Demmurage_Cost']=0

    ### Create Demmuragecost Simulation Function

    def sim_demuragecost(totfc,data):
        totfc=totfc
        for i in range(1,data.shape[0]):
            #if previous iteration row value is greater than current iteration row value then
            if (data.loc[i-1,'Est_Departure_Date_change'] >= data.loc[i,'Arrival_Date_change']) :
                totfc=totfc-data.loc[i-1,'demanddays_new']
                #if available fc >= demand fc i
                if (totfc >= data.loc[i,'demanddays_new'] ):
                    data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']
                    data.loc[i,'FC_End_Date_change'] = data.loc[i,'Est_Departure_Date_change']
                    # Calculate Demurage cost
                    data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'Departure_Date_change'])/np.timedelta64(1,'D'))
                    data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
#                     data.loc[i,'FC_gap_Date_change'] = data.loc[i,'Departure_Date_change'] + pd.to_timedelta(1, unit='D') 

#                             data.loc[i,'Demmurage_Day']=0 #will be no risk to get demurage day n cost
#                             data.loc[i,'Demmurage_Cost']=0
                #if available fc < demand fc i and fc is at least available for one then
                elif (totfc < data.loc[i,'demanddays_new']) & (totfc >0):
                    #state the available FC to start operate
                    data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']
                    data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                    #cal the number of days that available FC can start
                    data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                    #cal the remaining quantity that is already loaded by available FC
                    data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*totfc*data.loc[i,'dayrun_progress'])
                    #cal the remaining number of FC to fulfill the demand
                    data.loc[i,'demandfc_remain'] = data.loc[i,'demanddays_new'] - totfc
                    #re-cal the total demandays based on this condition
                    data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demanddays_new'])) +data.loc[i,'dayrun_progress']
                    #cal the end date fc operate
                    data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                    # Calculate Demurage cost
                    data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'Departure_Date_change'])/np.timedelta64(1,'D'))
                    data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
#                     data.loc[i,'FC_gap_Date_change'] = data.loc[i,'Departure_Date_change'] + pd.to_timedelta(1, unit='D') 

                #if available fc < demand fc i and fc none available then
                else:
                    #the fc must start till the previous mv finisih to load
                    data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') 
                    data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                    # Calculate Demurage cost
                    data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'Departure_Date_change'])/np.timedelta64(1,'D'))
                    data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
#                     data.loc[i,'FC_gap_Date_change'] = data.loc[i,'Departure_Date_change'] + pd.to_timedelta(1, unit='D') 
                totfc=3 #reset to initial total fc
            else:
                totfc = 3
                data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']
                data.loc[i,'FC_End_Date_change'] = data.loc[i,'Est_Departure_Date_change']
                data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'Departure_Date_change'])/np.timedelta64(1,'D'))
                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
#                 data.loc[i,'FC_gap_Date_change'] = data.loc[i,'Departure_Date_change'] + pd.to_timedelta(1, unit='D') 

        data.loc[data.Demmurage_Day<=0 ,'Demmurage_Day']=0
        data.loc[data.Demmurage_Cost<=0 ,'Demmurage_Cost']=0
#         data.loc[data.Demmurage_Cost<=0 ,'FC_gap_Date_change']=data.loc[data.Demmurage_Cost<=0 ,'FC_End_Date_change']
        return data
    ### Call function
    data=sim_demuragecost(totfc,data)
    data

    def gantt_fig3(data):
        data3 = []
        for row in data.itertuples():
            data3.append(dict(Task=str(row.MV), Start=str(row.Arrival_Date_change),
                          Finish=str(row.Departure_Date_change), Resource='Plan'))
            data3.append(dict(Task=str(row.MV), Start=str(row.FC_Start_Date_change),
                          Finish=str(row.FC_End_Date_change), Resource='Actual'))


        fig = ff.create_gantt(data3, index_col='Resource', title='Gantt Chart', show_colorbar = True, group_tasks = True , height=500, width=1300 )
        fig['layout'].update(legend=dict(traceorder='reversed'))
        return fig

    iplot(gantt_fig3(data))
    data=pd.concat(datadone,data)
    newtable=data
    posttable=data
    newtable.columns
    newtable['Arrival_Date']=newtable.Arrival_Date_change
    newtable['Departure_Date']=newtable.Departure_Date_change
    tab=newtable[['MV', 'ETA', 'Arrival_Date', 'Laytime_Duration', 'Departure_Date',
       'Demand_Qty', 'Loading_Rate', 'Price',
                  'FC_A', 'FC_B', 'FC_C', 'FC_D','FC_E', 'FC_F', 
                  'Demmurage_Day', 'Demurrage_Rate', 'Demmurage_Cost']]
    tab.to_excel('story_'+ story.value+'/story'+ story.value+'.xlsx',sheet_name='sample',engine='xlsxwriter',index=False)

    data.drop(['demanddays'],axis=1,inplace=True)
    data.rename(columns={'demanddays_new':'demanddays'},inplace=True)
    print( 'Total demurage cost: USD ' +str(data.Demmurage_Cost.sum()))
    button
    data.dropna(axis=0, how='all', thresh=None, subset=None, inplace=True)
    data=data.drop(['FC_A', 'FC_B', 'FC_C', 'FC_D','FC_E', 'FC_F'],axis=1)
    data

    return button,  display(data),data;