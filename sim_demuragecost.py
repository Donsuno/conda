def sim_demuragecost(totfc,data):
    totfc=fc
#         print(totfc)
    for i in range(1,data.shape[0]):
        if i <2:
            if ((data.loc[i,'Arrival_Date_change'] >=data.loc[i,'Arrival_Date']) & (data.loc[i,'Arrival_Date_change'] <=data.loc[i,'Departure_Date'])):
                data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                #if previous iteration row value is greater than current iteration row value then
                if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) :
                    totfc=fc-data.loc[i-1,'demandfc']
                    #if available fc >= demand fc i
                    if (totfc >= data.loc[i,'demandfc'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change']+pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule1')


                    #if available fc < demand fc i and fc is at least available for one and demand fc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demandfc'] )) + data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule2')
                    #if available fc < demand fc i and fc is at least available for one and demandfc=1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule3')
                    #if available fc < demand fc i and fc none available then
                    else:
                        #the fc must start till the previous mv finisih to load
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule4')
                else:#reset to initial total fc
                    totfc = fc
                    data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change'] + pd.to_timedelta(1, unit='D') 
                    data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                    data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                    if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                    else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                    # Calculate Dispatch cost
                    data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                    if data.loc[i,'Dispatch_Day'] <0:
                        data.loc[i,'Dispatch_Value']=0
                    else:
                        data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                    print(i)
                    print(totfc)
                    print('rule5')
            elif  (data.loc[i,'Arrival_Date_change'] > data.loc[i,'Departure_Date']):
                data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                #if previous iteration row value is greater than current iteration row value then
                if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) :
                    totfc=fc-data.loc[i-1,'demandfc']
                    #if available fc >= demand fc i
                    if (totfc >= data.loc[i,'demandfc'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change']+pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule6')
                    #if available fc < demand fc i and fc is at least available for one and demand fc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demandfc'] )) + data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule7')
                    #if available fc < demand fc i and fc is at least available for one and demandfc=1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule8')
                    #if available fc < demand fc i and fc none available then
                    else:
                        #the fc must start till the previous mv finisih to load
                        data.loc[i,'FC_Start_Date']=data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date'] + pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule9')
                else:#reset to initial total fc
                    totfc = fc
                    data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change'] + pd.to_timedelta(1, unit='D') 
                    data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                    data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                    if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                    else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                    # Calculate Dispatch cost
                    data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                    if data.loc[i,'Dispatch_Day'] <0:
                        data.loc[i,'Dispatch_Value']=0
                    else:
                        data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                    print(i)
                    print(totfc)
                    print('rule10')
            else: #MV arriv before plan then
                data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date']+pd.to_timedelta(1, unit='D')
                data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                #if previous iteration row value is greater than current iteration row value then
                if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) :
                    totfc=fc-data.loc[i-1,'demandfc']
                    #if available fc >= demand fc i
                    if (totfc >= data.loc[i,'demandfc'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date']+pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change']+pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule11')


                    #if available fc < demand fc i and fc is at least available for one and demand fc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date']+pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demandfc'] )) + data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule12')
                    #if available fc < demand fc i and fc is at least available for one and demandfc=1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date']+pd.to_timedelta(1, unit='D')
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule13')
                    #if available fc < demand fc i and fc none available then
                    else:
                        #the fc must start till the previous mv finisih to load
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule14')
                else:#reset to initial total fc
                    totfc = fc
                    data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date'] + pd.to_timedelta(1, unit='D') 
                    data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                    data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                    if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                    else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                    # Calculate Dispatch cost
                    data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                    if data.loc[i,'Dispatch_Day'] <0:
                        data.loc[i,'Dispatch_Value']=0
                    else:
                        data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                    print(i)
                    print(totfc)
                    print('rule15')

        else : #i >=2
            if ((data.loc[i,'Arrival_Date_change'] >=data.loc[i,'Arrival_Date']) & (data.loc[i,'Arrival_Date_change'] <=data.loc[i,'Departure_Date'])) :
                #if previous iteration row value is greater than current iteration row value then
                if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] <= data.loc[i-2,'FC_End_Date_change'] ) :
                    totfc=fc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
                    #if available fc > demand fc i
                    if (totfc >= data.loc[i,'demandfc']):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule16')
                    #if available fc < demand fc i and fc is at least available for one and demand fc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demandfc'] )) + data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule17')
                    #if available fc < demand fc i and fc is at least available for one and demandfc=1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule18')
                    #if available fc < demand fc i and fc none available then
                    else:
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] =1 # (data.loc[i,'demandfc'] - 1)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule19')
                        else:
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule20')
                elif (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] > data.loc[i-2,'FC_End_Date_change'] ) :
                    totfc=fc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
                    #if available fc > demand fc i
                    if (totfc >= data.loc[i,'demandfc']):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule21')
                    #if available fc < demand fc i and fc is at least available for one and demand fc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demandfc'] )) + data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule22')
                    #if available fc < demand fc i and fc is at least available for one and demandfc=1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule23')
                    #if available fc < demand fc i and fc none available then
                    else:
                        totfc=fc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] =1 # (data.loc[i,'demandfc'] - 1)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule24')
                        else:
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule25')
                elif (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] < data.loc[i,'FC_Start_Date']):
                    totfc=fc-data.loc[i-1,'demandfc']
                    #if available fc >= demand fc i
                    if (totfc >= data.loc[i,'demandfc'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule26')
                    #if available fc < demand fc i and fc is at least available for one and demandfc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*2)) +data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule27')
                    #if available fc < demand fc i and fc is at least available for one and demandfc =1then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule28')
                    #if available fc < demand fc i and fc none available then
                    else:
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] = (data.loc[i,'demandfc'] - totfc)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule29')
                        else:
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule30')
                else:# (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] < data.loc[i,'FC_Start_Date']):
                    totfc=fc-data.loc[i-2,'demandfc']
                    #if available fc >= demand fc i
                    if (totfc >= data.loc[i,'demandfc'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule31')
                    #if available fc < demand fc i and fc is at least available for one and demandfc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*2)) +data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule32')
                    #if available fc < demand fc i and fc is at least available for one and demandfc =1then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule33')
                    #if available fc < demand fc i and fc none available then
                    else:
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] =1 # (data.loc[i,'demandfc'] - 1)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule34')
                        else:
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule35')

##2###########################################
            elif  (data.loc[i,'Arrival_Date_change'] > data.loc[i,'Departure_Date']):
                data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                #if previous iteration row value is greater than current iteration row value then
                if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] <= data.loc[i-2,'FC_End_Date_change'] ) :
                    totfc=fc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
                    #if available fc > demand fc i
                    if (totfc >= data.loc[i,'demandfc']):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule36')
                    #if available fc < demand fc i and fc is at least available for one and demand fc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demandfc'] )) + data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule37')
                    #if available fc < demand fc i and fc is at least available for one and demandfc=1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule38')
                    #if available fc < demand fc i and fc none available then
                    else:
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date']=data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] =1 # (data.loc[i,'demandfc'] - 1)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule39')
                        else:
                            data.loc[i,'FC_Start_Date']=data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule40')
                elif (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] > data.loc[i-2,'FC_End_Date_change'] ) :
                    totfc=fc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
                    #if available fc > demand fc i
                    if (totfc >= data.loc[i,'demandfc']):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule41')
                    #if available fc < demand fc i and fc is at least available for one and demand fc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demandfc'] )) + data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('42')
                    #if available fc < demand fc i and fc is at least available for one and demandfc=1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule43')
                    #if available fc < demand fc i and fc none available then
                    else:
                        totfc=fc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date']=data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] =1 # (data.loc[i,'demandfc'] - 1)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule44')
                        else:
                            data.loc[i,'FC_Start_Date']=data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule45')
                elif (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] < data.loc[i,'FC_Start_Date']):
                    totfc=fc-data.loc[i-1,'demandfc']
                    #if available fc >= demand fc i
                    if (totfc >= data.loc[i,'demandfc'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule46')
                    #if available fc < demand fc i and fc is at least available for one and demandfc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*2)) +data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule47')
                    #if available fc < demand fc i and fc is at least available for one and demandfc =1then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule48')
                    #if available fc < demand fc i and fc none available then
                    else:
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date']=data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] = (data.loc[i,'demandfc'] - totfc)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule49')
                        else:
                            data.loc[i,'FC_Start_Date']=data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule50')
                else:# (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] < data.loc[i,'FC_Start_Date']):
                    totfc=fc-data.loc[i-2,'demandfc']
                    #if available fc >= demand fc i
                    if (totfc >= data.loc[i,'demandfc'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule51')
                    #if available fc < demand fc i and fc is at least available for one and demandfc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*2)) +data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule52')
                    #if available fc < demand fc i and fc is at least available for one and demandfc =1then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule53')
                    #if available fc < demand fc i and fc none available then
                    else:
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date']=data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] = (data.loc[i,'demandfc'] - totfc)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule54')
                        else:
                            data.loc[i,'FC_Start_Date']=data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule55')
########################################################################################
            else: #data.loc[i,'Arrival_Date_change'] <= data.loc[i,'Arrival_Date']
                data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date']+pd.to_timedelta(1, unit='D')
                data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                #if previous iteration row value is greater than current iteration row value then
                if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] <= data.loc[i-2,'FC_End_Date_change'] ) :
                    totfc=fc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
                    #if available fc > demand fc i
                    if (totfc >= data.loc[i,'demandfc']):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule56')
                    #if available fc < demand fc i and fc is at least available for one and demand fc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demandfc'] )) + data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule57')
                    #if available fc < demand fc i and fc is at least available for one and demandfc=1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule58')
                    #if available fc < demand fc i and fc none available then
                    else:
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] =1 # (data.loc[i,'demandfc'] - 1)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule59')
                        else:
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule60')
                elif (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] > data.loc[i-2,'FC_End_Date_change'] ) :
                    totfc=fc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
                    #if available fc > demand fc i
                    if (totfc >= data.loc[i,'demandfc']):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule61')
                    #if available fc < demand fc i and fc is at least available for one and demand fc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*data.loc[i,'demandfc'] )) + data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule62')
                    #if available fc < demand fc i and fc is at least available for one and demandfc=1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta((data.loc[i,'demanddays_new']), unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule63')
                    #if available fc < demand fc i and fc none available then
                    else:
                        totfc=fc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] =1 # (data.loc[i,'demandfc'] - 1)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule64')
                        else:
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule65')
                elif (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] < data.loc[i,'FC_Start_Date']):
                    totfc=fc-data.loc[i-1,'demandfc']
                    #if available fc >= demand fc i
                    if (totfc >= data.loc[i,'demandfc'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule66')
                    #if available fc < demand fc i and fc is at least available for one and demandfc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*2)) +data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule67')
                    #if available fc < demand fc i and fc is at least available for one and demandfc =1then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule68')
                    #if available fc < demand fc i and fc none available then
                    else:
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] = (data.loc[i,'demandfc'] - totfc)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule69')
                        else:
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule70')
                else:# (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] < data.loc[i,'FC_Start_Date']):
                    totfc=fc-data.loc[i-2,'demandfc']
                    #if available fc >= demand fc i
                    if (totfc >= data.loc[i,'demandfc'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule71')
                    #if available fc < demand fc i and fc is at least available for one and demandfc>1 then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']>1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                        #cal the number of days that available FC can start
                        data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                        #cal the remaining quantity that is already loaded by available FC
                        data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                        #cal the remaining number of FC to fulfill the demand
                        data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                        #re-cal the total demandays based on this condition
                        data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*2)) +data.loc[i,'dayrun_progress']
                        #cal the end date fc operate
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule72')
                    #if available fc < demand fc i and fc is at least available for one and demandfc =1then
                    elif (totfc < data.loc[i,'demandfc']) & (totfc >0) & (data.loc[i,'demandfc']==1):
                        #state the available FC to start operate
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'FC_Start_Date']
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Demmurage_Day'] <0:
                            data.loc[i,'Demmurage_Cost']=0
                        else:
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule73')
                    #if available fc < demand fc i and fc none available then
                    else:
                        if (data.loc[i,'demandfc']>1):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] =1 # (data.loc[i,'demandfc'] - 1)
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule74')
                        else:
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Demmurage_Day'] <0:
                                data.loc[i,'Demmurage_Cost']=0
                            else:
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demmurage_Day'] * data.loc[i,'Demurrage_Rate']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule75')
    data.loc[data.Demmurage_Day<=0 ,'Demmurage_Day']=0
    data.loc[data.Demmurage_Cost<=0 ,'Demmurage_Cost']=0
    return data