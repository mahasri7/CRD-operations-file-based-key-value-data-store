import json                 
import threading 
from threading import*
import time

d={} #creating dictionary


def create(key,value,timeout=0):
    if key in d:
        print("Error: this key already exists") #error message1
    else:
        if(key.isalpha()):
            if len(d)<(1024*1020*1024) and value<=(16*1024*1024): #constraints for file size less than 1GB and Jasonobject value less than 16KB 
                if timeout==0:
                    l=[value,timeout]
                else:
                    l=[value,time.time()+timeout]
                if len(key)<=32: #constraints for input key_name capped at 32chars
                    d[key]=l
                print(key+" is created in database")
            else:
                print("Error: Memory limit exceeded!! ")#error message2
        else:
            print("Error: Invalind key_name!! key_name must contain only alphabets and no special characters or numbers")#error message3
def read(key):
    if key not in d:
        print("Error: given key does not exist in database. Please enter a valid key") #error message4
    else:
        b=d[key]
        if b[1]!=0:
            if time.time()<b[1]: #comparing the present time with expiry time
                stri=str(key)+":"+str(b[0]) #to return the value in the format of JasonObject i.e.,"key_name:value"
                return stri
                print(key+" is read")
            else:
                print("Error: time-to-live of",key,"has expired") #error message5
        else:
            stri=str(key)+":"+str(b[0])
            return stri
            print(key+" is read")

#for delete operation
#use syntax "delete(key_name)"

def delete(key):
    if key not in d:
        print("Error: given key does not exist in database. Please enter a valid key") #error message4
    else:
        b=d[key]
        if b[1]!=0:
            if time.time()<b[1]: #comparing the current time with expiry time
                del d[key]
                print("key is successfully deleted")
            else:
                print("Error: time-to-live of",key,"has expired") #error message5
        else:
            del d[key]
            print("key is successfully deleted")

#I have an additional operation of modify in order to change the value of key before its expiry time if provided

#for modify operation 
#use syntax "modify(key_name,new_value)"

def modify(key,value):
    b=d[key]
    if b[1]!=0:
        if time.time()<b[1]:
            if key not in d:
                print("error: given key does not exist in database. Please enter a valid key") #error message6
            else:
                l=[]
                l.append(value)
                l.append(b[1])
                d[key]=l
        else:
            print("Error: time-to-live of",key,"has expired") #error message5
    else:
        if key not in d:
            print("Error: given key does not exist in database. Please enter a valid key") #error message6
        else:
            l=[]
            l.append(value)
            l.append(b[1])
            d[key]=l
print("Enter the data to be created:")
#create("maha",25,3600)
create(input(),int(input()),int(input()))

#to create a key with key_name,value given and with no time-to-live property


#create("src",70,3600) 
#to create a key with key_name,value given and with time-to-live property value given(number of seconds)

print("enter the key that value to be read:")
#read("maha")
read(input())
#it returns the value of the respective key in Jasonobject format 'key_name:value'


#read("src")
#it returns the value of the respective key in Jasonobject format if the TIME-TO-LIVE IS NOT EXPIRED else it returns an ERROR


#create("maha",50)
#create("pavi",200)
#it returns an ERROR since the key_name already exists in the database
#To overcome this error 
#either use modify operation to change the value of a key
#or use delete operation and recreate it

#print("Enter the key to be modified:")
#modify("maha",55)
#modify(input(),int(input()))
#it replaces the initial value of the respective key with new value 

print("Enter the key to be deleted:")
#delete("maha")
delete(input())
#it deletes the respective key and its value from the database(memory is also freed)

#we can access these using multiple threads like

t1=threading.Thread(target=(create or read or delete),args=("maha",50,3600)) #as per the operation
t1.start()
time.sleep(3)
print("Thread_1 executed")

t2=threading.Thread(target=(create or read or delete),args=("pavi",200)) #as per the operation
t2.start()
time.sleep(1)
print("Thread_2 executed")

t3=Thread(target=(create or read or delete),args=("maha",400,400))#as per the operation
t3.start()
time.sleep(2)
print("Thread_3 executed")
x=json.dumps(d) #json object is x
print(x)
