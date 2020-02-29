def on_button_clicked(b):
    clear_output()
    display(button)
    fc=2
    ### Create Demmuragecost Simulation Function
    def sim_demuragecost(totfc,data):
        totfc=fc
#         print(totfc)
        for i in range(1,data.shape[0]):
            if i <2:
                if ((data.loc[i,'Arrival_Date_change'] >=data.loc[i,'Arrival_Date']) & (data.loc[i,'Arrival_Date_change'] <=data.loc[i,'Departure_Date'])):
                    data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                    data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                    #if previous iteration row value is greater than current iteration row value then
                    if (data.loc[i-1,'Est_Departure_Date_change'] >= data.loc[i,'FC_Start_Date']) :
                        totfc=totfc-data.loc[i-1,'demandfc']

                        #if available fc >= demand fc i
                        if (totfc >= data.loc[i,'demandfc'] ):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'Est_Departure_Date_change']
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            
                            print(i)
                            print(totfc)
                            print('rule1')


                        #if available fc < demand fc i and fc is at least available for one then
                        elif (totfc < data.loc[i,'demandfc']) & (totfc >0)  :
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
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule2x')

                        #if available fc < demand fc i and fc none available then
                        else:
                            #the fc must start till the previous mv finisih to load
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule3')
    #                                 print( data.loc[i,'MV'])
            #                     data.loc[i,'FC_gap_Date_change'] = data.loc[i,'Departure_Date_change'] + pd.to_timedelta(1, unit='D') 
                    else:#reset to initial total fc
                        totfc = 3
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change'] + pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'Est_Departure_Date_change']
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule4')
                elif  (data.loc[i,'Arrival_Date_change'] > data.loc[i,'Departure_Date']):
                    
                    data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date_change']+pd.to_timedelta(1, unit='D')
                    data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                    #if previous iteration row value is greater than current iteration row value then
                    if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-1,'FC_End_Date_change'] < data.loc[i-2,'FC_End_Date_change']) :
#                       
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change']+pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                        data.loc[i,'FC_Start_Date'] = data.loc[i,'FC_Start_Date_change']
                        data.loc[i,'FC_End_Date'] = data.loc[i,'FC_End_Date_change'] 
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day'] = np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        data.loc[i,'Demmurage_Cost'] = data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2

                        print(i)
                        print(totfc)
                        print('ruleafterlaycan1')
                    elif (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] < data.loc[i-1,'FC_End_Date_change']) & (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_End_Date_change']):
                    
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change']+pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                        data.loc[i,'FC_Start_Date'] = data.loc[i,'FC_Start_Date_change']
                        data.loc[i,'FC_End_Date'] = data.loc[i,'FC_End_Date_change'] 
                        # Calculate Demurage cost
                        data.loc[i,'Demmurage_Day'] = np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        data.loc[i,'Demmurage_Cost'] = data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2

                        print(i)
                        print(totfc)
                        print('ruleafterlaycan2')
                    else:#reset to initial total fc
                        totfc = 3
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change'] + pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                        print(i)
                        print(totfc)
                        print('ruleafterlaycan3')
                else:
                    data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date']+pd.to_timedelta(1, unit='D')
                    data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                    #if previous iteration row value is greater than current iteration row value then
                    if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) :
                        totfc=totfc-data.loc[i-1,'demandfc']
    #                             print(totfc)
                        #if available fc >= demand fc i
                        if (totfc >= data.loc[i,'demandfc'] ):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date']+pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change']+pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule1')

                        #if available fc < demand fc i and fc is at least available for one then
                        elif (totfc < data.loc[i,'demandfc']) & (totfc >0)  :
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
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule2x')


                        #if available fc < demand fc i and fc none available then
                        else:
                            #the fc must start till the previous mv finisih to load
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule3')
    
                    else:#reset to initial total fc
                        totfc = 3
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date'] + pd.to_timedelta(1, unit='D') 
                        data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        data.loc[i,'Demmurage_Day']= np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        data.loc[i,'Demmurage_Cost']= data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule4')
            else : #i >=2

                if ((data.loc[i,'Arrival_Date_change'] >=data.loc[i,'Arrival_Date']) & (data.loc[i,'Arrival_Date_change'] <=data.loc[i,'Departure_Date'])) | (data.loc[i,'Arrival_Date_change'] >data.loc[i,'Departure_Date']):                
                    #if previous iteration row value is greater than current iteration row value then
                    totfc=fc
                    if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date'])  :

                        totfc=totfc-data.loc[i-1,'demandfc']-data.loc[i-2,'demandfc']
    #                         print(totfc)
                        #if available fc >= demand fc i
                        if (totfc >= data.loc[i,'demandfc']):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'Est_Departure_Date_change']
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule5')

                        #if available fc < demand fc i and fc is at least available for one then
                        elif (totfc < data.loc[i,'demandfc']) & (totfc >0):
                            #state the available FC to start operate
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] ))) + data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule6')
    #                                 print( data.loc[i,'MV'])
        #                     data.loc[i,'FC_gap_Date_change'] = data.loc[i,'Departure_Date_change'] + pd.to_timedelta(1, unit='D') 

                        #if available fc < demand fc i and fc none available then
                        else:
                            if (data.loc[i-2,'FC_End_Date_change'] <= data.loc[i-1,'FC_End_Date_change']):
                                data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                                data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                                #cal the number of days that available FC can start
                                data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                                #cal the remaining quantity that is already loaded by available FC
                                data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - 1)*data.loc[i,'dayrun_progress'])
                                #cal the remaining number of FC to fulfill the demand
                                data.loc[i,'demandfc_remain'] = (data.loc[i,'demandfc'] - 1)
                                #re-cal the total demandays based on this condition
                                data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'])) +data.loc[i,'dayrun_progress']
                                #cal the end date fc operate
                                # data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                                # Calculate Demurage cost
                                data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                                # Calculate Dispatch cost
                                data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                                if data.loc[i,'Dispatch_Day'] <0:
                                    data.loc[i,'Dispatch_Value']=0
                                else:
                                    data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                                print(i)
                                print(totfc)
                                print('rule7')
    #                                     print( data.loc[i,'MV'])
            #                     data.loc[i,'FC_gap_Date_change'] = data.loc[i,'Departure_Date_change'] + pd.to_timedelta(1, unit='D') 
                            else:
                                data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                                data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                                #cal the number of days that available FC can start
                                data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                                #cal the remaining quantity that is already loaded by available FC
                                data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*1*data.loc[i,'dayrun_progress'])
                                #cal the remaining number of FC to fulfill the demand
                                data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                                #re-cal the total demandays based on this condition
                                data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate'])*2) +data.loc[i,'dayrun_progress']
                                #cal the end date fc operate
                                data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                                # Calculate Demurage cost
                                data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                                # Calculate Dispatch cost
                                data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                                if data.loc[i,'Dispatch_Day'] <0:
                                    data.loc[i,'Dispatch_Value']=0
                                else:
                                    data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                                print(i)
                                print(totfc)
                                print('rule8')
    #                                     print( data.loc[i,'MV'])
                    elif (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] < data.loc[i,'FC_Start_Date']):
                        totfc=totfc-data.loc[i-1,'demandfc']
    #                             print(totfc)
                        #if available fc >= demand fc i
                        if (totfc >= data.loc[i,'demandfc'] ):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'Est_Departure_Date_change']
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule9')
    #                                 print( data.loc[i,'MV'])
                        #if available fc < demand fc i and fc is at least available for one then
                        elif (totfc < data.loc[i,'demandfc']) & (totfc >0):
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
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule10')
    #                                 print( data.loc[i,'MV'])
                        #if available fc < demand fc i and fc none available then
                        else:

                            #the fc must start till the previous mv finisih to load
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule11x')
    #                                 print( data.loc[i,'MV'])
                    else:
                        totfc=fc
    
#                         if (data.loc[i-1,'FC_End_Date_change'] < data.loc[i,'FC_End_Date_change']  & data.loc[i+1,'FC_Start_Date'] > data.loc[i,'FC_End_Date_change'] ):
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
                        data['demanddays']= np.ceil(data.Demand_Qty/data.Loading_Rate*totfc)
                        data['demandfc']=np.ceil(data['demanddays']/data.Laytime_Duration)
                        data['demanddays_new']=np.ceil(data.Demand_Qty/(data.Loading_Rate*data['demandfc']))
                        data.loc[i,'FC_End_Date_change'] =  data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule12xx')
                            
#                         else:
#                             data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date_change']+ pd.to_timedelta(1, unit='D')
#                             data.loc[i,'FC_End_Date_change'] = data.loc[i,'Est_Departure_Date_change']
#                             data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
#                             data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
#                             # Calculate Dispatch cost
#                             data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
#                             if data.loc[i,'Dispatch_Day'] <0:
#                                 data.loc[i,'Dispatch_Value']=0
#                             else:
#                                 data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
#                             print(i)
#                             print(totfc)
#                             print('rule12xx')

########################################################################################                         
                else: #data.loc[i,'Arrival_Date_change'] <= data.loc[i,'Arrival_Date'] 
                    data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date']+pd.to_timedelta(1, unit='D')
                    data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                    totfc=fc
                    print(totfc)
                    #if previous iteration row value is greater than current iteration row value then
                    if (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date'])  :
                        totfc = totfc - data.loc[i-1,'demandfc'] - data.loc[i-2,'demandfc']
                        #if available fc >= demand fc i
                        if (totfc >= data.loc[i,'demandfc']):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date']+ pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change']+pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule5')

                        #if available fc < demand fc i and fc is at least available for one then
                        elif (totfc < data.loc[i,'demandfc']) & (totfc >0):
                            #state the available FC to start operate
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date']+ pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule6')

                        #if available fc < demand fc i and fc none available then
                        else:
                            
                            if (data.loc[i-2,'FC_End_Date_change'] <= data.loc[i-1,'FC_End_Date_change']):
                                data.loc[i,'FC_Start_Date_change'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                                data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                                #cal the number of days that available FC can start
                                data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                                #cal the remaining quantity that is already loaded by available FC
                                data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - 1)*data.loc[i,'dayrun_progress'])
                                #cal the remaining number of FC to fulfill the demand
                                data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                                #re-cal the total demandays based on this condition
                                data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'])) +data.loc[i,'dayrun_progress']
                                #cal the end date fc operate
                                data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                                # Calculate Demurage cost
                                data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                                # Calculate Dispatch cost
                                data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                                if data.loc[i,'Dispatch_Day'] <0:
                                    data.loc[i,'Dispatch_Value']=0
                                else:
                                    data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                                print(i)
                                print(totfc)
                                print('rule7x')
    #                                     print( data.loc[i,'MV'])
            #                     data.loc[i,'FC_gap_Date_change'] = data.loc[i,'Departure_Date_change'] + pd.to_timedelta(1, unit='D') 
                            else:
                                data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate 1st fc
                                data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-2,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                                #cal the number of days that available FC can start
                                data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                                #cal the remaining quantity that is already loaded by available FC
                                data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - 1)*data.loc[i,'dayrun_progress'])
                                #cal the remaining number of FC to fulfill the demand
                                data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                                #re-cal the total demandays based on this condition
                                data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate'])*(data.loc[i,'demandfc'])) +data.loc[i,'dayrun_progress']
                                #cal the end date fc operate
                                data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                                # Calculate Demurage cost
                                data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                                data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                                # Calculate Dispatch cost
                                data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                                if data.loc[i,'Dispatch_Day'] <0:
                                    data.loc[i,'Dispatch_Value']=0
                                else:
                                    data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                                print(i)
                                print(totfc)
                                print('rule8')
    #                                     print( data.loc[i,'MV'])
                    elif (data.loc[i-1,'FC_End_Date_change'] >= data.loc[i,'FC_Start_Date']) & (data.loc[i-2,'FC_End_Date_change'] < data.loc[i,'FC_Start_Date']):
                        totfc=totfc-data.loc[i-1,'demandfc']
                        data.loc[i,'FC_Start_Date']=data.loc[i,'Arrival_Date']+pd.to_timedelta(1, unit='D')
                        data.loc[i,'FC_End_Date']=data.loc[i,'FC_Start_Date']+pd.to_timedelta(data.loc[i,'demanddays'], unit='D')
                        #print(totfc)
                        #if available fc >= demand fc i
                        if (totfc >= data.loc[i,'demandfc'] ):
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date'] + pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'Est_Departure_Date_change']
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule9')
    #                                 print( data.loc[i,'MV'])
                        #if available fc < demand fc i and fc is at least available for one then
                        elif (totfc < data.loc[i,'demandfc']) & (totfc >0):
                            #state the available FC to start operate
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date']+ pd.to_timedelta(1, unit='D')
                            data.loc[i,'FC_Start_Date_change_2'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') #startdate next fc
                            #cal the number of days that available FC can start
                            data.loc[i,'dayrun_progress']=np.ceil((data.loc[i,'FC_Start_Date_change_2'] - data.loc[i,'FC_Start_Date_change'])/np.timedelta64(1,'D'))
                            #cal the remaining quantity that is already loaded by available FC
                            data.loc[i,'Demand_Qty_remain']= data.loc[i,'Demand_Qty'] - (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc'] - totfc)*data.loc[i,'dayrun_progress'])
                            #cal the remaining number of FC to fulfill the demand
                            data.loc[i,'demandfc_remain'] = data.loc[i,'demandfc'] - totfc
                            #re-cal the total demandays based on this condition
                            data.loc[i,'demanddays_new']= np.ceil(data.loc[i,'Demand_Qty_remain'] / (data.loc[i,'Loading_Rate']*(data.loc[i,'demandfc']))) +data.loc[i,'dayrun_progress']
                            #cal the end date fc operate
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule10x')
                            
                        #if available fc < demand fc i and fc none available then
                        else:
                            
                            #the fc must start till the previous mv finisih to load
                            data.loc[i,'FC_Start_Date_change'] = data.loc[i-1,'FC_End_Date_change'] + pd.to_timedelta(1, unit='D') 
                            data.loc[i,'FC_End_Date_change'] = data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                            # Calculate Demurage cost
                            data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                            data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                            # Calculate Dispatch cost
                            data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                            if data.loc[i,'Dispatch_Day'] <0:
                                data.loc[i,'Dispatch_Value']=0
                            else:
                                data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                            print(i)
                            print(totfc)
                            print('rule11')
                            
                    else:
                        totfc =fc
                        data.loc[i,'FC_Start_Date_change'] = data.loc[i,'Arrival_Date']+ pd.to_timedelta(1, unit='D')
                        data['demanddays']= np.ceil(data.Demand_Qty/data.Loading_Rate*totfc)
                        data['demandfc']=np.ceil(data['demanddays']/data.Laytime_Duration)
                        data['demanddays_new']=np.ceil(data.Demand_Qty/(data.Loading_Rate*data['demandfc']))
                        data.loc[i,'FC_End_Date_change'] =  data.loc[i,'FC_Start_Date_change'] + pd.to_timedelta(data.loc[i,'demanddays_new'], unit='D')
                        data.loc[i,'Demmurage_Day']=np.ceil((data.loc[i,'FC_End_Date_change'] - data.loc[i,'FC_End_Date'])/np.timedelta64(1,'D'))
                        data.loc[i,'Demmurage_Cost']=data.loc[i,'Demurrage_Rate'] * data.loc[i,'Demmurage_Day']
                        # Calculate Dispatch cost
                        data.loc[i,'Dispatch_Day']=np.ceil((data.loc[i,'FC_End_Date'] - data.loc[i,'FC_End_Date_change'])/np.timedelta64(1,'D'))
                        if data.loc[i,'Dispatch_Day'] <0:
                            data.loc[i,'Dispatch_Value']=0
                        else:
                            data.loc[i,'Dispatch_Value']=data.loc[i,'Dispatch_Day'] * data.loc[i,'Demurrage_Rate']/2
                        print(i)
                        print(totfc)
                        print('rule12x')

                
        data.loc[data.Demmurage_Day<=0 ,'Demmurage_Day']=0
        data.loc[data.Demmurage_Cost<=0 ,'Demmurage_Cost']=0
#         data.loc[data.Demmurage_Cost<=0 ,'FC_gap_Date_change']=data.loc[data.Demmurage_Cost<=0 ,'FC_End_Date_change']
        return data