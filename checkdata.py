def checkdata(b):
    clear_output()
    display(button0)
    print('Initial Data Condition:')
    #checkdata = pd.read_excel('story_'+ story.value+'/story'+ story.value+'.xlsx', sheet_name='sample')
    checkdata = pd.read_excel('story_0/story0'+'.xlsx', sheet_name='sample')
    checkdata['FC_Start_Date'] = checkdata['Arrival_Date'] + pd.to_timedelta(1, unit='D') #startdate next fc
    
    #### Create feature demanddays for 1 floating crane
    checkdata['demanddays']= np.ceil(checkdata.Demand_Qty/checkdata.Loading_Rate)
    checkdata['demandfc']=np.ceil(checkdata['demanddays']/checkdata.Laytime_Duration)
    checkdata.loc[checkdata.demandfc>2,'demandfc']=2
    checkdata['demanddays_new']=np.ceil(checkdata.Demand_Qty/(checkdata.Loading_Rate*checkdata['demandfc']))
    checkdata['FC_End_Date'] = checkdata['FC_Start_Date'] + pd.to_timedelta(checkdata['demanddays'], unit='D') #startdate next fc
    checkdata['Arrival_Date_change']=checkdata.Arrival_Date
    checkdata['Departure_Date_change']=checkdata.Departure_Date
    checkdata['FC_Start_Date_change']=checkdata.FC_Start_Date
    checkdata['FC_End_Date_change']=checkdata.FC_End_Date
    chartdata1=checkdata[['MV', 'Price','Arrival_Date','Departure_Date']]
    chartdata1['x']=chartdata1.MV
    for i in range(0,chartdata1.shape[0]):
        chartdata1.loc[i,'MV'] = '1 arv plan - '+chartdata1.loc[i,'MV']

    chartdata2=checkdata[['MV', 'Price','Arrival_Date_change','Departure_Date_change']]
    chartdata2['x']=chartdata2.MV
    for i in range(0,chartdata2.shape[0]):
        chartdata2.loc[i,'MV'] = '2 arv actual - '+chartdata2.loc[i,'MV']

    chartdata3=checkdata[['MV', 'Price','FC_Start_Date','FC_End_Date']]
    chartdata3['x']=chartdata3.MV
    for i in range(0,chartdata3.shape[0]):
        chartdata3.loc[i,'MV'] = '3 FC work plan - '+chartdata3.loc[i,'MV']

    chartdata4=checkdata[['MV', 'Price','FC_Start_Date_change','FC_End_Date_change']]
    chartdata4['x']=chartdata4.MV
    for i in range(0,chartdata4.shape[0]):
        chartdata4.loc[i,'MV'] = '4 FC work actual - '+chartdata4.loc[i,'MV']


    chartdata=chartdata1.append(chartdata2,sort=False)
    chartdata=chartdata.append(chartdata3,sort=False)
    chartdata=chartdata.append(chartdata4,sort=False)

    chartdata=chartdata.sort_values(by=['x','MV','Arrival_Date_change','Price'], ascending=[True,True,True,False])
    chartdata=chartdata.reset_index()
    chartdata.drop('index',axis=1,inplace=True)
    chartdata
    def gantt_fig(chartdata):
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

        colors = dict(Plan_Arrival='rgb(0,0,150)',Actual_Arrival='rgb(0,0,255)' , Plan_FC_Working='rgb(255,140,0)',Actual_FC_Working='rgb(235, 220, 52)')
        fig = ff.create_gantt(data3, index_col='Resource', title='Gantt Chart', show_colorbar = True, group_tasks = True , height=500, width=1300 ,colors=colors)
    #     fig['layout'].update(legend=dict(traceorder='reversed'))
        return fig

    iplot(gantt_fig(chartdata))

    button0
    checkdata
    return button0, display(checkdata),checkdata