from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import json
from web3 import Web3, HTTPProvider
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import random
from datetime import date
from geopy.distance import geodesic

global driver, user, usertype, ip, callack, page, start, details

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Carpool.json' #carpool contract code
    deployed_contract_address = '0xac775b7bccd64d7D3cE7ab38F83ce64aFdc097Df' #hash address to access student contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getUser().call()
    if contract_type == 'ride':
        details = contract.functions.getRide().call()
    if contract_type == 'passengers':
        details = contract.functions.getPassengers().call()
    if contract_type == 'ratings':
        details = contract.functions.getRatings().call()       
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Carpool.json' #carpool contract file
    deployed_contract_address = '0xac775b7bccd64d7D3cE7ab38F83ce64aFdc097Df' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.addUser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'ride':
        details+=currentData
        msg = contract.functions.setRide(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'passengers':
        details+=currentData
        msg = contract.functions.setPassengers(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'ratings':
        details+=currentData
        msg = contract.functions.setRatings(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)    

def updateRide(currentData):
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Carpool.json' #student contract file
    deployed_contract_address = '0xac775b7bccd64d7D3cE7ab38F83ce64aFdc097Df' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    msg = contract.functions.setRide(currentData).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def updatePassenger(currentData):
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Carpool.json' #student contract file
    deployed_contract_address = '0xac775b7bccd64d7D3cE7ab38F83ce64aFdc097Df' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    msg = contract.functions.setPassengers(currentData).transact()
    tx_receipt = web3.eth.waitForTransactionReceipt(msg)    

def Ratings(request):
    if request.method == 'GET':
        output = '<tr><td><font size="" color="black">Driver&nbsp;Name</b></td><td><select name="t1">'
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[5] == 'Driver':
                output += '<option value="'+arr[0]+'">'+arr[0]+"</option>"
        output += "</select></td></tr>"
        context= {'data1':output}
        return render(request, 'Ratings.html', context)

def RatingsAction(request):
    if request.method == 'POST':
        global user
        driver = request.POST.get('t1', False)
        rating = request.POST.get('t2', False)
        data = user+"#"+driver+"#"+rating+"\n"
        saveDataBlockChain(data,"ratings")
        context= {'data':'Ratings accepted! Thank you'}
        return render(request, 'UserScreen.html', context)
    
def ShareLocationAction(request):
    if request.method == 'GET':
        global user
        rid = request.GET.get('rid', False)
        driver = request.GET.get('driver', False)
        passenger_id = 0
        readDetails("passengers")
        rows = details.split("\n")
        if len(rows) == 0:
            passenger_id = 1
        else:
            passenger_id = len(rows)
        data = str(passenger_id)+"#"+rid+"#"+driver+"#"+user+"#0#0#0#0#waiting\n"
        saveDataBlockChain(data,"passengers")    
        context= {'data':'Your request shared with driver with ID '+str(passenger_id)}
        return render(request, 'UserScreen.html', context)
        
def ViewDrivers(request):
    if request.method == 'POST':
        destination = request.POST.get('t1', False)
        latitude = request.POST.get('t2', False)
        longitude = request.POST.get('t3', False)
        driver_location = [float(latitude), float(longitude)]
        columns = ['Ride ID','Driver Name','Location Name','Latitude','Longitude','Available Seats','Ride Date','Share Location']
        output = "<table border=1 align=center>"
        font = '<font size="" color="black">'
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"
        readDetails("ride")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[7] == 'waiting':
                user_location = [float(arr[3]), float(arr[4])]
                miles = geodesic(driver_location, user_location).miles
                if miles <= 3:
                    output+='<tr><td>'+font+str(arr[0])+'</td>'
                    output+='<td>'+font+str(arr[1])+'</td>'
                    output+='<td>'+font+str(arr[2])+'</td>'
                    output+='<td>'+font+str(arr[3])+'</td>'
                    output+='<td>'+font+str(arr[4])+'</td>'
                    output+='<td>'+font+str(arr[5])+'</td>'
                    output+='<td>'+font+str(arr[6])+'</td>'
                    output+='<td><a href=\'ShareLocationAction?rid='+str(arr[0])+'&driver='+str(arr[1])+'\'><font size=3 color=black>Click Here to Share Location</font></a></td></tr>'                
        output += "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)
    

def ShareLocation(request):
    if request.method == 'GET':
       return render(request, 'ShareLocation.html', {})

def RideCompleteAction(request):
    if request.method == 'POST':
        rid = request.POST.get('t1', False)
        passenger = request.POST.get('t2', False)
        miles = request.POST.get('t3', False)
        total_amount = request.POST.get('t4', False)
        card = request.POST.get('t5', False)
        cvv = request.POST.get('t6', False)
        record = ''
        readDetails("passengers")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] != passenger and arr[1] != rid:
                record += rows[i]+"\n"
            else:
                if arr[8] == 'accepted':
                    record += arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+miles+"#"+str(total_amount)+"#"+card+"#"+cvv+"#completed\n"
                else:
                    record += rows[i]+"\n"
        updatePassenger(record)

        record = ''
        readDetails("ride")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] != rid:
                record += rows[i]+"\n"
            else:
                record += arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+arr[4]+"#"+arr[5]+"#"+arr[6]+"#completed\n"
        updateRide(record)
        context= {'data':'Total Fare : '+str(total_amount)}
        return render(request, 'DriverScreen.html', context)

def RideComplete(request):
    if request.method == 'GET':
        global driver
        output = '<tr><td><font size="" color="black">Ride&nbsp;ID</b></td><td><select name="t1">'
        readDetails("passengers")
        rows = details.split("\n")
        ride = []
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            print("===="+str(arr))
            if arr[8] == 'accepted' and arr[2] == driver:
                if str(arr[1]) not in ride:
                    ride.append(str(arr[1]))
                    output += '<option value="'+str(arr[1])+'">'+str(arr[1])+"</option>"
        output += "</select></td></tr>"
        output += '<tr><td><font size="" color="black">Passenger&nbsp;ID</b></td><td><select name="t2">'
        ride = []
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[8] == 'accepted' and arr[2] == driver:
                if str(arr[0]) not in ride:
                    ride.append(str(arr[0]))
                    output += '<option value="'+str(arr[0])+'">'+str(arr[0])+"</option>"
        output += "</select></td></tr>"        
        context= {'data1':output}
        return render(request, 'RideComplete.html', context)
        

def StartRide(request):
    if request.method == 'GET':
        context= {'data':'Ride Started'}
        return render(request, 'DriverScreen.html', context)

def DriverLocation(request):
    if request.method == 'GET':
       return render(request, 'DriverLocation.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def checkUser(username):
    flag = False
    readDetails("signup")
    rows = details.split("\n")
    for i in range(len(rows)-1):
        arr = rows[i].split("#")
        if arr[0] == username:
            flag = True
            break
    return flag

def DriverLocationAction(request):
    if request.method == 'POST':
        global driver
        location = request.POST.get('t1', False)
        latitude = request.POST.get('t2', False)
        longitude = request.POST.get('t3', False)
        seats = request.POST.get('t4', False)
        ride_id = 0
        readDetails("ride")
        rows = details.split("\n")
        if len(rows) == 0:
            ride_id = 1
        else:
            ride_id = len(rows)
        today = date.today()        
        data = str(ride_id)+"#"+driver+"#"+location+"#"+latitude+"#"+longitude+"#"+seats+"#"+str(today)+"#waiting\n"
        saveDataBlockChain(data,"ride")    
        context= {'data':'Location details added with ID '+str(ride_id)+" Passenger Requests will arrived here"}
        return render(request, 'DriverWaiting.html', context)

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('vehicle', False)
        user_type = request.POST.get('type', False)
        if checkUser(username) == False:
            data = username+"#"+password+"#"+contact+"#"+email+"#"+address+"#"+user_type+"\n"
            saveDataBlockChain(data,"signup")    
            context= {'data':'Signup Process Completed'}
            return render(request, 'Register.html', context)
        else:
            context= {'data':'Given username already exists'}
            return render(request, 'Register.html', context)

def AcceptRide(request):
    if request.method == 'GET':
        rid = request.GET.get('rid', False)
        pid = request.GET.get('pid', False)
        record = ''
        readDetails("passengers")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] != pid and arr[1] != rid:
                record += rows[i]+"\n"
            else:
                record += arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+arr[4]+"#"+arr[5]+"#"+arr[6]+"#"+arr[7]+"#accepted\n"
        updatePassenger(record)
        context= {'data':'Passenger on the way. Please wait here only'}
        return render(request, 'DriverWaiting.html', context)

def DriverWaiting(request):
    if request.method == 'GET':
        global driver
        font = '<font size="" color="black">'
        columns = ['Passenger ID','Ride ID','Driver Name','Passenger Name','Accept Ride']
        output = "<table border=1 align=center>"
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"
        readDetails("passengers")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[8] == 'waiting' and arr[2] == driver:
                output+='<tr><td>'+font+str(arr[0])+'</td>'
                output+='<td>'+font+str(arr[1])+'</td>'
                output+='<td>'+font+str(arr[2])+'</td>'
                output+='<td>'+font+str(arr[3])+'</td>'
                output+='<td><a href=\'AcceptRide?rid='+str(arr[1])+'&pid='+str(arr[0])+'\'><font size=3 color=black>Click Here to Accept</font></a></td></tr>'                
        output += "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>"
        return HttpResponse(output, content_type="text/html")


def CancelRideAction(request):
    if request.method == 'GET':
        rid = request.GET.get('rid', False)
        pid = request.GET.get('pid', False)
        record = ''
        readDetails("passengers")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] != pid and arr[1] != rid:
                record += rows[i]+"\n"
            else:
                print("*****"+arr[8])
                if arr[8] == 'accepted' or arr[8] == 'waiting':
                    record += arr[0]+"#"+arr[1]+"#"+arr[2]+"#"+arr[3]+"#"+arr[4]+"#"+arr[5]+"#"+arr[6]+"#"+arr[7]+"#cancelled 10% penalty applied\n"
                else:
                    record += rows[i]+"\n"
        print("*****"+record)
        updatePassenger(record)
        context= {'data':'Ride Cancelled 10% penalty applied'}
        return render(request, 'UserScreen.html', context)

def ViewPastRides(request):
    if request.method == 'GET':
        global user
        font = '<font size="" color="black">'
        columns = ['Passenger ID','Ride ID','Driver Name','Passenger Name','Miles Travelled', 'Amount', 'Card No', 'Cvv No', 'Status']
        output = "<table border=1 align=center>"
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"
        readDetails("passengers")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[3] == user:
                output+='<tr><td>'+font+str(arr[0])+'</td>'
                output+='<td>'+font+str(arr[1])+'</td>'
                output+='<td>'+font+str(arr[2])+'</td>'
                output+='<td>'+font+str(arr[3])+'</td>'
                output+='<td>'+font+str(arr[4])+'</td>'
                output+='<td>'+font+str(arr[5])+'</td>'
                output+='<td>'+font+str(arr[6])+'</td>'
                output+='<td>'+font+str(arr[7])+'</td>'
                output+='<td>'+font+str(arr[8])+'</td>'
        output += "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)

def CancelRide(request):
    if request.method == 'GET':
        global user
        font = '<font size="" color="black">'
        columns = ['Passenger ID','Ride ID','Driver Name','Passenger Name','Cancel Ride']
        output = "<table border=1 align=center>"
        for i in range(len(columns)):
            output += '<th>'+font+columns[i]+'</th>'
        output += "</tr>"
        readDetails("passengers")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if (arr[8] == 'waiting' or arr[8] == 'accepted') and arr[3] == user:
                output+='<tr><td>'+font+str(arr[0])+'</td>'
                output+='<td>'+font+str(arr[1])+'</td>'
                output+='<td>'+font+str(arr[2])+'</td>'
                output+='<td>'+font+str(arr[3])+'</td>'
                output+='<td><a href=\'CancelRideAction?rid='+str(arr[1])+'&pid='+str(arr[0])+'\'><font size=3 color=black>Click Here to Cancel Ride</font></a></td></tr>'                
        output += "<tr></tr><tr></tr><tr></tr><tr></tr><tr></tr>"
        context= {'data':output}
        return render(request, 'UserScreen.html', context)


def UserLogin(request):
    if request.method == 'POST':
        global ip, driver, user, usertype, callack, page
        page = None
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        status = 'none'
        readDetails("signup")
        rows = details.split("\n")
        for i in range(len(rows)-1):
            arr = rows[i].split("#")
            if arr[0] == username and arr[1] == password:
                if arr[5] == 'Driver':
                    driver = username
                    page = "DriverScreen.html"
                if arr[5] == 'Passenger':
                    user = username
                    page = "UserScreen.html"
                status = 'success'                
        if status == 'success':
            callack = request
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, page, context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)
        




        
            
