#!/usr/bin/python

import json

conversion = 4.54609 # liters in an imperial gallon
vdat = 'vehicles.dat'
vehicles = []

rdat = 'records.dat'
records = []

def load_vehicles():
    if len(vehicles) == 0:
        f=0
        try:
            with open(vdat) as f: 
                f.close
        except IOError as e:
            print e
            f = open(vdat, 'w')
            f.close()
            
        f = open(vdat)
        for line in f:
            vehicles.append(json.loads(line))

def add_vehicle():
    vehicle = {'make':'', 'model':'', 'year':'', 'reg':''}
    print 'Add Vehicle:'
    vehicle['make'] = raw_input('Make:')
    vehicle['model'] = raw_input('Model:')
    vehicle['year'] = raw_input('Year:')
    vehicle['reg'] = raw_input('Reg. No.:')
    vehicles.append(vehicle)
    save(vdat, vehicles)

def modify_vehicle():
    print 'Modify Vehicle:'
    num = 1
    for v in vehicles:
        print '{0}) {1}'.format(num, v['reg'])
        num +=1
    print '0) Back'
    option = int(raw_input('Option? :'))
    if option == 0:
        manage_vehicles()
    else:
        vehicle = vehicles[option-1]
        e= raw_input('Make ({0}):'.format(vehicle['make']))
        if e:
            vehicle['make'] = e
        e = raw_input('Model ({0}):'.format(vehicle['model']))
        if e:
            vehicle['model'] = e
        e = raw_input('Year ({0}):'.format(vehicle['year']))
        if e:
            vehicle['year'] = e
        e = raw_input('Reg. No. ({0}):'.format(vehicle['reg']))
        if e:
            vehicle['reg'] = e

        save(vdat, vehicles)
        manage_vehicles()

def list_vehicles():
    print 'List Vehicle:'
    for v in vehicles:
        print '{0} {1} {2} {3}'.format(v['year'], v['make'], v['model'], v['reg'])

def remove_vehicle():
    print 'Remove Vehicle:'
    num = 1
    for v in vehicles:
        print '{0}) {1}'.format(num, v['reg'])
        num +=1
    print '0) Back'
    option = int(raw_input('Option? :'))
    if option == 0:
        manage_vehicles()
    else:
        vehicle = vehicles[option-1]
        confirm = raw_input('Remove {0}? [y/n]:'.format(vehicle['reg'])).lower()
        if confirm == 'y':
            del vehicles[option-1]
            save(vdat, vehicles)
        manage_vehicles()

def manage_vehicles():
    print '''Vehicles:
    1) Add
    2) Modify
    3) Delete
    4) List
    0) Back
    '''
    option = int(raw_input('Option? :'))
    if option == 0:
        menu()
    elif option == 1:
        add_vehicle()
        manage_vehicles()
    elif option == 2:
        modify_vehicle()
        manage_vehicles()
    elif option == 3:
        remove_vehicle()
        manage_vehicles()
    elif option == 4:
        list_vehicles()
        manage_vehicles()
    else:
        menu()

def load_records():
    if len(records) == 0:
        f=0
        try:
            with open(rdat) as f: 
                f.close
        except IOError as e:
            print e
            f = open(rdat, 'w')
            f.close()
            
        f = open(rdat)
        for line in f:
            records.append(json.loads(line))

def save(fname, data):
    f = open(fname, 'w')
    for v in data:
        s = json.dumps(v)
        f.write(s+'\n')
    f.close()

def choose_vehicle():
    num = 1
    for v in vehicles:
        print '{0}) {1}'.format(num, v['reg'])
        num +=1

    option = int(raw_input('Vehicle? :'))
    return vehicles[option-1]['reg']

def add_record():
    record = {'date':'', 'litres':0.0, 'ppl':0.0, 'trip':0.0, 'odo':0, 'reg':'', 'notes':''}
    print 'Add Record:'
    record['reg'] = choose_vehicle()
    record['date'] = raw_input('Date (yyyy/mm/dd):')
    record['litres'] = float(raw_input('Litres:'))
    record['ppl'] = float(raw_input('Price per Litre:'))
    record['trip'] = float(raw_input('Trip:'))
    record['odo'] = int(raw_input('Odometer:'))
    record['notes'] = raw_input('Notes:')
    summarise(record, False)
    print 'MPG: {0}'.format(record['mpg'])
    records.append(record)
    save(rdat, records)
    menu()

def summarise(record, doSave):
    if not 'mpg' in record:
        record['gallons'] = record['litres']/conversion
        record['mpg'] = record['trip']/record['gallons']

        if doSave:
            save(rdat, records)

def summary():
    print 'Summary'
    reg = choose_vehicle()
    avgMpg=0.0
    lowMpg=float('inf')
    highMpg=0.0
    num=0 #number of mathing records
    for record in records:
        if record['reg'] == reg:
            summarise(record, True)
            num+=1
            lowMpg=min(lowMpg, record['mpg'])
            highMpg=max(highMpg, record['mpg'])
            avgMpg += record['mpg']

    avgMpg /= num

    print 'Low {:.2f} mpg, Avg {:.2f} mpg, High {:.2f} mpg'.format(lowMpg, avgMpg, highMpg)

    menu()

def menu():
    print '''Fuel Economy
    1) Add Record
    2) Show Summary
    9) Vehicles
    0) Quit
    '''
    option = int(raw_input('Option? :'))

    if option == 1:
        add_record()
    elif option == 2:
        summary()
    elif option == 9:
        manage_vehicles()
    elif option == 0:
        exit()
    else:
        menu()

'''
load record data
load vehicle data
show main menu
'''
def main():
    load_records()
    load_vehicles()
    menu() 


#call main
main()
