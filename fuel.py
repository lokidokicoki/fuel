#!/usr/bin/python3

import datetime
from operator import itemgetter
import json

ltr_gal_conv = 4.54609 # liters in an imperial gallon
vdat = 'vehicles.dat'
vehicles = []

rdat = 'records.dat'
records = []

sdat = 'summaries.dat'
summaries = []

svg = '''
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="800" height="600">
	<text x="400" y="25" text-anchor="middle" fill="black" stroke="none" font-weight='normal'>Fuel Economy for {0}</text>
	<line stroke="black" x1="50" y1="550" x2="750" y2="550"/><!-- xaxis 700 wide-->
	<line stroke="black" x1="50" y1="50"  x2="50"  y2="550"/><!-- yaxis 500 tall -->
    {1}
</svg>
'''

'''
Add new vehicle record
'''
def add_vehicle():
    vehicle = {'make':'', 'model':'', 'year':'', 'reg':'', 'ftc':0}
    print('Add Vehicle:')
    vehicle['make'] = input('Make:')
    vehicle['model'] = input('Model:')
    vehicle['year'] = input('Year:')
    vehicle['reg'] = input('Reg. No.:')
    vehicle['ftc'] = input('Fuel Tank Capacity (litres):')
    vehicles.append(vehicle)
    save(vdat, vehicles)
    manage_vehicles()

'''
Modify a vehicle record
'''
def modify_vehicle():
    print('Modify Vehicle:')
    num = 1

    for v in vehicles:
        print('{0}) {1}'.format(num, v['reg']))
        num +=1

    print('0) Back')
    option = int(input('Option? :'))
    if option != 0:
        vehicle = vehicles[option-1]
        if not 'ftc' in vehicle:
            vehicle['ftc']=0
        e= input('Make ({0}):'.format(vehicle['make']))
        if e:
            vehicle['make'] = e
        e = input('Model ({0}):'.format(vehicle['model']))
        if e:
            vehicle['model'] = e
        e = input('Year ({0}):'.format(vehicle['year']))
        if e:
            vehicle['year'] = e
        e = input('Reg. No. ({0}):'.format(vehicle['reg']))
        if e:
            vehicle['reg'] = e
        e = input('Fuel Tank Capacity ({0}):'.format(vehicle['ftc'] or 0))
        if e:
            vehicle['ftc'] = int(e)

        save(vdat, vehicles)

    manage_vehicles()

'''
List known vehicles
'''
def list_vehicles():
    print('List Vehicles:')
    for v in vehicles:
        print('{0} {1} {2} {3} {4} litres'.format(v['year'], v['make'], v['model'], v['reg'], v['ftc']))
    manage_vehicles()

'''
Remove vehicle from data
'''
def remove_vehicle():
    print('Remove Vehicle:')
    num = 1
    for v in vehicles:
        print('{0}) {1}'.format(num, v['reg']))
        num +=1
    print('0) Back')
    option = input('Option? :')

    # check option is numeric
    if option.isnumeric():
        option = int(option)
    else:
        remove_vehicle()

    if option != 0:
        vehicle = vehicles[option-1]
        confirm = input('Remove {0}? [y/N]:'.format(vehicle['reg'])).lower()
        if confirm == 'y':
            del vehicles[option-1]
            save(vdat, vehicles)
    manage_vehicles()

'''
Manage vehicles sub-menu
'''
def manage_vehicles():
    print('''Vehicles:
    A) Add
    E) Edit
    L) List
    R) Remove
    B) Back to Main Menu
    ''')
    option = input('Option? :')[0].upper()

    if option == 'B':
        menu()
    elif option == 'A':
        add_vehicle()
    elif option == 'E':
        modify_vehicle()
    elif option == 'R':
        remove_vehicle()
    elif option == 'L':
        list_vehicles()
    else:
        menu()

'''
Load data from file into collection
'''
def load(fname, data):
    if len(data) == 0:
        f=0
        try:
            with open(fname) as f: 
                f.close
        except IOError as e:
            print(e)
            f = open(fname, 'w')
            f.close()
            
        f = open(fname)
        for line in f:
            data.append(json.loads(line))

'''
Save data to named file
'''
def save(fname, data):
    f = open(fname, 'w')
    for v in data:
        s = json.dumps(v)
        f.write(s+'\n')
    f.close()

'''
Choose vehicle by reg
'''
def choose_vehicle():
    num = 1
    for v in vehicles:
        print('{0}) {1}'.format(num, v['reg']))
        num +=1

    option = int(input('Vehicle? :'))
    return vehicles[option-1]['reg']

'''
Get vehicle record by registration
If no vehicle with that reg, warn and call menu
'''
def get_vehicle(reg):
    vehicle = None
    for v in vehicles:
        if v['reg'] == reg:
            vehicle = v
            break
    if vehicle == None:
        print('No vehicle with that registration [{}]'.format(reg))
        menu()

    return vehicle

'''
Add new record, save to records.dat
'''
def add_record():
    record = {'date':'', 'litres':0.0, 'ppl':0.0, 'trip':0.0, 'odo':0, 'reg':'', 'notes':''}
    record['reg'] = choose_vehicle()

    # get previous recod, allows us to calculate trip
    last = last_record(record['reg'])

    print('Add Record for {}:'.format(record['reg']))
    record['date'] = input('Date (yyyy/mm/dd):')
    record['litres'] = float(input('Litres:'))
    record['ppl'] = float(input('Price per Litre:'))
    record['odo'] = int(input('Odometer:'))
    calc_trip = 0
    if last:
        record['odo'] - last['odo']
    trip = input('Trip: ({0})'.format(calc_trip))
    if trip:
        record['trip'] = float(trip)
    else:
        record['trip'] = calc_trip

    record['notes'] = input('Notes:')
    calc_mpg(record, False)
    print('MPG: {0}'.format(record['mpg']))
    records.append(record)
    save(rdat, records)
    menu()

'''
Edit chosen vehicle record.
Choose vehicle, display records by date (10 at a time?), on choice, get new values, save
'''
def edit_record():
    print('Edit Record:')
    record['reg'] = choose_vehicle()
    menu()

'''
Calculate MPG for record.
If `doSave`, then udpate records file
'''
def calc_mpg(record, doSave):
    if not 'mpg' in record:
        record['gallons'] = record['litres']/ltr_gal_conv
        record['mpg'] = record['trip']/record['gallons']

        if doSave:
            save(rdat, records)

'''
Get last record for this vehicle
'''
def last_record(reg):
    curr = None
    for record in records:
        if record['reg'] == reg:
            if curr == None:
                curr = record
            else:
                if curr['date'] < record['date']:
                    curr = record

    return curr

'''
Get summary record.
If one exists in collection return that, else, generate a new one
'''
def get_summary(reg):
    sum_rec = None
    for s in summaries:
        if s['reg'] == reg:
            sum_rec = s
            break

    if sum_rec == None:
        sum_rec = summary(reg)

    return sum_rec

'''
Create/update summary records for a vehicle
if no reg passed, prompt user to choose, calculate, save and display results
if reg passed, calculate, save and return results
'''
def summary(r=None):
    reg = None
    if r == None:
        reg = choose_vehicle()
    else:
        reg = r
    mpg={'avg':0.0, 'min':float('inf'), 'max':0.0}
    trip={'avg':0.0, 'min':float('inf'), 'max':0.0, 'total':0.0}
    ppl={'avg':0.0, 'min':float('inf'), 'max':0.0}
    sum_rec = None

    for s in summaries:
        if s['reg'] == reg:
            sum_rec = s
            break

    num=0 #number of matching records
    for record in records:
        if record['reg'] == reg:
            calc_mpg(record, True)
            num+=1
            mpg['min']=min(mpg['min'], record['mpg'])
            mpg['max']=max(mpg['max'], record['mpg'])
            mpg['avg'] += record['mpg']
            trip['min']=min(trip['min'], record['trip'])
            trip['max']=max(trip['max'], record['trip'])
            trip['total'] += record['trip']
            ppl['min']=min(ppl['min'], record['ppl'])
            ppl['max']=max(ppl['max'], record['ppl'])
            ppl['avg'] += record['ppl']

    mpg['avg'] /= num
    trip['avg'] = trip['total']/num
    ppl['avg'] /= num

    if sum_rec != None:
        sum_rec['mpg']=mpg
        sum_rec['trip']=trip
        sum_rec['ppl']=ppl
    else:
        sum_rec = {'mpg':mpg, 'trip':trip, 'ppl':ppl, 'reg':reg}
        summaries.append(sum_rec)
    
    save(sdat, summaries)

    if r == None:
        print('Summary for {0}:'.format(reg))
        print('Mpg  Min {:.2f}, Avg {:.2f}, Max {:.2f}'.format(mpg['min'], mpg['avg'], mpg['max']))
        print('Trip Min {:.1f}, Avg {:.1f}, Max {:.1f}'.format(trip['min'], trip['avg'], trip['max']))
        print('PPL  Min {:.3f}, Avg {:.3f}, Max {:.3f}'.format(ppl['min'], ppl['avg'], ppl['max']))
        print('Total miles: {:.2f}'.format(trip['total']))
   
        menu()
    else:
        return sum_rec

'''
Based on chosen vehicle's average MPG, calculate max distance travelable
'''
def predict():
    reg = choose_vehicle()
    print('Prediction for {0}'.format(reg))
    vehicle = get_vehicle(reg)
    sum_rec = get_summary(reg)

    ftcg = vehicle['ftc'] / ltr_gal_conv
    prediction = sum_rec['mpg']['avg'] * ftcg
    print('{:.2f} miles'.format(prediction))
    menu()

'''
For a vehicle, create an SVG graph showing the MPG over time.
Include average MPG.
'''
def graph():
    reg = choose_vehicle()
    vehicle = get_vehicle(reg)
    sum_rec = get_summary(reg)
    mpg_avg = sum_rec['mpg']['avg']
    #mpg_max = sum_rec['mpg']['max']
    #mpg_min = sum_rec['mpg']['min']
    mpg_min=99999999
    mpg_max = 0

    scalex = 400
    scaley = 400

    # extract records for this vehicle, store in temporary
    recs = []
    num = 0
    dmin=999999999999
    dmax=0
    drange = 0
    for r in records:
        if r['reg'] == reg:
            d=datetime.datetime.strptime(r['date'], '%Y/%m/%d')
            d = (d-datetime.datetime(1970,1,1)).total_seconds()
            r['secs'] = d
            m = r['mpg']
            dmax  =max(dmax, d)
            dmin  =min(dmin, d)
            mpg_max  =max(mpg_max, m)
            mpg_min  =min(mpg_min, m)

            recs.append(r)
            num += 1

    drange = dmax - dmin
    mpg_range = mpg_max - mpg_min
    newlist = sorted(recs, key=itemgetter('secs'))
    #print(newlist)

    inner_svg = ''

    tick_dist = scalex / num
    offset=50
    for i in range(num):
        #print(i, num)
        x = (i * tick_dist) + 50
        inner_svg += '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="grey"/>\n'.format(x, 550, x, 560)
        #inner_svg += '<text x="{}" y="{}" text-anchor="middle" font-size="8" stroke="black">{}</text>\n'.format(x, 575, recs[i]['date'])

    yscale = mpg_max
    xscale = dmax

    path = None
    x=None
    y=None
    for r in newlist:
        x=r['secs']
        y=r['mpg']

        # generate x coordinate
        x = dmax - x
        x /= drange
        x *= scalex
        x = scalex -x
        x += 50

        # generate y coordinate
        y = mpg_max - y
        y /= mpg_range
        y *= scaley
        y += 50

        inner_svg += '<circle cx="{:.2f}" cy="{:.2f}" r="3" fill="black"/>'.format(x,y)

        if path == None:
            path = 'M{:.2f},{:.2f}'
        else:
            path += ' L{:.2f},{:.2f}'
        path=path.format(x,y)

        y -= 5
        inner_svg += '<text x="{:.2f}" y="{:.2f}" text-anchor="middle" font-size="10" stroke="none" fill="black">{:.2f}</text>'.format(x,y,r['mpg'])

    inner_svg += '<path d="{}" fill="none" stroke="red" stroke-width="0.5"/>'.format(path)

    # where does the average line go?
    y = mpg_max - mpg_avg
    y /= mpg_range
    y *= scaley
    y += 50
    inner_svg += '<line x1="50" y1="{0}" x2="750" y2="{0}" stroke="grey"/>\n'.format(y)
    inner_svg += '<text x="45" y="{}" dominant-baseline="central" text-anchor="end" font-size="10" stroke="none" fill="blue">{:.2f}</text>'.format(y,mpg_avg)


    #print(inner_svg)
    svg_fname = 'mpg-{}.svg'.format(reg)
    f = open(svg_fname, 'w')
    f.write(svg.format(reg, inner_svg)+'\n')
    f.close()
    print('File at ',svg_fname)
    menu()

def menu():
    print('''\nFuel Economy
    A) Add Record
    E) Edit Record
    S) Show Summary
    P) Predict
    G) Graph
    V) Vehicles
    Q) Quit
    ''')
    option = input('Option? :')[0].upper()

    if option == 'A':
        add_record()
    elif option == 'S':
        summary()
    elif option == 'E':
        edit_record()
    elif option == 'P':
        predict()
    elif option == 'G':
        graph()
    elif option == 'V':
        manage_vehicles()
    elif option == 'Q':
        exit()
    else:
        menu()

'''
load record data
load vehicle data
show main menu
'''
def main():
    load(rdat, records)
    load(vdat, vehicles)
    load(sdat, summaries)
    menu() 

#call main
main()
