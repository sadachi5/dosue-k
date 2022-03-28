import os

# subprocess: https://www.sejuku.net/blog/65485    

command_list = [
    'python3 aho.py 1 2>&1>&aho1.out', 
    'python3 aho.py 2 2>&1>&aho2.out', 
];

for i, command in enumerate(command_list):
    if i%10!=9:
        command = command + ' &' # background job (Not wait for the end of the job)
        
    os.system(command);
    pass;