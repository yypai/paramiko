# Make sure to ssh into the aci-b first 
# I haven't figure how to resolve "keyboard interactive" failure. 
# I added an handler but got authentication error in the end.


'''
Simple script that grabs all the files with keyword in folders within a folder. 

For example, assuming working directory is folderL2, 
and folderL2 has a bunch of subfolders folderL3, and 
folder L3 has the files to be grabbed:

scratch/folderL2/folderL3/*input.in 
'''
import paramiko         #SFTP
import ipywidgets as widgets
import os
import stat             #Tell if an item is folder or file
host = ""                   
port = 22
transport = paramiko.Transport((host, port))
username = ""                      
password = ""                
transport.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(transport)

# for Jupyter Notebook
folderL2 =  widgets.Select(
            options=sorted(sftp.listdir('scratch/')),
            rows=8,
            description='Folder:',
            disabled=False, 
)
folderL2.layout.width = '600px'
display(folderL2)


def printTotals(transferred, toBeTransferred):
    print ("-----Transferred (MB): {0:.2f} Out of: {1:.2f}".format(transferred/1e6, toBeTransferred/1e6), 
           end='\r')

def aci_get(match, f2, f3List, overwrite):
    for folder3 in f3List:
        match = match
        filePathPSU = ['/'.join(['scratch', f2, folder3, file]) \
                      for file in sorted(sftp.listdir('scratch/' + f2 + '/' + folder3))\
                       if match in file]
        
        folderPathMac = '/Volumes/Arcturus/Expt/PSU/STO/' + f2 + '/' + folder3 + '/'

#        folderPathMac = '/Users/yun-yi/Desktop/' + f2 + '/' + folder3 + '/'
    
    
        if os.path.exists(folderPathMac):
            print('Folder:',  folderPathMac, ' exists.')
        else:
            os.mkdir(folderPathMac)
            print('Folder:', folderPathMac, ' created.')

        filePathMac = [folderPathMac + file.split('/')[-1] for file in filePathPSU]

        for i in range(len(filePathPSU)):
            print('-----Processing', i, 'of', len(filePathPSU), filePathPSU[i])
            if os.path.exists(filePathMac[i]) and overwrite == False:
                print('-----File:', filePathMac[i], ' exists\n')
            else: 
                sftp.get(filePathPSU[i], filePathMac[i], callback=printTotals)
                print('-----File:', filePathMac[i], ' downloaded\n')

def aci_get_last(match, f2, f3List, overwrite):
    for folder3 in f3List:
        match = match
        filePathPSU = ['/'.join(['scratch', f2, folder3, file]) \
                      for file in sorted(sftp.listdir('scratch/' + f2 + '/' + folder3))\
                       if match in file]
        
        folderPathMac = '/Volumes/Arcturus/Expt/PSU/STO/' + f2 + '/' + folder3 + '/'
#        folderPathMac = '/Users/yun-yi/Desktop/' + f2 + '/' + folder3 + '/'
        
        if os.path.exists(folderPathMac):
            print('Folder:',  folderPathMac, ' exists.')
        else:
            os.mkdir(folderPathMac)
            print('Folder:', folderPathMac, ' created.')

        filePathPSU = filePathPSU[-1:]
        filePathMac = [folderPathMac + file.split('/')[-1] for file in filePathPSU]

        
        for i in range(len(filePathPSU)):
            print('-----Processing', i, 'of', len(filePathPSU), filePathPSU[i])
            if os.path.exists(filePathMac[i]) and overwrite == False:
                print('-----File:', filePathMac[i], ' exists\n')
            else: 
                sftp.get(filePathPSU[i], filePathMac[i], callback=printTotals)
                print('-----File:', filePathMac[i], ' downloaded\n')
                
# example 1              
aci_get("input.in", folderL2.value, folderL3_List, True)


# example 2
%%time
for pattern in ["input.in", "pot.in", ".pbs", "energy_out.dat", ".o"]:
    print(pattern)
    aci_get(pattern, folderL2.value, folderL3_List, False)

for pattern in ["energy_out.dat"]:
    print(pattern)
    aci_get(pattern, folderL2.value, folderL3_List, True)

aci_get_last("OctaTilt.0", folderL2.value, folderL3_List, True)
aci_get_last("Polar", folderL2.value, folderL3_List, True)
aci_get_last("Strain", folderL2.value, folderL3_List, True)

