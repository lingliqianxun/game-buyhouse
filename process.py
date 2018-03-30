import win32com.client


#获取进程ID
def GetProcessId(name):
    num = 0
    wmi = win32com.client.GetObject('winmgmts:')
    for p in wmi.InstancesOf('win32_process'):
        if name in p.Name:
            num += 1
    return num


#def GetAllProcess():
    #wmi = win32com.client.GetObject('winmgmts:')
    #print(p.Name, p.Properties_('ProcessId'), \
    #    int(p.Properties_('UserModeTime').Value)+int(p.Properties_('KernelModeTime').Value))
    #children=wmi.ExecQuery('Select * from win32_process where ParentProcessId=%s' %p.Properties_('ProcessId'))
    #for child in children:
    #    print('\t',child.Name,child.Properties_('ProcessId'), \
    #        int(child.Properties_('UserModeTime').Value)+int(child.Properties_('KernelModeTime').Value))
