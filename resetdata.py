def resetdata(b):
    clear_output()
    display(buttonreset)
    print('Data is reset already!')
    resetdata = pd.read_excel('archieves/story0'+'.xlsx', sheet_name='sample')
    resetdata.to_excel('story_0/story0'+'.xlsx',sheet_name='sample',engine='xlsxwriter',index=False)
    buttonreset
    resetdata
    return buttonreset, resetdata