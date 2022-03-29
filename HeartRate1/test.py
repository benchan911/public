import csv
import datetime
import time
import os

def write_data(x, y, z, d, name):

    output_file = 'data/'+name+'.csv'
    
    fieldnames = ['hr', 'seconds', 'timestamp', 'process']

    if os.path.isfile(output_file):
        print("File Exist")
        print("Writing to existing file")
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writerow({'hr':x, 'seconds':y, 'timestamp':z, 'process': d})
                            
    else:
        print("File does not exist")
        print("Creating new file")
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerow({'hr':x, 'seconds':y, 'timestamp':z, 'process': d})
