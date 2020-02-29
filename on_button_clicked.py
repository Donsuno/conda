def on_button_clicked(b):
    clear_output()
    display(button)
    fc=2
    ### Create Demmuragecost Simulation Function
    

## UPLOADED INITIAL DATA
    if (mv.value !='')==True:
        try:
            data = pd.read_excel('story_0/story0'+'.xlsx', sheet_name='sample')
            data['Departure_Date']=pd.to_datetime(data.Departure_Date)
            datadone=data[data.Departure_Date< pd.Timestamp(nowaday.value)]
            data=data[data.Departure_Date>= pd.Timestamp(nowaday.value)]
            ## 1. Sort by Arival Date and Priority
            data=data.sort_values(by=['Arrival_Date','Price'], ascending=[True,False])

            ## 2. Set Parameter and Constraint
            #Total Floating Crane
            totfc = 3
            #### Create feature demanddays for 1 floating crane working
            data['demanddays']= np.ceil(data.Demand_Qty/data.Loading_Rate)
            data['demandfc']=np.ceil(data['demanddays']/data.Laytime_Duration)
            data.loc[data.demandfc>2,'demandfc']=2
            data['demanddays_new']=np.ceil(data.Demand_Qty/(data.Loading_Rate*data['demandfc'])) 
            
            data['FC_Start_Date_change_2']=pd.to_datetime(np.nan)
#             data['FC_End_Date']=pd.to_datetime(np.nan)
#             data['FC_End_Date_change']=pd.to_datetime(np.nan)
            data['dayrun_progress']=(np.nan)
            data['Demand_Qty_remain']=(np.nan)
            data['demandfc_remain']=(np.nan)
            data=data[['MV', 'ETA','Arrival_Date', 'Laytime_Duration', 'Departure_Date',
                           'Demand_Qty', 'Loading_Rate', 'Price', 'Demurrage_Rate', 'demanddays',
                           'demandfc', 'demanddays_new',
                           'Arrival_Date_change', 'Departure_Date_change','FC_Start_Date_change','FC_Start_Date','FC_Start_Date_change_2',
                       'FC_End_Date','FC_End_Date_change','dayrun_progress','Demand_Qty_remain','demandfc_remain']]
            datachange=pd.DataFrame([[mv.value,arvl.value]],columns=['MV','Arrival_Date_change_source'])
            datachange['Arrival_Date_change_source']=pd.to_datetime(datachange.Arrival_Date_change_source)
            data=pd.merge(data,datachange,how='left',on=['MV'])
            data['Arrival_Date']=pd.to_datetime(data.Arrival_Date)
            data['Departure_Date']=pd.to_datetime(data.Departure_Date)
            data.loc[data.MV == mv.value,'Arrival_Date_change']=data.loc[data.MV == mv.value ,'Arrival_Date_change_source']
            data['Est_Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta((data['demanddays_new']+1), unit='D')
            data['Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta(10, unit='D')
            data.loc[data.Arrival_Date_change.isnull() ,'Arrival_Date_change']=data.loc[data.Arrival_Date_change.isnull()  ,'Arrival_Date']
            data['Est_Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta((data['demanddays_new']+1), unit='D')
            data['Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta(10, unit='D')
            data['FC_Start_Date']=data['Arrival_Date_change']+pd.to_timedelta(1, unit='D')
            data['FC_End_Date']=data['FC_Start_Date']+pd.to_timedelta(data['demanddays'], unit='D')

            data.drop('Arrival_Date_change_source',axis=1,inplace=True)
            x=datachange['MV'][0]

            ### 6. Check the next sequence Schedule
            #     If the departure date change is clash, so FC_start_date_change must be adjusted and check the potential demurage cost

            ## Sort by Arival Date Change and Priority (Price)
            data=data.sort_values(by=['Arrival_Date_change','Price'], ascending=[True,False])
            data=data.reset_index()
            data.drop('index',axis=1,inplace=True)
            data['FC_Start_Date_change']=data['Arrival_Date_change']+pd.to_timedelta(1, unit='D')
            data['FC_End_Date_change']=data['Est_Departure_Date_change']

            # Calculate Demurage cost
            data.loc[0,'Demmurage_Day']=0
            data.loc[0,'Demmurage_Cost']=0
            # Calculate Dispatch cost
            data.loc[0,'Dispatch_Day']=np.ceil((data.loc[0,'FC_End_Date'] - data.loc[0,'FC_End_Date_change'])/np.timedelta64(1,'D'))
            if data.loc[0,'Dispatch_Day'] <0:
                data.loc[0,'Dispatch_Value']=0
            else:
                data.loc[0,'Dispatch_Value']=data.loc[0,'Dispatch_Day'] * data.loc[0,'Demurrage_Rate']/2

            
            ### Call function
            data=sim_demuragecost(totfc,data)
            prioritybase=data[['MV', 'Price','Arrival_Date_change']].sort_values(by=['Arrival_Date_change','Price'], ascending=[True,False])
            prioritybase=prioritybase.reset_index()
            
            data=pd.merge(data,prioritybase[['MV','index']],how='left',on='MV')
            chartdata1=data[['index','MV', 'Price','Arrival_Date','Departure_Date']]
            chartdata1['x']=chartdata1.MV
            for i in range(0,chartdata1.shape[0]):
                chartdata1.loc[i,'MV'] = '1 arv plan - '+chartdata1.loc[i,'MV']

            chartdata2=data[['index','MV', 'Price','Arrival_Date_change','Departure_Date_change']]
            chartdata2['x']=chartdata2.MV
            for i in range(0,chartdata2.shape[0]):
                chartdata2.loc[i,'MV'] = '2 arv actual - '+chartdata2.loc[i,'MV']

            chartdata3=data[['index','MV', 'Price','FC_Start_Date','FC_End_Date']]
            chartdata3['x']=chartdata3.MV
            for i in range(0,chartdata3.shape[0]):
                chartdata3.loc[i,'MV'] = '3 FC work plan - '+chartdata3.loc[i,'MV']

            chartdata4=data[['index','MV', 'Price','FC_Start_Date_change','FC_End_Date_change']]
            chartdata4['x']=chartdata4.MV
            for i in range(0,chartdata4.shape[0]):
                chartdata4.loc[i,'MV'] = '4 FC work actual - '+chartdata4.loc[i,'MV']

            chartdata=chartdata1.append(chartdata2,sort=False)
            chartdata=chartdata.append(chartdata3,sort=False)
            chartdata=chartdata.append(chartdata4,sort=False)
            
            chartdata=chartdata.sort_values(by=['index','x'], ascending=[True,True])
            chartdata=chartdata.reset_index()
            chartdata.drop('index',axis=1,inplace=True)
            chartdata
            def gantt_fig3(chartdata):
                data3 = []
                for row in chartdata.itertuples():
                    data3.append(dict(Task=str(row.MV), Start=str(row.Arrival_Date),
                                  Finish=str(row.Departure_Date), Resource='Plan_Arrival'))
                    data3.append(dict(Task=str(row.MV), Start=str(row.Arrival_Date_change),
                                  Finish=str(row.Departure_Date_change), Resource='Actual_Arrival'))
                    data3.append(dict(Task=str(row.MV), Start=str(row.FC_Start_Date),
                                  Finish=str(row.FC_End_Date), Resource='Plan_FC_Working'))
                    data3.append(dict(Task=str(row.MV), Start=str(row.FC_Start_Date_change),
                                  Finish=str(row.FC_End_Date_change), Resource='Actual_FC_Working'))

                colors = dict(Plan_Arrival='rgb(0,0,255)',Actual_Arrival='rgb(0,0,150)' , Plan_FC_Working='rgb(255,140,0)',Actual_FC_Working='rgb(255,50,0)')
                fig = ff.create_gantt(data3, index_col='Resource', title='Gantt Chart', show_colorbar = True, group_tasks = True , height=500, width=1300 ,colors=colors)
            #     fig['layout'].update(legend=dict(traceorder='reversed'))
                return fig
            
            
#             data=pd.concat([datadone,data],sort=False)
            newtable=data
            posttable=data
            newtable.columns
#             newtable['Arrival_Date']=newtable.Arrival_Date_change
#             newtable['Departure_Date']=newtable.Departure_Date_change
            tab=newtable[['MV', 'ETA', 'Arrival_Date', 'Laytime_Duration', 'Departure_Date',
               'Demand_Qty', 'Loading_Rate', 'Price','Demmurage_Day', 'Demurrage_Rate', 'Demmurage_Cost','Arrival_Date_change','Departure_Date_change','FC_Start_Date','FC_Start_Date_change','FC_End_Date','FC_End_Date_change']]
            tab.to_excel('story_0'+ '/story0'+'.xlsx',sheet_name='sample',engine='xlsxwriter',index=False)
#             data.drop(['demanddays'],axis=1,inplace=True)
#             data.rename(columns={'demanddays_new':'demanddays'},inplace=True)
            print( 'Total demurage cost: USD ' +str(data.Demmurage_Cost.sum()))
            print( 'Total dispatch value: USD ' +str(data.Dispatch_Value.sum()))
            button
            data.dropna(axis=0, how='all', thresh=None, subset=None, inplace=True)
            data=data[['MV', 'Arrival_Date', 'Departure_Date',
               'Demand_Qty',  'Price', 'Demmurage_Day', 'Dispatch_Value', 'Demmurage_Cost', 'demanddays','demanddays_new',
               'demandfc', 'Arrival_Date_change', 'Departure_Date_change','FC_Start_Date','FC_Start_Date_change','FC_Start_Date_change_2','FC_End_Date','FC_End_Date_change'
                       ,'dayrun_progress','Demand_Qty_remain','demandfc_remain'
                      ]]
            data
            return button,iplot(gantt_fig3(chartdata)),  display(data),data;
        except:
            print("Out of prototype limit")
            
    else:
        try:
#             print('nomv change')
            data = pd.read_excel('story_0/story0'+'.xlsx', sheet_name='sample')
            # data=data.drop(['FC_D','FC_E','FC_F'],axis=1)
            data['Departure_Date']=pd.to_datetime(data.Departure_Date)
            ## 1. Sort by Arival Date and Priority
            data=data.sort_values(by=['Arrival_Date','Price'], ascending=[True,False])

            ## 2. Set Parameter and Constraint
            #Total Floating Crane
            totfc = 3

            #### Create feature demanddays for 1 floating crane
            data['demanddays']= np.ceil(data.Demand_Qty/data.Loading_Rate)
            data['demandfc']=np.ceil(data['demanddays']/data.Laytime_Duration)
            data.loc[data.demandfc>2,'demandfc']=2
            data['demanddays_new']=np.ceil(data.Demand_Qty/(data.Loading_Rate*data['demandfc']))
            ## 4. Recalculate Departure Date
            #     based on real demanddays_new
#             data['Arrival_Date_change']=pd.to_datetime(np.nan)
#             data['Departure_Date_change']=pd.to_datetime(np.nan)
#             data['FC_Start_Date']=pd.to_datetime(np.nan)
#             data['FC_Start_Date_change']=pd.to_datetime(np.nan)
            data['FC_Start_Date_change_2']=pd.to_datetime(np.nan)
#             data['FC_End_Date']=pd.to_datetime(np.nan)
#             data['FC_End_Date_change']=pd.to_datetime(np.nan)
            data['dayrun_progress']=(np.nan)
            data['Demand_Qty_remain']=(np.nan)
            data['demandfc_remain']=(np.nan)
            data=data[['MV', 'ETA','Arrival_Date', 'Laytime_Duration', 'Departure_Date',
                           'Demand_Qty', 'Loading_Rate', 'Price', 'Demurrage_Rate', 'demanddays',
                           'demandfc', 'demanddays_new',
                           'Arrival_Date_change', 'Departure_Date_change','FC_Start_Date_change','FC_Start_Date','FC_Start_Date_change_2',
                       'FC_End_Date','FC_End_Date_change','dayrun_progress','Demand_Qty_remain','demandfc_remain']]
            data['Arrival_Date']=pd.to_datetime(data.Arrival_Date)
            data['Departure_Date']=pd.to_datetime(data.Departure_Date)
#             data['FC_Start_Date']=data['Arrival_Date']+pd.to_timedelta(1, unit='D')
#             data['FC_End_Date']=data['FC_Start_Date']+pd.to_timedelta(data['demanddays'], unit='D')
            data['Est_Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta((data['demanddays_new']+1), unit='D')
            data['Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta(10, unit='D')
            data.loc[data.Arrival_Date_change.isnull() ,'Arrival_Date_change']=data.loc[data.Arrival_Date_change.isnull()  ,'Arrival_Date'] #fill the remaining nulldata
            data['Est_Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta((data['demanddays_new']+1), unit='D')
            data['Departure_Date_change']=data['Arrival_Date_change']+pd.to_timedelta(10, unit='D')
            data['FC_Start_Date']=data['Arrival_Date']+pd.to_timedelta(1, unit='D')
            data['FC_End_Date']=data['FC_Start_Date']+pd.to_timedelta(data['demanddays'], unit='D')

            ### 6. Check the next sequence Schedule
            #     If the departure date change is clash, so FC_start_date_change must be adjusted and check the potential demorage cost

            ## Sort by Arival Date Change and Priority (Price)
            data=data.sort_values(by=['Arrival_Date_change','Price'], ascending=[True,False])
            data=data.reset_index()
            data.drop('index',axis=1,inplace=True)
            data['FC_Start_Date_change']=data['Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
            data['FC_End_Date_change']=data['Est_Departure_Date_change']

            # Calculate Demurage cost
            data.loc[0,'Demmurage_Day']=0
            data.loc[0,'Demmurage_Cost']=0
            # Calculate Dispatch cost
            data.loc[0,'Dispatch_Day']=np.ceil((data.loc[0,'FC_End_Date'] - data.loc[0,'FC_End_Date_change'])/np.timedelta64(1,'D'))
            if data.loc[0,'Dispatch_Day'] <0:
                data.loc[0,'Dispatch_Value']=0
            else:
                data.loc[0,'Dispatch_Value']=data.loc[0,'Dispatch_Day'] * data.loc[0,'Demurrage_Rate']/2
                
            ### Call function
            data=sim_demuragecost(totfc,data)
            prioritybase=data[['MV', 'Price','Arrival_Date_change']].sort_values(by=['Arrival_Date_change','Price'], ascending=[True,False])
            prioritybase=prioritybase.reset_index()
            
            data=pd.merge(data,prioritybase[['MV','index']],how='left',on='MV')
            chartdata1=data[['index','MV', 'Price','Arrival_Date','Departure_Date']]
            chartdata1['x']=chartdata1.MV
            for i in range(0,chartdata1.shape[0]):
                chartdata1.loc[i,'MV'] = '1 arv plan - '+chartdata1.loc[i,'MV']

            chartdata2=data[['index','MV', 'Price','Arrival_Date_change','Departure_Date_change']]
            chartdata2['x']=chartdata2.MV
            for i in range(0,chartdata2.shape[0]):
                chartdata2.loc[i,'MV'] = '2 arv actual - '+chartdata2.loc[i,'MV']

            chartdata3=data[['index','MV', 'Price','FC_Start_Date','FC_End_Date']]
            chartdata3['x']=chartdata3.MV
            for i in range(0,chartdata3.shape[0]):
                chartdata3.loc[i,'MV'] = '3 FC work plan - '+chartdata3.loc[i,'MV']

            chartdata4=data[['index','MV', 'Price','FC_Start_Date_change','FC_End_Date_change']]
            chartdata4['x']=chartdata4.MV
            for i in range(0,chartdata4.shape[0]):
                chartdata4.loc[i,'MV'] = '4 FC work actual - '+chartdata4.loc[i,'MV']

            chartdata=chartdata1.append(chartdata2,sort=False)
            chartdata=chartdata.append(chartdata3,sort=False)
            chartdata=chartdata.append(chartdata4,sort=False)
            
            chartdata=chartdata.sort_values(by=['index','x'], ascending=[True,True])
            chartdata=chartdata.reset_index()
            chartdata.drop('index',axis=1,inplace=True)
            chartdata
            def gantt_fig3(chartdata):
                data3 = []
                for row in chartdata.itertuples():
                    data3.append(dict(Task=str(row.MV), Start=str(row.Arrival_Date),
                                  Finish=str(row.Departure_Date), Resource='Plan_Arrival'))
                    data3.append(dict(Task=str(row.MV), Start=str(row.Arrival_Date_change),
                                  Finish=str(row.Departure_Date_change), Resource='Actual_Arrival'))
                    data3.append(dict(Task=str(row.MV), Start=str(row.FC_Start_Date),
                                  Finish=str(row.FC_End_Date), Resource='Plan_FC_Working'))
                    data3.append(dict(Task=str(row.MV), Start=str(row.FC_Start_Date_change),
                                  Finish=str(row.FC_End_Date_change), Resource='Actual_FC_Working'))

                colors = dict(Plan_Arrival='rgb(0,0,255)',Actual_Arrival='rgb(0,0,150)' , Plan_FC_Working='rgb(255,140,0)',Actual_FC_Working='rgb(255,50,0)')
                fig = ff.create_gantt(data3, index_col='Resource', title='Gantt Chart', show_colorbar = True, group_tasks = True , height=500, width=1300 ,colors=colors)
            #     fig['layout'].update(legend=dict(traceorder='reversed'))
                return fig
            
#             data=pd.concat([datadone,data],sort=False)
            data
            newtable=data
            posttable=data
            newtable.columns
#             newtable['Arrival_Date']=newtable.Arrival_Date_change
#             newtable['Departure_Date']=newtable.Departure_Date_change
            tab=newtable[['MV', 'ETA', 'Arrival_Date', 'Laytime_Duration', 'Departure_Date',
               'Demand_Qty', 'Loading_Rate', 'Price',
                          'Demmurage_Day', 'Demurrage_Rate', 'Demmurage_Cost','Arrival_Date_change','Departure_Date_change','FC_Start_Date','FC_Start_Date_change','FC_End_Date','FC_End_Date_change']]
            tab.to_excel('story_0'+ '/story0'+'.xlsx',sheet_name='sample',engine='xlsxwriter',index=False)
#             data.drop(['demanddays'],axis=1,inplace=True)
#             data.rename(columns={'demanddays_new':'demanddays'},inplace=True)
            print( 'Total demurage cost: USD ' +str(data.Demmurage_Cost.sum()))
            print( 'Total dispatch value: USD ' +str(data.Dispatch_Value.sum()))
            button
            data.dropna(axis=0, how='all', thresh=None, subset=None, inplace=True)
            data=data[['MV', 'Arrival_Date',  'Departure_Date',
               'Demand_Qty','Price', 'Demmurage_Day', 'Dispatch_Value','Demmurage_Cost', 'demanddays','demanddays_new',
               'demandfc', 
               'Arrival_Date_change', 'Departure_Date_change','FC_Start_Date','FC_Start_Date_change','FC_Start_Date_change_2','FC_End_Date','FC_End_Date_change'
                       ,'dayrun_progress','Demand_Qty_remain','demandfc_remain'
                      ]]
            data
            return button, iplot(gantt_fig3(chartdata)), display(data),data;
        except:
            print("Out of prototype limit")
    