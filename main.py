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
    print ("Transferred (MB): {0:.2f} Out of: {1:.2f}".format(transferred/1e6, toBeTransferred/1e6), end='\r')
    
            
folderL3_List = []
for item in sftp.listdir('scratch/' + folderL2.value):
    if stat.S_ISDIR(sftp.lstat('scratch/' + folderL2.value + '/' + item).st_mode):
        folderL3_List = folderL3_List + [item]
folderL3_List = sorted(folderL3_List)


def aci_get(match, f2, f3List, overwrite):
    for folder3 in f3List:
        match = match
        filePathServer = ['/'.join(['scratch', f2, folder3, file]) \
                      for file in sorted(sftp.listdir('scratch/' + f2 + '/' + folder3))\
                       if match in file]
        
        folderPathMac = '/Volumes/Deneb/PF/SrTiO3Simulations/' + f2 + '/' + folder3 + '/'

        if os.path.exists(folderPathMac):
            print('Export folder exists')
        else:
            os.mkdir(folderPathMac)

        filePathMac = [folderPathMac + file.split('/')[-1] for file in filePathServer]

        for i in range(len(filePathServer)):
            print(filePathServer[i], end='\r')
            if os.path.exists(filePathMac[i]) and overwrite == False:
                print('local file exists:', filePathMac[i])
            else: 
                sftp.get(filePathServer[i], filePathMac[i], callback=printTotals)
                
# example                
aci_get("input.in", folderL2.value, folderL3_List, True)
