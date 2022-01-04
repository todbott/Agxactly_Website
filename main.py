# -*- coding: utf-8 -*-

# ---------------------------------------- Imports FLASK and some utilities -----------------------------------------------------
from flask import request, Flask, redirect, url_for, render_template, session, Response
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, UserMixin
from passlib.hash import sha256_crypt
import datetime
from datetime import date
from pytz import timezone

import gspread

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
#from google.cloud import tasks_v2

from google.oauth2 import service_account
from google.cloud import ndb

import requests

import json

import mailjet_rest

#MAILJET_API_KEY = os.environ['MAILJET_API_KEY']
#MAILJET_API_SECRET = os.environ['MAILJET_API_SECRET']
#MAILJET_SENDER = os.environ['MAILJET_SENDER']

MAILJET_API_KEY = "no"
MAILJET_API_SECRET = "3"
MAILJET_SENDER = "to"



# spreadsheet credentials
skey_location = "online-library-app-43816975ead2.json"
scredentials = service_account.Credentials.from_service_account_file(skey_location)

# build a cloud datastore client using those spreadsheet credentials
ndbclient = ndb.Client(project="online-library-app", credentials=scredentials)


# set the scopes for the spreadsheet interactions, and create a spreadsheet client
sheetscopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
spreadsheet_credentials = service_account.Credentials.from_service_account_file(
    skey_location,
    scopes = sheetscopes
)
spreadsheet_client = gspread.authorize(spreadsheet_credentials)

# build a task Client for cloud tasks (currently unused)
#task_client = tasks_v2.CloudTasksClient()

# set the key location and scopes for drive interactions, and create a drive client
dkey_location = "online-library-app-ff559ec5ab97.json"
dcredentials = service_account.Credentials.from_service_account_file(dkey_location)
drivescopes = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive']
drive_credentials = service_account.Credentials.from_service_account_file(
    dkey_location,
    scopes = drivescopes
)
drive = build('drive', 'v3', credentials=drive_credentials)










# ---------------------------------------- Flask setup ---------------------------------------------------------------
app = Flask(__name__, static_folder='static')  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    with ndbclient.context():
        try:
            query = secureAccount.query().filter(ndb.IntegerProperty("id") == int(user_id))
            for key in query.iter(keys_only=True):
                entity = key.get() 
    
            return entity
        except:
            pass


           



# ----------------- General variables ------------------------------------------------
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
oBragaExpected = 44805







# ----------------- google datastore storage-related functions and classes ------------------------
class secureAccount(UserMixin, ndb.Model):
    id = ndb.IntegerProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    client = ndb.StringProperty()
    
def create_secure_account(username, password, c):
    one = secureAccount(
            username = username,
            password = sha256_crypt.encrypt(password),
            client = c)
    one.put()
    
class ranchReportPreferences(ndb.Model):
    email = ndb.StringProperty()
    asked = ndb.BooleanProperty()
    currentPastLost = ndb.BooleanProperty()
    lossTrend = ndb.BooleanProperty()
    fiveBestPerforming = ndb.BooleanProperty()
    fiveWorstPerforming = ndb.BooleanProperty()
    stressHealthData = ndb.BooleanProperty()
    activitiesData = ndb.BooleanProperty()
    anythingElse = ndb.StringProperty()
     
def create_ranch_report_preferences(e):
    one = ranchReportPreferences(
        id = e,
        email = e,
        asked = True,
        currentPastLost = True,
        lossTrend = True,
        fiveBestPerforming = False,
        fiveWorstPerforming = False,
        stressHealthData = False,
        activitiesData = False,
        anythingElse = "")
    one.put()
    
class lossTrend(ndb.Model):
    loss_trend = ndb.StringProperty()
    
class viewPreferences(ndb.Model):
    expectedCountW = ndb.BooleanProperty()
    actualCountW = ndb.BooleanProperty()
    totalCurrentLossW = ndb.BooleanProperty()
    flyoverNotesW = ndb.BooleanProperty()
    lossTrendW = ndb.BooleanProperty()
    lossOverTimeW = ndb.BooleanProperty()
    topFiveW = ndb.BooleanProperty()
    contributingActivitiesW = ndb.BooleanProperty()
    contributingActivitiesChartW = ndb.BooleanProperty()
    eventsPieChartW = ndb.BooleanProperty()
    eventsChartW = ndb.BooleanProperty()
    eventsOverTimeW = ndb.BooleanProperty()
    ndviAverageW = ndb.BooleanProperty()
    ndviAverageByEventW = ndb.BooleanProperty()
    ndviAveragePerDateW = ndb.BooleanProperty()
    ndviChangeW = ndb.BooleanProperty()
    ndviOverTimeW = ndb.BooleanProperty() 
    
def create_view_preferences(e):
    one = viewPreferences(
        id = e,
        expectedCountW = False,
        actualCountW = False,
        totalCurrentLossW = True,
        flyoverNotesW = False,
        lossTrendW = True,
        lossOverTimeW = True,
        topFiveW = False,
        contributingActivitiesW = False,
        contributingActivitiesChartW = False,
        eventsPieChartW = True,
        eventsChartW = True,
        eventsOverTimeW = False,
        ndviAverageW = False,
        ndviAverageByEventW = True,
        ndviAveragePerDateW = True,
        ndviChangeW = False,
        ndviOverTimeW = False)
    one.put()
    
class secureAdminAccount(UserMixin, ndb.Model):
    id = ndb.IntegerProperty()
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    
def create_secure_admin_account(username, password):
    one = secureAdminAccount(
            username = username,
            password = sha256_crypt.encrypt(password))
    one.put()
    
class chartImages(ndb.Model):
    client = ndb.StringProperty()
    eventsPieChart = ndb.TextProperty(indexed=False)
    
class comparisonCard(ndb.Model):
    client = ndb.StringProperty()
    title = ndb.StringProperty()
    text = ndb.StringProperty()
    
def create_new_comparison_card(client, title, text):
    one = comparisonCard(
        id = client + text,
        client = client,
        title = title,
        text = text)
    one.put()
    
class customerData(ndb.Model):
    Customer = ndb.StringProperty()
    DateFlown = ndb.DateProperty()
    RanchBlock = ndb.StringProperty()
    Sublot = ndb.StringProperty()
    BlockSublotConcat = ndb.StringProperty()
    LotSize  = ndb.FloatProperty()
    Crop = ndb.StringProperty()
    AcresFlown  = ndb.FloatProperty()
    PlantingMethod = ndb.StringProperty()
    WetDate = ndb.DateProperty()
    HarvestDate = ndb.DateProperty()
    Test = ndb.StringProperty()
    Event = ndb.StringProperty()
    NDVIScore  = ndb.FloatProperty()
    NDVIChange = ndb.FloatProperty()
    NDVIPercentChange = ndb.FloatProperty()
    Count = ndb.IntegerProperty()
    LossToDate = ndb.IntegerProperty()
    CropLossSinceLastCount = ndb.IntegerProperty()
    LossAsPercent = ndb.FloatProperty()
    GbsProcessed = ndb.FloatProperty()
    Notes = ndb.StringProperty()
    
def create_customer_data(cu, df, rb, sl, bsc, ls, cr, af, pm, wd, hd, te, ev, ns, nc, np, co, ltd, clsl, lap, gb, no):
    one = customerData(
        id = cu + bsc + te + str(ns) + str(co),
        Customer = cu,
        DateFlown = df,
        RanchBlock = rb,
        Sublot = sl,
        BlockSublotConcat = bsc,
        LotSize  = ls,
        Crop = cr,
        AcresFlown  = af,
        PlantingMethod = pm,
        WetDate = wd,
        HarvestDate = hd,
        Test = te,
        Event = ev,
        NDVIScore  = ns,
        NDVIChange = nc,
        NDVIPercentChange = np,
        Count = co,
        LossToDate = ltd,
        CropLossSinceLastCount = clsl,
        LossAsPercent = lap,
        GbsProcessed = gb,
        Notes = no)
    one.put()
    
class userDefinedEvent(ndb.Model):
    client = ndb.StringProperty()
    event = ndb.StringProperty()
    percent = ndb.FloatProperty()

def create_user_defined_event(c, e, p):
    one = userDefinedEvent(
        id = c + e + str(p),
        client = c,
        event = e,
        percent = float(p))
    one.put()
    
class emailNotification(ndb.Model):
    client = ndb.StringProperty()
    email = ndb.StringProperty()
    ranches = ndb.StringProperty()
    
def create_email_notification(c, e, r):
    one = emailNotification(
            id = c + e + r,
            client = c,
            email = e,
            ranches = r)
    one.put()
    
class emailAlert(ndb.Model):
    client = ndb.StringProperty()
    email = ndb.StringProperty()
    ranches = ndb.StringProperty()
    conditions = ndb.StringProperty()
    sent = ndb.StringProperty(repeated=True)
    
def create_email_alert(c, e, r, co):
    one = emailAlert(
            id = c + e + r,
            client = c,
            email = e,
            ranches = r,
            conditions = co)
    one.put()    
    
class lastUpdated(ndb.Model):
    date = ndb.StringProperty()
    
def create_last_updated(client, date):
    one = lastUpdated(
        id = client,
        date = date)
    one.put()
    
class cropsSaved(ndb.Model):
    saved = ndb.IntegerProperty()
    
class acresFlown(ndb.Model):
    acres_flown = ndb.FloatProperty()
    
class linkedInPost(ndb.Model):
    content = ndb.StringProperty()
    
def create_linkedin_post(c):
    one = linkedInPost(
        id = "rcole",
        content = c)
    one.put()
    
class targetLossPercent(ndb.Model):
    client = ndb.StringProperty()
    event = ndb.StringProperty()
    target_percent = ndb.FloatProperty()
    
def create_target_loss_percent(c, e, t):
    one = targetLossPercent(
        id = c + e,
        client = c,
        event = e,
        target_percent = t)
    one.put()
    
class loginRecord(ndb.Model):
    login_record = ndb.StringProperty(repeated=True)

def create_login_record(login_info):
    one = loginRecord(
            id = "login",
            login_record = login_info)
    one.put()

    
    
    
# ----------------- Mailjet function --------------------------------------------
def send_email(name, email, organization, role_title, size, location, checks):
    
    client = mailjet_rest.Client(
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')
    
    checksList = ""
    for c in range(0, len(checks)):
        checksList += checks[c] + ", "
        
    checksList = checksList[0:len(checksList)-2]
    body = "<p>" + name + ", with the email address " + email + " who works for " + organization + " (a company with " + size + " acres in " + location + ") in the role of " + role_title +  " sent an inquiry from the Agxactly website.  They are interested in monitoring the following items:<br><br>" + checksList
    data = {
        'Messages': [{
            "From": {
                    "Email": MAILJET_SENDER,
                    "Name": name
            },
            "To": [
                {
                    "Email": "r"
                },
                {
                    "Email": "tg"
                }                
            ],
            "Subject": "Inquiry from Agxactly website",
            "TextPart": body,
            "HTMLPart": body
        }]
    }      
    client.send.create(data=data) 
    
    # Now, we send an email to the person who inquired, saying 'Your email has been sent!'
    body_two = "<p>Thank you for your request! A team member will reach out to you within 24hrs to set up an introductory call and to get you started!</p>"
    data_two = {
        'Messages': [{
            "From": {
                    "Email": MAILJET_SENDER,
                    "Name": "Agxactly auto-reply"
            },
            "To": [
                {
                    "Email": email
                }                
            ],
            "Subject": "Contact request from the Agxactly website received!",
            "TextPart": body_two,
            "HTMLPart": body_two
        }]
    }      
    client.send.create(data=data_two) 
    
def send_ranch_report_customization_request(username, checks, additional):
    
    client = mailjet_rest.Client(
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')
    
    checksList = ""
    for c in range(0, len(checks)):
        checksList += checks[c] + ", "
        
    checksList = checksList[0:len(checksList)-2]
    body = "<p>" + username + " has asked that their ranch report be customized.  They now want to include:<br><br>" + checksList + "<br>Additional requests:<br>" + additional
    data = {
        'Messages': [{
            "From": {
                    "Email": MAILJET_SENDER,
                    "Name": "RanchReportCustomizationAlert"
            },
            "To": [
                {
                    "Email": "r"
                },
                {
                    "Email": "t"
                }                
            ],
            "Subject": "Ranch Report Customization Request",
            "TextPart": body,
            "HTMLPart": body
        }]
    }      
    client.send.create(data=data) 
    
    
    
def send_entry(guess, email, details):
    client = mailjet_rest.Client(
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')

    if (details == ""):
    
        body = "<p>Someone (not in the ag industry), with the email address " + email + " just tried to guess the number of crops in the video. \
                <p>Their guess is <b>" + str(guess) + "</b>." 
    else:
        
        body = "<p>A person who is in the ag industry, with the email address " + email + " just tried to guess the number of crops in the video. \
                <p>Their guess is <b>" + str(guess) + "</b>, and here are their job details. \
                <p>" + details
    
    data = {
        'Messages': [{
            "From": {
                    "Email": MAILJET_SENDER,
                    "Name": "Contest Guess"
            },
            "To": [
                {
                    "Email": "r"
                },
                {
                    "Email": "t"
                }                
            ],
            "Subject": "Count the crops contest guess",
            "TextPart": body,
            "HTMLPart": body
        }]
    }      
    client.send.create(data=data) 
    
def send_notification(email, name, subject, body):
    client = mailjet_rest.Client(
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET), version='v3.1')
    data = "{\"Messages\": [{  \"From\": {\"Email\": \"" + MAILJET_SENDER + "\", \"Name\": \"" + name  + "\"},\"To\": [ "
    for m in range(0, len(email)-1):
        thisEmail = "{\"Email\": \"" + email[m] + "\"},"
        
        #If this is a ranch report email (which it might not be, hence the try-catch statement)
        #we have to set the "ask" boolean to true in the ranchReportPreferences entity in the database,
        #so that next time the user logs in, they will be asked if the report suited their preferences
        with ndbclient.context():
            try:
                entity = ndb.Key(ranchReportPreferences, email[m]).get()
                entity.asked = False
                entity.put()
            except:
                pass
        
        data = data + thisEmail
    data = data[0:len(data)-1]
    data = data + " ], \"Subject\": \"" + subject + "\",\"TextPart\": \"" + body + "\",\"HTMLPart\": \"" + body + "\" }] }"
    client.send.create(data=json.loads(data)) 
    return json.loads(data)

@app.route("/emailComparison", methods=['GET', 'POST'])
def emailComparison():
    # We're actually just going to create a good email body here, then send it
    # to the function above (send_notification) to actually be sent
    
    if request.method == "POST":
        
        event = request.form['event']
        details = request.form['details']
        date = request.form['date']
        lossOrGain = request.form['lossOrGain']
        address = request.form['address']
        posOrNeg = request.form['posOrNeg']
        
        if posOrNeg == "positive":
            fluffyBody = "<h2>A method was changed, and a change in crop loss resulted</h2> \
                <p>Regarding " + event + ", a change in methodology was enacted on " + date + ", which resulted \
                in a <span style='color:green'><b>" + lossOrGain + "% decrease in crop loss</b></span>.  The details of the change are below. \
                <p>" + details
        else:
             fluffyBody = "<h2>A method was changed, and a change in crop loss resulted</h2> \
                <p>Regarding " + event + ", a change in methodology was enacted on " + date + ", which resulted \
                in a <span style='color:red'><b>" + lossOrGain + "% increase in crop loss</b></span>.  The details of the change are below. \
                <p>" + details           
        
        addresses = []
        addresses.append(address)
        addresses.append("this needs to be appended because usually the email string contains a dash at the end -")
        
        email = send_notification(addresses, "Agxactly Comparison Forwarding Service", "A method-change comparison result from Agxactly", fluffyBody)
        
    return email#('', 204)



    
    
    
    
    
    
# ----------------- general functions for working with data ------------------------    
def toDateTime(dmyyyy):
    chunks = dmyyyy.split("/")
    return datetime.date(int(chunks[2]), int(chunks[0]), int(chunks[1]))

def fromDateTime(dt):
    return "new Date(" + str(dt.year) + "," + str(dt.month-1) + "," + str(dt.day) + ")"

def dateTimeToString(dt):
    return str(dt.month) + "/" + str(dt.day) + "/" + str(dt.year)

def trimFinalChar(string):
    if len(string) == 0:
        return string
    if string[len(string)-1] == ",":
        return string[0:len(string)-1]
    else:
        return string

def weird_division(n, d):
    return n / d if d else 0

def updateDictionaryByAddition(value, dictionary, value_to_add):
    v = 0
    if value in dictionary:
        v = dictionary[value]
        v = v + value_to_add
        dictionary.update({value: v})
    else:
        dictionary.update({value: value_to_add})
    return dictionary

def getUserDefinedEventNames(client):
    
    usersEvents = []
    with ndbclient.context():
        
        # Here we get all the user-defined events
        query = userDefinedEvent.query().filter(ndb.StringProperty("client") == client)
        for key in query.iter(keys_only=True):
            entity = key.get() 
            usersEvents.append(entity.event)
            
    return usersEvents

def getUserDefinedEventPercent(client, event):
    
    with ndbclient.context():
        
        # Here we get all the user-defined events
        query = userDefinedEvent.query().filter(ndb.StringProperty("client") == client).filter(ndb.StringProperty("event") == event)
        for key in query.iter(keys_only=True):
            entity = key.get() 
            return entity.percent
            
def adjustForFictitiousEvents(client, _TotalCropsLostForPerEventCalculation, eventTotals, events):
    # We have to loop through all the custom events that the customer wants to assign,
    # and get the percent loss associated with each fictitious event.
    fictitiousEvents = getUserDefinedEventNames(client)
    totalToSubtractFromRealEvents = 0
    
    for fe in fictitiousEvents:
        # we get the fictitious loss associated with that event
        thisFictitiousLossPercent = getUserDefinedEventPercent(client, fe)
        # then turn it into a concrete number, based on the total crops lost
        thisFictitiousLossNumber = int((thisFictitiousLossPercent/100) * _TotalCropsLostForPerEventCalculation)
        # we put that number into the event totals list
        eventTotals[events.index(fe)] = thisFictitiousLossNumber
        # and add it to a variable which will keep track of the total number of crops
        # fictitiously lost, which we can then divide and subtract equally from each true loss 
        totalToSubtractFromRealEvents += thisFictitiousLossNumber
        
    # Then, we take that total number from each real event, in a distributed fashion
    totalTaken = 0
    while totalTaken < totalToSubtractFromRealEvents:
        for realEvent in range(0, 7):
            if eventTotals[realEvent] > 0:
                eventTotals[realEvent] -= 1
                totalTaken += 1
            
    return eventTotals, events
            
def sentAlready(thisString, alreadySent):
    if (thisString in alreadySent):
        return True
    return False

def buildRateOfLineChart(dictionary):
    
    rateOfLossChartData = ""
    
    for line in dictionary.items():
        rbs = line[0]
        dataPointNumbers = line[1]
        
        # First, we'll construct everything before the dataPoints field
        rateOfLossChartData = rateOfLossChartData + \
        "{ \
            type: 'line', \
            axisYType: 'secondary', \
            name: '" + rbs + "', \
            showInLegend: true, \
            markerSize: 0, \
            yValueFormatString: '##.##', \
            dataPoints: ["
                    
        # Now, let's construct the datapoints
        theseDataPoints = ""
        for x in range(0, len(dataPointNumbers)):
            theseDataPoints = theseDataPoints + \
                "{ x: " + str(x) + ", y: " + str(dataPointNumbers[x]) + "},"
        theseDataPoints = trimFinalChar(theseDataPoints) + "]"
        
        # And add the datapoints to the chart data
        rateOfLossChartData = rateOfLossChartData + theseDataPoints
        
        # And finally put a cap on the chunk
        rateOfLossChartData = rateOfLossChartData + "},"
        
    return trimFinalChar(rateOfLossChartData)
        
def swapRanchNames(name):
    
    Braga = ["Braga", "Ryan", "Eade", "Brandt", "Moranda", "Gularte", "Martin", "Manzoni", "Vinyard", "Sargenti", "Grisetti", "Vineyard", "Home"]
    Betterworld = ["Brottler", "Riana", "Eadeson", "Brandon", "Morranetti", "Guliani", "Martinson", "Manfield", "Vinson", "Southfield", "Gillasetti", "Voorhies", "Homefield"]

    for b in range(0, len(Braga)):
        if Braga[b] in name:
            return name.replace(Braga[b], Betterworld[b])
    return name


# ----------------- Here are all the functions which get and process the data for the dashboard ---------
def getEntitiesAndRanchesToView(client, startDate, endDate, ranchesToView, whichOrder, historicalDataChecked):
    
    # Variables for the UI
    _Ranches = []
    
    # We're going to make a list of dictionaries,
    # each dictionary being an entity.
    # Here is the list we'll be putting them into
    allEntities = []
    
    with ndbclient.context():
        
        # Here we get all the data from the entities
        # If 'onlyShowCurrentlyPlanted' is set to True, we skip entites where the harvest date is before today
        if historicalDataChecked == False:
            query = customerData.query().filter(ndb.DateProperty("HarvestDate") >= date.today())
        else:
            query = customerData.query().filter(ndb.DateProperty("DateFlown") >= startDate).filter(ndb.DateProperty("DateFlown") <= endDate)


        if whichOrder == "DateFlown":
            query.order(customerData.DateFlown)
        else:
            query.order(customerData.WetDate)
        for key in query.iter(keys_only=True):
            entity = key.get()
            if entity.Customer != client:
                continue 
            
            if entity.DateFlown <= startDate or entity.DateFlown >= endDate:
                continue
            
#            # If 'onlyShowCurrentlyPlanted' is set to True, we skip entites where the harvest date is before today
#            if onlyShowCurrentlyPlanted == True:
#                if entity.HarvestDate < date.today():
#                    continue
            
            # Get the ranches for the dropdown in the UI
            if entity.BlockSublotConcat not in _Ranches:
                _Ranches.append(entity.BlockSublotConcat)
            
            if "All" not in ranchesToView:
                if entity.BlockSublotConcat not in ranchesToView:
                    continue
            
            # Let's put all the bits of data into a dictionary, to make it all easier to keep track of
            entityDict = dict({})
            entityDict.update({'DateFlown': entity.DateFlown})
            entityDict.update({'RanchBlock': entity.RanchBlock})
            entityDict.update({'Sublot': entity.Sublot})
            entityDict.update({'BlockSublotConcat': entity.BlockSublotConcat})
            entityDict.update({'LotSize': entity.LotSize})
            entityDict.update({'Crop': entity.Crop})
            entityDict.update({'AcresFlown': entity.AcresFlown})
            entityDict.update({'PlantingMethod': entity.PlantingMethod})
            entityDict.update({'WetDate': entity.WetDate})
            entityDict.update({'HarvestDate': entity.HarvestDate})
            entityDict.update({'Test': entity.Test})
            entityDict.update({'Event': entity.Event})
            entityDict.update({'NDVIScore': entity.NDVIScore})
            entityDict.update({'NDVIChange': entity.NDVIChange})
            entityDict.update({'NDVIPercentChange': entity.NDVIPercentChange})
            entityDict.update({'Count': entity.Count})
            entityDict.update({'LossToDate': entity.LossToDate})
            entityDict.update({'CropLossSinceLastCount': entity.CropLossSinceLastCount})
            entityDict.update({'LossAsPercent': entity.LossAsPercent})
            entityDict.update({'GbsProcessed': entity.GbsProcessed})
            entityDict.update({'Notes': entity.Notes})
            
            
            allEntities.append(entityDict)
            
    _Ranches.sort()
            
    return allEntities, _Ranches
    
def getNotes(allEntities, client):
    
    notes = ""
    
    for entity in allEntities:

        try:
            if len(entity['Notes']) > 0:
                
                notes = notes + "<b>Note regarding " + entity['RanchBlock'] + " " + entity['Sublot'] + " on " + dateTimeToString(entity['DateFlown']) + "</b><br>" + entity['Notes'] + "<br><br>"
        except:
            print("no note")
            
    return notes

def getCountData(allEntities, client):
    
    # Variables for the 'Count' Tab
    _LandAcres = 0.0
    _AcresFlown = 0.0
    _AlreadyInAcresCount = []
    _LatestCropCount = 0
    CropCounts = dict([])
    _CropsLost = 0
    _TotalCropsLostForPerEventCalculation = 0
    _PercentMissing = 0.0
    _CountTabMainTablePackage = []
    _PackagedEventPercents = []

    events = ["Cultivation", "Planting", "Roboweeder", "Sidedress", "Weather", "Disease", "Weeding"]
    eventTotals = [0, 0, 0, 0, 0, 0, 0]
    _CropsLostPerDateFlownAndEvent = ["", "", "", "", "", "", ""]
    chartEvents = ["Cultivation", "Planting", "Roboweeder", "Sidedress", "Weather", "Disease", "Weeding"]

    # The user can now enter custom events and assign percents loss to those events
    # Here, we have to check if they have any custom events registered, and 
    # alter the length / contents of the events lists accordingly
    for ce in getUserDefinedEventNames(client):
        events.append(ce)
        eventTotals.append(0)
    
    for event in range(0, len(_CropsLostPerDateFlownAndEvent)):
        _CropsLostPerDateFlownAndEvent[event] = _CropsLostPerDateFlownAndEvent[event] + "{type: 'stackedColumn',name:'" + chartEvents[event] + "',showInLegend: true,dataPoints: ["
    
    _TopFiveRanchCropsLost = ""
    _TopFiveRanchCropsLostAsPercentOfTotal = ""
    _BottomFiveRanchCropsLost = ""
    _BottomFiveRanchCropsLostAsPercentOfTotal = ""
    topFives = dict([])
    topFivesAsPercent = dict([])
    alreadySeenThisSublot = []

    
    for entity in allEntities:

        if entity['Test'] == "Count" and entity['Count'] > 0:
            # Here we get all the data that will go into the 'Count' Tab main table

            _CountTabMainTablePackage.append(entity['DateFlown'])
            _CountTabMainTablePackage.append(entity['RanchBlock'])
            _CountTabMainTablePackage.append(entity['Sublot'])
            _CountTabMainTablePackage.append(entity['LotSize'])
            _CountTabMainTablePackage.append(entity['WetDate'])
            _CountTabMainTablePackage.append(entity['HarvestDate'])
            _CountTabMainTablePackage.append(entity['Event'])
            _CountTabMainTablePackage.append('{:,}'.format(entity['Count']))
            _CountTabMainTablePackage.append('{:,}'.format(entity['LossToDate']))
            _CountTabMainTablePackage.append('{:,}'.format(entity['CropLossSinceLastCount']))
            _CountTabMainTablePackage.append(entity['LossAsPercent'])
            
            _TotalCropsLostForPerEventCalculation += entity['CropLossSinceLastCount']
            # Just realized as of mid-October that the "Latest Crop Count" and "Crops Lost" boxes
            # on the Count tab need to tally ONLY the data from the most recent flyovers--in essence
            # ignoring all but the most recent flyover data.  This next few lines attempts to do just that.
            # We put each entity Count and CropLossSinceLastCount in a dictionary.
            # These dictionaries will automatically be updated with the latest data as we go through the loop
            # here.  Later on, we will sum the values in the dictionaries to ge the totals.
            CropCounts.update({entity['BlockSublotConcat']: entity['Count']})
        
            _AcresFlown += entity['AcresFlown']
            
            # And the data that will go into the 'Count' tab stat cards
            if (entity['BlockSublotConcat'] not in _AlreadyInAcresCount):
                _LandAcres += entity['LotSize']
                _AlreadyInAcresCount.append(entity['BlockSublotConcat'])
        
        # We also have to which events led to how much crop loss each, so we 
        # associate the crop losses with certain events here
        if entity['Event'] in events:
            eventTotals[events.index(entity['Event'])] += entity['CropLossSinceLastCount']
        
        # This is for the 'Crops lost per date flown and event' line chart at the bottom of
        # the 'Count' Tab.  It makes line coordinate data to be used in the line chart
        for event in range(0, len(_CropsLostPerDateFlownAndEvent)):
            if entity['Event'] == chartEvents[event]:
                _CropsLostPerDateFlownAndEvent[event] = _CropsLostPerDateFlownAndEvent[event] + "{x: " + fromDateTime(entity['DateFlown']) + ", y: " + str(entity['CropLossSinceLastCount']) + "},"
            else:
                _CropsLostPerDateFlownAndEvent[event] = _CropsLostPerDateFlownAndEvent[event] + "{x: " + fromDateTime(entity['DateFlown']) + ", y: 0},"
                
        # This is for the 'Top 5 Ranch crops lost' table in the 'Count' Tab.
        # It associates crop loss numbers with particular ranches and sublots.
        topFives = updateDictionaryByAddition(entity['RanchBlock'], topFives, entity['CropLossSinceLastCount'])

        # This is for the 'Top 5 Ranch crops lost as percent of total' table in the "Count" Tab.
        # It tracks how many crops should be in each ranch/block

        # Here, we remove the suffix A, B, C, D or E from the Ranch/block sublot
        # UPDATE! -- The sublots now sometimes have _(1) on the end, or something, to denote re-plants
        # so this part of the program had to be re-written (2020/12/29)
        if ("_(" in entity['BlockSublotConcat']):
            rbs = entity['BlockSublotConcat'][0:len(entity['BlockSublotConcat'])-5]
        else:
            rbs = entity['BlockSublotConcat'][0:len(entity['BlockSublotConcat'])-1]
        if entity['BlockSublotConcat'] not in alreadySeenThisSublot:
            topFivesAsPercent = updateDictionaryByAddition(rbs, topFivesAsPercent, (entity['LotSize'] * oBragaExpected))
            alreadySeenThisSublot.append(entity['BlockSublotConcat'])
   
    # Now, the entity-reading loop is over, so we just sort and 
    # package the data that we now have...
    
    # Let's get the latest crop count and crop losses from those dictionaries we made
    for k, v in CropCounts.items():
        _LatestCropCount += v

    _ExpectedCrops = int(oBragaExpected * _LandAcres)
    _CropsLost = _ExpectedCrops - _LatestCropCount
    
    # In our "topFivesAsPercent" dictionary, we currently have {ranchblock: total crops that should be there} for
    # all existing ranch blocks.  Here, we have to make a dictionary of percent losses, using this
    # dictionary as well as the topFives dictionary (which contains the total number of crops lost for each ranchblock)
    topFivesPercentized = dict({})
    for r, c in topFivesAsPercent.items():
        topFivesPercentized.update({r: (weird_division(topFives[r] ,c))*100})
    
    # The 'Count' Tab needs a bar chart of the
    # top-five crop-losing ranches (and bottom five).  This bit of the program makes the bar chart data
    # for those bar charts.
    realTops = [0, 0, 0, 0, 0]
    realBottoms = [0, 0, 0, 0, 0]
    for r, c in topFives.items():
        realTops.append(c)
        realBottoms.append(c)
    realTops.sort(reverse=True)
    realBottoms.sort(reverse=False)
    realBottomsNoZeros = [i for i in realBottoms if i != 0]
    
    realTopsForPercentized = [0, 0, 0, 0, 0]
    realBottomsForPercentized = [0.0, 0.0, 0.0, 0.0, 0.0]
    for r, c in topFivesPercentized.items():
        realTopsForPercentized.append(c)
        realBottomsForPercentized.append(c)
    realTopsForPercentized.sort(reverse=True)
    realBottomsForPercentized.sort(reverse=False)
    realBottomsForPercentizedNoZeros = [i for i in realBottomsForPercentized if i != 0]
    
    # The 'Count' Tab also needs a bar chart of the top-five (and bottom five)
    # crop-losing ranches adjusted for size, where the crops lost are not shown as numbers,
    # but as a percent of what should be there, based on the lot size
    for r, c in topFives.items():
        if c >= realTops[4] and c > 0:
            _TopFiveRanchCropsLost = _TopFiveRanchCropsLost + "{y: " + str(c) + ", label: '" + r + "'},"
    _TopFiveRanchCropsLost = trimFinalChar(_TopFiveRanchCropsLost)

    realBottomForComparison = 0
    if len(realBottomsNoZeros) >= 5:
        realBottomForComparison = realBottomsNoZeros[4]
    elif len(realBottomsNoZeros) > 0:
        realBottomForComparison = realBottomsNoZeros[len(realBottomsNoZeros)-1]
        
    for r, c in topFives.items():
        if c <= realBottomForComparison and c > 0:
            _BottomFiveRanchCropsLost = _BottomFiveRanchCropsLost + "{y: " + str(c) + ", label: '" + r + "'},"
    _BottomFiveRanchCropsLost = trimFinalChar(_BottomFiveRanchCropsLost)
    
    for r, c in topFivesPercentized.items():
       if c >= realTopsForPercentized[4] and c > 0:
           _TopFiveRanchCropsLostAsPercentOfTotal = _TopFiveRanchCropsLostAsPercentOfTotal + "{y: " + str(round(c, 2)) + ", label: '" + r + "'},"
    _TopFiveRanchCropsLostAsPercentOfTotal = trimFinalChar(_TopFiveRanchCropsLostAsPercentOfTotal)       
    
    realBottomPercentizedForComparison = 0
    if len(realBottomsForPercentizedNoZeros) >= 5:
        realBottomPercentizedForComparison = realBottomsForPercentizedNoZeros[4]
    elif len(realBottomsForPercentizedNoZeros) > 0:
        realBottomPercentizedForComparison = realBottomsForPercentizedNoZeros[len(realBottomsForPercentizedNoZeros)-1]        
    
    for r, c in topFivesPercentized.items():
       if c <= realBottomPercentizedForComparison and c > 0:
           _BottomFiveRanchCropsLostAsPercentOfTotal = _BottomFiveRanchCropsLostAsPercentOfTotal + "{y: " + str(round(c, 2)) + ", label: '" + r + "'},"
    _BottomFiveRanchCropsLostAsPercentOfTotal = trimFinalChar(_BottomFiveRanchCropsLostAsPercentOfTotal)  

    _PercentMissing = round((weird_division(float(_CropsLost), float(_ExpectedCrops)) * 100), 2)

    for event in range(0, len(_CropsLostPerDateFlownAndEvent)):
        if (event < len(_CropsLostPerDateFlownAndEvent)-1):
            _CropsLostPerDateFlownAndEvent[event] = trimFinalChar(_CropsLostPerDateFlownAndEvent[event]) + "]},"
        else:
            _CropsLostPerDateFlownAndEvent[event] = trimFinalChar(_CropsLostPerDateFlownAndEvent[event]) + "]}"
    
    CropsLostPerDateFlownAndEventString = ""
    for event in range(0, len(_CropsLostPerDateFlownAndEvent)):
        CropsLostPerDateFlownAndEventString = CropsLostPerDateFlownAndEventString + _CropsLostPerDateFlownAndEvent[event]
    
    # Put fictitious data into the events and event totals lists
    eventTotals, events = adjustForFictitiousEvents(client, _TotalCropsLostForPerEventCalculation, eventTotals, events)
        
    # Then sort them
    eventTotals, events = (list(x) for x in zip(*sorted(zip(eventTotals, events), reverse=True)))
    
    for e in range(0, len(eventTotals)):
        if _CropsLost == 0:
            thisPercent = 0.0
        else:
            thisPercent = round((weird_division(float(eventTotals[e]), float(_TotalCropsLostForPerEventCalculation)) * 100), 2)
            
        _PackagedEventPercents.append(events[e])
        _PackagedEventPercents.append(thisPercent)
    
    _LandAcres = round(_LandAcres, 2)
    _AcresFlown = round(_AcresFlown, 2)

    #'{:,}'.format(_AcresFlown), \
    
    return '{:,}'.format(_LandAcres), \
            _AcresFlown, \
            '{:,}'.format(_ExpectedCrops), \
            '{:,}'.format(_LatestCropCount), \
            '{:,}'.format(_CropsLost), \
            _PercentMissing, \
            _PackagedEventPercents, \
            _CountTabMainTablePackage, \
            CropsLostPerDateFlownAndEventString, \
            _TopFiveRanchCropsLost, \
            _TopFiveRanchCropsLostAsPercentOfTotal, \
            _BottomFiveRanchCropsLost, \
            _BottomFiveRanchCropsLostAsPercentOfTotal, \
            _CropsLost
            
def getRateOfChangeData(allEntities, client, whichChange):
    
    
    # In this function, we're going to get the percent lost on each flight,
    # for each ranch, block and sublot.  Then we can graph how quickly each ranch
    # is losing crops over time

    # All the data we need, actually, is in the main chart of the "Count" tab, which we'll get here       
    a,a,a,a,a,a,a,CountData,a,a,a,a,a,a = getCountData(allEntities, client)
    
    # In this "CountData" array, we have:
    #    0           1            2        3          4       5             6      7
    #   DateFlown   RanchBlock   Sublot   Size   WetDate   HarvestDate   Event   str-Count   
    #
    #    8                 9                          10               
    #   str-LossToDate  str-CropLossSinceLastCount   LossAsPercent
    
    # Let's go through and put all the data into a dictionary of lists, like so:
        
    # ({'Braga 15A': [100, 93.4, 90.2, 88.3], 'Braga 16B': [100, 98.4]})
    
    nestedListsForLossVisualization = dict({})
    # We can also get the percent lost on each flight FOR EACH EVENT, as well,
    # which we're going to do, as well, with the following dictionary:
    nestedListsForEventVisualization = dict({})
    
    # First, just go through and put a list containing one value (100%) as the value of each ranch block sublot
    for c in range(0, len(CountData), 11):
        
        # Uncommen this line if we actually want to see each sublot separately (for example,
        # see Braga 15A and Braga 15B separately)
        # (the chart becomes very cluttered, however)
        #rbs = CountData[c+1] + " " + CountData[c+2]
        
        # Uncomment this line if we actually want to see each block separately (for example,
        # see Braga 15 and Braga 16 separately) 
        rbs = CountData[c+1]
        
        # As it stands now, we're only showing the base ranches in the chart (Just Braga, Manzoni, etc...
        # no letters or numbers) because the chart gets too cluttered otherwise
        rbs = CountData[c+1].split(' ')[0]
        nestedListsForLossVisualization.update({rbs: [100]})
        
        event = CountData[c+6]
        nestedListsForEventVisualization.update({event: [0]})
        
    # Now, go through and get each percent loss this time, and append it to the empty lists
    # we made in the previous step
    for c in range(0, len(CountData), 11):
        rbs = CountData[c+1].split(' ')[0]
        event = CountData[c+6]
        # Loss to date x 100 / (loss # as percent)
        # this formula will give us "percent lost on this flight" data!
        losssincelast = int(CountData[c+9].replace(",", ""))
        losstodate = int(CountData[c+8].replace(",", "")) * 100
        lossaspercent = float(CountData[c+10])
        percentLostThisTime = round(weird_division(losssincelast, weird_division(losstodate, lossaspercent)) * 100, 2)
 
        previousPercent = nestedListsForLossVisualization[rbs][len(nestedListsForLossVisualization[rbs])-1]
        thisPercent = previousPercent - percentLostThisTime
        nestedListsForLossVisualization[rbs].append(thisPercent)
        
        # We also append the loss percent to the dictionary full of events
        previousPercent = nestedListsForEventVisualization[event][len(nestedListsForEventVisualization[event])-1]
        thisPercent = previousPercent + percentLostThisTime
        nestedListsForEventVisualization[event].append(thisPercent)
        
    # Now we have all the data for rate of loss in our dictionaries, let's make
    # it into a canvas JS chart!
    
    # We need to send alot of chunks like this, one for each ranch-block-sublot:
    #     {
    # 			type:"line",
    # 			axisYType: "secondary",
    # 			name: "Braga 15A",
    # 			showInLegend: true,
    # 			markerSize: 0,
    # 			yValueFormatString: "##.##",
    # 			dataPoints: [		
    # 				{ x: 0, y: 100 },
    # 				{ x: 1, y: 93.3 },
    # 				{ x: 2, y: 90.88 }
    # 			]
    # 		},
    
    if whichChange == "count":   
        return buildRateOfLineChart(nestedListsForLossVisualization)
        
    else:   
        return buildRateOfLineChart(nestedListsForEventVisualization)

def getStressOverTimeData(allEntities, client):
    
    # This is just like the function above, except it gets the 
    # percent loss/gain of the NDVI score over time,
    # and will plot it on a chart

    # All the data we need, actually, is in the main chart of the "Stress" tab, which we'll get here       
    a,a,a, StressData,a,a = getStressData(allEntities)
    
    # In this "StressData" array, we have:
    #   0            1              2      3           4 
    #   DateFlown   RanchBlock   Sublot   Event   NDVIScore
    #
    #   5                6             7
    #   up-down-flat   NDVIChange   NDVIPercentChange
    
    # Let's go through and put all the data into a dictionary of lists, like so:
        
    # ({'Braga 15A': [2, 5.6, -9.2, 8.3], 'Braga 16B': [1.4, -9.4]})
    
    nestedListsForStressVisualization = dict({})
    
    # First, we'll go through and put all the ranch blocks into the dictionary
    for s in range(0, len(StressData), 8):
        rbs = StressData[s+1]
        nestedListsForStressVisualization.update({rbs: []})
        
    # Now we go through and get the NDVI percent change per flight
    for s in range(0, len(StressData), 8):   
        rbs = StressData[s+1]
        nestedListsForStressVisualization[rbs].append(StressData[s+4])
        
    # Now we have all the data for rate of loss in our dictionaries, let's make
    # it into a canvas JS chart!
    
    # We need to send alot of chunks like this, one for each ranch-block-sublot:
    #     {
    # 			type:"spline",
    # 			axisYType: "secondary",
    # 			name: "Braga 15A",
    # 			showInLegend: true,
    # 			markerSize: 0,
    # 			yValueFormatString: "##.##",
    # 			dataPoints: [		
    # 				{ x: 0, y: 100 },
    # 				{ x: 1, y: 93.3 },
    # 				{ x: 2, y: 90.88 }
    # 			]
    # 		},
    
    stressOverTimeChartData = ""
    
    for line in nestedListsForStressVisualization.items():
        rbs = line[0]
        dataPointNumbers = line[1]
        
        # First, we'll construct everything before the dataPoints field
        stressOverTimeChartData = stressOverTimeChartData + \
        "{ \
            type: 'line', \
            axisYType: 'secondary', \
            name: '" + rbs + "', \
            showInLegend: true, \
            markerSize: 0, \
            yValueFormatString: '##.##', \
            dataPoints: ["
                    
        # Now, let's construct the datapoints
        theseDataPoints = ""
        for x in range(0, len(dataPointNumbers)):
            theseDataPoints = theseDataPoints + \
                "{ x: " + str(x) + ", y: " + str(dataPointNumbers[x]) + "},"
        theseDataPoints = trimFinalChar(theseDataPoints) + "]"
        
        # And add the datapoints to the chart data
        stressOverTimeChartData = stressOverTimeChartData + theseDataPoints
        
        # And finally put a cap on the chunk
        stressOverTimeChartData = stressOverTimeChartData + "},"
        
    stressOverTimeChartData = trimFinalChar(stressOverTimeChartData)
    
    return stressOverTimeChartData
    
def getEventAnalysisData(allEntities, client):

    # Variables for the 'Event Analysis' Tab
    _EventsAnalysisPieChart = ""
    _PackagedEventPercentsAndNumbersForEventsAnalysisTab = []
    FictitiousEvents = ""
    
    events = ["Cultivation", "Planting", "Roboweeder", "Sidedress", "Weather", "Disease", "Weeding"]
    eventTotals = [0, 0, 0, 0, 0, 0, 0]
    
    # The user can now enter custom events and assign percents loss to those events
    # Here, we have to check if they have any custom events registered, and 
    # alter the length / contents of the events lists accordingly
    for ce in getUserDefinedEventNames(client):
        events.append(ce)
        eventTotals.append(0)
        
    _TotalCropsLostForPerEventCalculation = 0
    CropCounts = dict({})
    _LatestCropCount = 0
    _LandAcres = 0
    _AlreadyInAcresCount = []
    
    
    for entity in allEntities:
            
        _TotalCropsLostForPerEventCalculation += entity['CropLossSinceLastCount']
        CropCounts.update({entity['BlockSublotConcat']: entity['Count']})
        
        # And the data that will go into the 'Count' tab stat cards
        if (entity['BlockSublotConcat'] not in _AlreadyInAcresCount):
            _LandAcres += entity['LotSize']
            _AlreadyInAcresCount.append(entity['BlockSublotConcat'])
        # We also have to which events led to how much crop loss each, so we 
        # associate the crop losses with certain events here
        if entity['Event'] in events:
            eventTotals[events.index(entity['Event'])] += entity['CropLossSinceLastCount']
        
  
    # Now, the entity-reading loop is over, so we just sort and 
    # package the data that we now have...
    
    # Put fictitious data into the events and event totals lists
    eventTotals, events = adjustForFictitiousEvents(client, _TotalCropsLostForPerEventCalculation, eventTotals, events)
        
    # Then sort them
    eventTotals, events = (list(x) for x in zip(*sorted(zip(eventTotals, events), reverse=True)))
   
    # Let's get the latest crop count and crop losses from those dictionaries we made
    for k, v in CropCounts.items():
        _LatestCropCount += v

    _ExpectedCrops = int(oBragaExpected * _LandAcres)
    _CropsLost = _ExpectedCrops - _LatestCropCount
    
    for e in range(0, len(eventTotals)):
        if _CropsLost == 0:
            thisPercent = 0.0
        else:
            thisPercent = round((weird_division(float(eventTotals[e]), float(_TotalCropsLostForPerEventCalculation)) * 100), 2)
            
        _PackagedEventPercentsAndNumbersForEventsAnalysisTab.append(events[e])
        _PackagedEventPercentsAndNumbersForEventsAnalysisTab.append('{:,}'.format(eventTotals[e]))
        _PackagedEventPercentsAndNumbersForEventsAnalysisTab.append(thisPercent)
        
        if thisPercent > 0:
            _EventsAnalysisPieChart = _EventsAnalysisPieChart + "{y: " + str(eventTotals[e]) + ", name: '" + str(events[e]) + "'},"
 
    _EventsAnalysisPieChart = trimFinalChar(_EventsAnalysisPieChart)
    
    
    
    with ndbclient.context():
        
        # Here we get all the saved comparison cards to populate the 'Comparisons' tab
        query = userDefinedEvent.query().filter(ndb.StringProperty("client") == str(client))
        for key in query.iter(keys_only=True):
            entity = key.get()
            
            FictitiousEvents = FictitiousEvents + "<div class='card'> \
	     			<div class='comparison-card'> \
				    	<div class='comparison-card-container'> \
					    	<div class='comparison-title'>" + entity.event + "</div> \
						    <div class='comparison-text'>Causes a crop loss of " + str(entity.percent) + "% of the total</div> \
    							<form action='' method='post'> \
    								<input type='hidden' id='eventTabShowing' name='tabShowing' value='EventsAnalysis'> \
    								<input type='hidden' name='typeOfPost' value='deleteEvent'> \
    								<input type='hidden' name='fictitiousEventName' value='" + entity.event + "'> \
    								<input type='hidden' name='fictitiousEventPercent' value='" + str(entity.percent) + "'> \
    								<input type='submit' class='dashboard-button' id='deleteEvent' value='Delete'> \
    							</form> \
				    	</div> \
			    	</div> \
	    		</div>" 
                
    # This here is for getting the target loss percents for each event
    # which are inputtable and alterable by the user
    targetEvents = ['cultivation', 'roboweeder', 'weeding', 'weather', 'sidedress', 'planting', 'disease']
    targetsDict = dict({})
      
    with ndbclient.context():
        for event in range(0, len(targetEvents)):
            try:
                thisKey = client + targetEvents[event]
                entity = ndb.Key(targetLossPercent, thisKey).get()
                targetsDict.update({targetEvents[event]: entity.target_percent})
            except:
                print("w")
                
     
    return _PackagedEventPercentsAndNumbersForEventsAnalysisTab, \
            _EventsAnalysisPieChart, \
            FictitiousEvents, \
            targetsDict
    
def getStressData(allEntities):
    
    # Variables for the 'Stress' Tab
    _withNDVI = 0
    _TotalNDVI = 0.0
    _NDVIAcresFlown = 0.0
    NDVIevents = ["Cultivation", "Planting", "Roboweeder", "Sidedress", "Weather", "Disease", "Weeding"]
    events = ["Cultivation", "Planting", "Roboweeder", "Sidedress", "Weather", "Disease", "Weeding"]
    NDVIeventTotals = [0, 0, 0, 0, 0, 0, 0]
    _PackagedNDVIEventAndAverage = []
    _PackagedNDVIOverallChart = []
    ndviAndDates = dict([])
    howManyNDVIScoresPerDate = dict([])
    howManyNDVIScoresPerEvent = dict({"Cultivation": 0, "Planting": 0, "Roboweeder": 0, "Sidedress": 0, "Weather": 0, "Disease": 0, "Weeding": 0})
    _AverageNDVIScorePerDate = "{type: 'spline', indexLabelFontSize: 16, dataPoints: ["
    firstNDVI = dict([])
    lastNDVI = dict([])
    NDVIChangeByRanchBlock = dict([])
    _TopFiveNDVIChanges = ""
    
    for entity in allEntities:

        # Here we get all the NDVI stats that will go into the main NDVI chart on the 'Stress' Tab
        if (entity['NDVIScore'] > 0):
            _PackagedNDVIOverallChart.append(entity['DateFlown'])
            _PackagedNDVIOverallChart.append(entity['RanchBlock'])
            _PackagedNDVIOverallChart.append(entity['Sublot'])
            _PackagedNDVIOverallChart.append(entity['Event'])
            _PackagedNDVIOverallChart.append(entity['NDVIScore'])
            if (entity['NDVIChange'] > 0):
                icon = "up"
            if (entity['NDVIChange'] < 0):
                icon = "down"
            if (entity['NDVIChange'] == 0):
                icon = "flat"
            _PackagedNDVIOverallChart.append(icon) #icon
            _PackagedNDVIOverallChart.append(entity['NDVIChange']) 
            _PackagedNDVIOverallChart.append(entity['NDVIPercentChange'])
            
            # We get the first NDVI score, which will act as a base to compare against
            if entity['RanchBlock'] not in firstNDVI:
                firstNDVI.update({entity['RanchBlock']: entity['NDVIScore']})
                
            # We get the most recent NDVI score (of course, all the NDVI scores
            # will be gotten in sequence here, but they will just be overwritten as
            # the loop continues)
            lastNDVI.update({entity['RanchBlock']: entity['NDVIScore']})

            # This is for the 'Stress' Tab, we get the total NDVI for the average, and
            # the NDVI acres flown, and finally the NDVI per event
      
            _withNDVI += 1
            _TotalNDVI += entity['NDVIScore']
            _NDVIAcresFlown += entity['AcresFlown']
            if entity['Event'] in events:
                NDVIeventTotals[NDVIevents.index(entity['Event'])] += entity['NDVIScore']
        
            # We also need the average NDVI score for each date, so here we
            # associate certain NDVI score totals with certain dates
            ndviAndDates = updateDictionaryByAddition(entity['DateFlown'], ndviAndDates, entity['NDVIScore'])
            
            # Also, because we finally need to take the average of all NDVI scores of a particular date,
            # we need to keep track of how many scores went into the figure for each date,
            # so, we store the 'Numbers of NDVI scores per date' in a different dictionary
            howManyNDVIScoresPerDate = updateDictionaryByAddition(entity['DateFlown'], howManyNDVIScoresPerDate, 1)
                
            # We also have to keep track of how many NDVI scores are associated with each event
            # so we do that here
            if entity['Event'] in howManyNDVIScoresPerEvent:
                v = howManyNDVIScoresPerEvent[entity['Event']]
                v = v + 1
                howManyNDVIScoresPerEvent.update({entity['Event']: v})
          
    # Now, the entity-reading loop is over, so we just sort and 
    # package the data that we now have...

    # Here, we create the x and y data for the line chart on the 'Stress' Tab,
    # then remove the final comma from the end of it
    for d, scoreTotal in ndviAndDates.items():
        _AverageNDVIScorePerDate = _AverageNDVIScorePerDate + "{x: " + fromDateTime(d) + ", y: " + str(weird_division(float(scoreTotal), float(howManyNDVIScoresPerDate[d]))) + "},"
    _AverageNDVIScorePerDate = trimFinalChar(_AverageNDVIScorePerDate) + "]}"


    # Here, we calculate the total NDVI change per Ranch Block by comparing the 1st NDVI
    # reading with the last, and put those values into a dictionary
    for r, s in firstNDVI.items():
        NDVIChangeByRanchBlock.update({r: (lastNDVI[r] - s)})
    # Now, we find the top five values in that dictionary
    NDVIChangeByRanchBlockOrdered = []
    for r, c in NDVIChangeByRanchBlock.items():
        NDVIChangeByRanchBlockOrdered.append(c)
    NDVIChangeByRanchBlockOrdered.sort(reverse=False)
    # Finally, we make a bar chart data string
    for r, c in NDVIChangeByRanchBlock.items():
        if c != 0:
            _TopFiveNDVIChanges = _TopFiveNDVIChanges + "{y: " + str(c) + ", label: '" + r + "'},"
    _TopFiveNDVIChanges = trimFinalChar(_TopFiveNDVIChanges)
    
    _NDVIeventTotals, NDVIevents = (list(x) for x in zip(*sorted(zip(NDVIeventTotals, NDVIevents), reverse=True)))
    
    for e in range(0, len(NDVIeventTotals)):
        _PackagedNDVIEventAndAverage.append(NDVIevents[e])
        if howManyNDVIScoresPerEvent[NDVIevents[e]] == 0:
            _PackagedNDVIEventAndAverage.append(0.0)
        else:
            _PackagedNDVIEventAndAverage.append(round(weird_division(float(NDVIeventTotals[e]), float(howManyNDVIScoresPerEvent[NDVIevents[e]])), 2))
            
    ndviAverage = round(weird_division(_TotalNDVI, _withNDVI), 2)
    _NDVIAcresFlown = round(_NDVIAcresFlown, 2)


    return ndviAverage, \
            _NDVIAcresFlown, \
            _PackagedNDVIEventAndAverage, \
            _PackagedNDVIOverallChart, \
            _AverageNDVIScorePerDate, \
            _TopFiveNDVIChanges
    
def getActivityData(allEntities):
        
    # Variables for the 'Activity' Tab
    _AcresFlownPerDateFlown = "{type: 'spline', indexLabelFontSize: 16, dataPoints: ["
    acresAndDates = dict([]) 

    for entity in allEntities:
            
        # This is for the 'Activity' Tab.  We need the acres flown on each date
        acresAndDates = updateDictionaryByAddition(entity['DateFlown'], acresAndDates, entity['AcresFlown'])
      
    # Now, the entity-reading loop is over, so we just sort and 
    # package the data that we now have...

    # Here, we make a line chart for the 'Activity' Tab,
    # then remove the final comma from the end of it
    for d, acres in acresAndDates.items():
        _AcresFlownPerDateFlown = _AcresFlownPerDateFlown + "{x: " + fromDateTime(d) + ", y: " + str(acres) + "},"
    _AcresFlownPerDateFlown = trimFinalChar(_AcresFlownPerDateFlown) + "]}"

    return _AcresFlownPerDateFlown


def getComparisonsCards(client): 
    
    ComparisonCards = ""
    
    with ndbclient.context():
        
        # Here we get all the saved comparison cards to populate the 'Comparisons' tab
        query = comparisonCard.query().filter(ndb.StringProperty("client") == str(client))
        for key in query.iter(keys_only=True):
            entity = key.get()
            
            if "Positive change" in entity.title:
                thisTitle = entity.title.replace("Positive change", "<span style='color:green'>Positive change</span>")
            else:
                thisTitle = entity.title.replace("Ineffective change", "<span style='color:orange'>Ineffective change</span>")
            
            ComparisonCards = ComparisonCards + "<div class='card'> \
	     			<div class='comparison-card'> \
				    	<div class='comparison-card-container'> \
					    	<div class='comparison-title'>" + thisTitle + "</div> \
						    <div class='comparison-text'>" + entity.text + "</div> \
                             <input type='button' class='dashboard-button' onclick=\"deleteComparison('" + entity.title + "', '" + entity.text + "')\" value='delete'> \
                        </div> \
			    	</div> \
	    		</div>"
                
    return ComparisonCards
        
    
    
def getComparisonData(client, startDate, endDate, comparisonCrop, comparisonPlantingMethod, comparisonActivity, comparisonDateOfChange, comparisonNote, allEntities, targetedRanches): 
    
    # Variables for the 'Comparisons' Tab
    _ComparisonCrop = comparisonCrop
    _ComparisonPlantingMethod = comparisonPlantingMethod
    _ComparisonEvent = comparisonActivity
    _ComparisonDateOfChange = comparisonDateOfChange
    _ComparisonLineChart = "{type: 'spline', indexLabelFontSize: 16, dataPoints: ["
    _ComparisonBarChart = ""
    _ComparisonLossesBeforeChange = []
    _ComparisonLossesAfterChange = []
    _ComparisonNote = comparisonNote
    ComparisonAnalysisMessage = ""
    ComparisonEvents = ["Cultivation", "Planting", "Roboweeder", "Sidedress", "Weeding"]
    ComparisonCards = ""
    
    targetedRanchesString = ""
    for tr in targetedRanches:
        if tr == "All":
            targetedRanchesString = "on all ranches"
            break
        else:
            targetedRanchesString = "on the " + tr.split(" ")[0] + " ranches"
            break
        
    
    with ndbclient.context():
        
        # Here we get all the saved comparison cards to populate the 'Comparisons' tab
        query = comparisonCard.query().filter(ndb.StringProperty("client") == str(client))
        for key in query.iter(keys_only=True):
            entity = key.get()
            
            if "Positive change" in entity.title:
                thisTitle = entity.title.replace("Positive change", "<span style='color:green'>Positive change</span>")
            else:
                thisTitle = entity.title.replace("Ineffective change", "<span style='color:orange'>Ineffective change</span>")
            
            ComparisonCards = ComparisonCards + "<div class='card'> \
	     			<div class='comparison-card'> \
				    	<div class='comparison-card-container'> \
					    	<div class='comparison-title'>" + thisTitle + "</div> \
						    <div class='comparison-text'>" + entity.text + "</div> \
                             <input type='button' class='dashboard-button' onclick=\"deleteComparison('" + entity.title + "', '" + entity.text + "')\" value='delete'> \
                        </div> \
			    	</div> \
	    		</div>"
        
    for entity in allEntities:
            

        if entity['Test'] == "Count" and entity['Count'] > 0:

                
            # While we're in the if entity.Test = Count section, let's get all the data
            # for the comparison tab
            
            if entity['Crop'] == _ComparisonCrop \
            and entity['Event'] == _ComparisonEvent \
            and entity['PlantingMethod'] == _ComparisonPlantingMethod:
                thisLossAsPercent = round((entity['CropLossSinceLastCount'] / (entity['LotSize'] * oBragaExpected)) * 100, 2)
                if entity['DateFlown'] < _ComparisonDateOfChange:
                   _ComparisonLossesBeforeChange.append(thisLossAsPercent)
                else:
                    _ComparisonLossesAfterChange.append(thisLossAsPercent)
                _ComparisonLineChart = _ComparisonLineChart + "{x: " + fromDateTime(entity['DateFlown']) + ", y: " + str(thisLossAsPercent) + "},"
    

    # Now, the entity-reading loop is over, so we just sort and 
    # package the data that we now have...
    
    # For the 'Comparison' Tab, let's chop off that final character
    # of the line chart we made way above,
    # and make a bar chart showing the before change / after change stats
    if len(_ComparisonLineChart) > 52:
        _ComparisonLineChart = trimFinalChar(_ComparisonLineChart) + "]}"
    else:
        _ComparisonLineChart = _ComparisonLineChart + "]}"
        
    averageLossesBeforeChange = round(weird_division(sum(_ComparisonLossesBeforeChange), len(_ComparisonLossesBeforeChange)), 2)
    averageLossesAfterChange = round(weird_division(sum(_ComparisonLossesAfterChange), len(_ComparisonLossesAfterChange)), 2)
    _ComparisonBarChart = "{y: " + str(averageLossesBeforeChange) + ", label: 'Average losses before change'}, \
                           {y: " + str(averageLossesAfterChange) + ", label: 'Average losses after change'}"
                           
    if averageLossesBeforeChange > 0 and averageLossesAfterChange > 0:
        
        if averageLossesBeforeChange < averageLossesAfterChange:
            
            ComparisonAnalysisMessage = \
                "<div class='card'> \
                    <div class='comparison-card'> \
						<div class='comparison-card-container'> \
							<div class='comparison-title'><span style='color:orange'>Ineffective change</span> re: " + _ComparisonEvent + "</div> \
							<div class='comparison-text'>" + _ComparisonNote + " (" + dateTimeToString(_ComparisonDateOfChange) + " " + targetedRanchesString + ") \
                            This resulted in a crop loss increase of " + str(abs(round(averageLossesBeforeChange - averageLossesAfterChange, 2))) + "%, \
                            when the timeframe between " + dateTimeToString(startDate) + " and " + dateTimeToString(endDate) + " was analyzed.</div> \
                            <input type='button' class='dashboard-button' onclick=\"saveComparison('Ineffective change re: " + _ComparisonEvent + "', '" + _ComparisonNote + " (" + dateTimeToString(_ComparisonDateOfChange) + " " + targetedRanchesString + "). \
                            This resulted in a crop loss increase of " + str(abs(round(averageLossesBeforeChange - averageLossesAfterChange, 2))) + "%, \
                            when the timeframe between " + dateTimeToString(startDate) + " and " + dateTimeToString(endDate) + " was analyzed.')\" value='save'> \
                            <input id='comparisonAddress' class='ComparisonDateInput' value='enter address'> \
                            <input type='button' class='dashboard-button' onclick=\"mailComparison('" + _ComparisonEvent + "', '" + _ComparisonNote + "', '" + dateTimeToString(_ComparisonDateOfChange) + " " + targetedRanchesString + "', '" + str(abs(round(averageLossesBeforeChange - averageLossesAfterChange, 2))) + "', 'negative')\" value='email this comparison'> \
                        </div> \
			    	</div> \
	    		</div> \
                <h1><center><span style='color:orange'>" \
                    + str(round(averageLossesBeforeChange - averageLossesAfterChange, 2)) \
                + "% change</span></center></h1>"
                
            
        else:
            ComparisonAnalysisMessage = \
                "<div class='card'> \
                    <div class='comparison-card'> \
						<div class='comparison-card-container'> \
							<div class='comparison-title'><span style='color:green'>Positive change</span> re: " + _ComparisonEvent + "</div> \
							<div class='comparison-text'>" + _ComparisonNote + " (" + dateTimeToString(_ComparisonDateOfChange) + " " + targetedRanchesString + ") \
                            This resulted in a crop loss decrease of " + str(round(averageLossesBeforeChange - averageLossesAfterChange, 2)) + "%, \
                            when the timeframe between " + dateTimeToString(startDate) + " and " + dateTimeToString(endDate) + " was analyzed.</div> \
                            <input type='button' class='dashboard-button' onclick=\"saveComparison('Positive change re: " + _ComparisonEvent + "', '" + _ComparisonNote + " (" + dateTimeToString(_ComparisonDateOfChange) + " " + targetedRanchesString + "). \
                            This resulted in a crop loss decrease of " + str(round(averageLossesBeforeChange - averageLossesAfterChange, 2)) + "%, \
                            when the timeframe between " + dateTimeToString(startDate) + " and " + dateTimeToString(endDate) + " was analyzed.')\" value='save'> \
                            <input id='comparisonAddress' class='ComparisonDateInput' value='enter address'> \
                            <input type='button' class='dashboard-button' onclick=\"mailComparison('" + _ComparisonEvent + "', '" + _ComparisonNote + "', '" + dateTimeToString(_ComparisonDateOfChange) + " " + targetedRanchesString + "', '" + str(abs(round(averageLossesBeforeChange - averageLossesAfterChange, 2))) + "', 'positive')\" value='email this comparison'> \
                        </div> \
			    	</div> \
	    		</div> \
                <h1><center><span style='color:green'>" \
                    + str(round(averageLossesBeforeChange - averageLossesAfterChange, 2)) \
                + "% <br>positive change!</span></center></h1>"

    
    else:
        
        if comparisonCrop != "":
        
            ComparisonAnalysisMessage = \
                "<div class='card'> \
                    <div class='comparison-card'> \
    					<div class='comparison-card-container'> \
    						<div class='comparison-title'><span style='color:red'>Insufficient data for this date range</span> re: " + _ComparisonEvent + "</div> \
    						<div class='comparison-text'>There is no crop count data either after or before the date of method change.  Please choose a wider date range and try again.</div> \
                        </div> \
    			   	</div> \
    	    	</div>"                          
    
    return _ComparisonLineChart, \
            _ComparisonBarChart, \
            ComparisonAnalysisMessage, \
            _ComparisonNote, \
            ComparisonEvents, \
            ComparisonCards
    
def getPlanningData():
    
    patchesAndInfo = [["Martin 15B", [199, 385, 150, 347, 218, 220, 255, 220, 388, 322, 349, 383], "#FFF000", "rgba( 88, 214, 141, 0.5)", 238, 291, "mft", "broccoliButton", "Broccoli"], ["Manzoni 12A", [267, 182, 287, 123, 405, 182, 448, 231, 400, 304, 352, 239], "#FFF000", "rgba( 244, 208, 63, 0.5)", 333, 170, "mst", "cornButton", "Corn"]]
                       
    return patchesAndInfo

@app.route('/getEventTimingData', methods=['GET', 'POST'])
def getEventTimingData():
    
    # This function will get the percent crop losses associated with each event,
    # also taking note of how long after the wet date the event happened.
    # It is hoped that a correlation will become apparent, for example
    # "The best time to do cultivation is from 36 to 40 days after the wet date, 
    # because that is when crop losses associated with cultivation have been the lowest"
    
    # Basically, what we want is a chart for each event (except those not able to be influenced by humans
    # such as weather and disease), showing the crop losses on the y axis and the "days since wet date" on the 
    # x axis
    
    if request.method == 'POST':
        
        client = request.form['client']
        windowStart = request.form['windowStart']
        windowEnd = request.form['windowEnd']
        eventForTiming = request.form['eventForTiming']
        ranch = request.form['ranch']
        
        startDate = datetime.date(2020, 7, 1)
        endDate = date.today()

        gottenEntities, ranches_for_ui = getEntitiesAndRanchesToView(client, startDate, endDate, ['All'], "WetDate", True)
        # All the data we need, actually, is in the main chart of the "Count" tab, which we'll get here       
        a,a,a,a,a,a,a,CountData,a,a,a,a,a,a = getCountData(gottenEntities, client)
    
        # In this "CountData" array, we have:
        #    0           1            2        3          4       5             6      7
        #   DateFlown   RanchBlock   Sublot   Size   WetDate   HarvestDate   Event   str-Count   
        #
        #    8                 9                          10               
        #   str-LossToDate  str-CropLossSinceLastCount   LossAsPercent
    
        thisTimingChart = "{type: 'spline', indexLabelFontSize: 16, dataPoints: ["
        thisPacket = []
        

        days = [0]
        percents = [0]

        
        debug = ""
        
        for c in range(0, len(CountData), 11):
            
            # We have to get the wet date of the ranch the user wants to receive
            # a timing suggestion about, so let's do that here
            rbs = CountData[c+1] + CountData[c+2]
            if (rbs == ranch):
                wetDateOfRanchOfInterest = CountData[c+4]
            
            if (CountData[c+6] == eventForTiming):
            
                daysSinceWetDate = (CountData[c] - CountData[c+4]).days
                days.append(daysSinceWetDate)
                
                losssincelast = int(CountData[c+9].replace(",", ""))
                losstodate = int(CountData[c+8].replace(",", "")) * 100
                lossaspercent = float(CountData[c+10])
                percentLostThisTime = round(weird_division(losssincelast, weird_division(losstodate, lossaspercent)) * 100, 2)
                percents.append(percentLostThisTime)
                
                
        # Order the days since wet date (x values) and associated percent losses
        # by days since wet date (sort 2 lists)
        days, percents = (list(x) for x in zip(*sorted(zip(days, percents), reverse=True)))


        # The user wants to carry out some event on the ranch of interest within
        # the time window.  How many days after wet date will that time window be, for that particular
        # ranch?
        windowStartDay = (toDateTime(windowStart) - wetDateOfRanchOfInterest).days
        windowEndDay = (toDateTime(windowEnd) - wetDateOfRanchOfInterest).days
        
        for d in range(1, len(days)):
            
       
            # Now we have the days and percents loss at the next datapoint in lists, but the unfortunate thing is that
            # there may be a huge gap between the two days since wet dates.
            # We have to "fluff up" the chart here, by filling in the data for the missing
            # spans of days
            
            # How many days do we need to fill in?
            fluffPeriod = days[d-1] - days[d]
            debug += "The fluff period is " + str(fluffPeriod) + "<br>"
           
            # What vertical span do we have to cover in this fluff?
            fluffVerticalSpan = percents[d-1] - percents[d]
            debug += "The vertical span is " + str(fluffVerticalSpan) + "<br>"
            
            # This is the increment we'll have to either increase or decrease
            # the y-axis line at each "fake" step of fluffing
            fluffIncrement = weird_division(fluffVerticalSpan, fluffPeriod)
            debug += "The fluff increment is " + str(fluffIncrement) + "<br>"
            
            fluffStep = 1
                
            # Which day are we really at?
            baseDay = days[d]
            debug += "The base day is " + str(baseDay) + "<br>"
            debug += "<br>"
 
            for x in range(baseDay, fluffPeriod + baseDay):

                # If the day is wihin the window of days for the ranch in question, append it to the chart
                if (x >= windowStartDay) and (x <= windowEndDay):
                    
                    thisTimingChart = thisTimingChart + "{x: " + fromDateTime(toDateTime(windowStart) + datetime.timedelta(days = x)) + ", y: " + str(round((fluffIncrement * fluffStep) + percents[d], 2)) + "},"
                    
                fluffStep += 1
                       
                
        # Here we just package the return chart for the GUI
        if (len(thisTimingChart) > 55):
            thisTimingChart = trimFinalChar(thisTimingChart) + "]}"
                    
            thisPacket.append([eventForTiming, ranch, thisTimingChart])    
        
        return render_template('timingSuggestion.html', thisPacket = thisPacket, debug = debug)

def getNotificationsData(client):
    
    Notifications = ""
    
    with ndbclient.context():
        query = emailNotification.query().filter(ndb.StringProperty("client") == str(client))
        for key in query.iter(keys_only=True):
            entity = key.get()
            
            Notifications = Notifications + "<div class='card'> \
    	     			<div class='notification-card'> \
    				    	<div class='notification-card-container'> \
    					    	<div class='notification-title'><span style='color:OrangeRed'><b>Recipients:</b></span> " + entity.email + "</div> \
    						    <div class='notification-text'><span style='color:OrangeRed'><b>Ranches included in report:</b></span> " + entity.ranches + "</div> \
                             <input type='button' class='dashboard-button' onclick=\"deleteNotification('" + entity.ranches + "', '" + entity.email + "')\" value='delete'> \
                        </div> \
    			    	</div> \
    	    		</div>"
    return Notifications

def getAlertsData(client):
    
    Alerts = ""
    
    with ndbclient.context():
        query = emailAlert.query().filter(ndb.StringProperty("client") == str(client))
        for key in query.iter(keys_only=True):
            entity = key.get()
            
            Alerts = Alerts + "<div class='card'> \
	     			<div class='alert-card'> \
				    	<div class='alert-card-container'> \
					    	<div class='alert-title'><span style='color:#bd4271'><b>Recipients:</b></span> " + entity.email + "</div> \
						    <div class='alert-text'><span style='color:#bd4271'><b>Ranches included in alert:</b></span> " + entity.ranches + "</div> \
                            <div class='alert-text'><span style='color:#bd4271'><b>Condition(s):</b></span> " + entity.conditions + "</div> \
                             <input type='button' class='dashboard-button' onclick=\"deleteAlert('" + entity.ranches + "', '" + entity.email + "')\" value='delete'> \
                        </div> \
			    	</div> \
	    		</div>"
    return Alerts




















# -------------- Here are some functions related to robots and https protocols ------------------------
@app.before_request
def force_https():
    if request.endpoint in app.view_functions and request.headers.get('X-Forwarded-Proto', None) == 'http':
        return redirect(request.url.replace('http://', 'https://'))
    
@app.route("/robots.txt")
def robots_dot_txt():
    return "User-agent: *\nDisallow:"








# ----------- Here are functions related to analyzing images and updating the database from the spreadsheet ---
# ----------- This is an endpoint that the user can interact with to start a plant count
#@app.route("/analyze/<client>", methods=['GET', 'POST'])
#def analyze(client):
#    
#    count = None
#    _Ranches = []
#    
#    if request.method == "GET":
#                
#        with ndbclient.context():
#            
#            # Here we get all the data from the entities
#            query = customerData.query()
#            query.order(customerData.DateFlown)
#            for key in query.iter(keys_only=True):
#                entity = key.get()
#                if entity.Customer != client:
#                    continue
#                
#                # Get the ranches for the dropdown in the UI
#                if entity.BlockSublotConcat not in _Ranches:
#                    _Ranches.append(entity.BlockSublotConcat)
#                    
#        return render_template('analyze.html', ranchesForSelection = _Ranches, result = count)
#    
#    if request.method == "POST":     
#                
#        with ndbclient.context():
#            
#            # Here we get all the data from the entities
#            query = customerData.query()
#            query.order(customerData.DateFlown)
#            for key in query.iter(keys_only=True):
#                entity = key.get()
#                if entity.Customer != client:
#                    continue
#                
#                # Get the ranches for the dropdown in the UI
#                if entity.BlockSublotConcat not in _Ranches:
#                    _Ranches.append(entity.BlockSublotConcat)
#                    
#        flyoverDate = request.form['flyoverDate']
#
#        chosenRanchList = request.form.getlist('rtv[]')
#        try:
#            chosenRanch = chosenRanchList[0]
#        except:
#            chosenRanch = request.form['rbs']
#            
#        # The ranch name and number and letter are all one string,
#        # at this point, so let's break them up
#        ranch = chosenRanch.split(' ')[0]
#        blockSublot = chosenRanch.split(' ')[1]
#        if len(blockSublot) == 2:
#            block = blockSublot[0:1]
#            sublot = blockSublot[1:2]
#        else:
#            block = blockSublot[0:2]
#            sublot = blockSublot[2:3]
#            
#        ranchBlock = ranch + " " + block
#        
#        # In a few seconds, the EC2 instance will be started, and it will
#        # look in the Braga sheet RecentCounts tab for a new row
#        # with an empty count cell.  Therefore, before we start the function,
#        # we have to make that new row with an empty count cell.
#        bookString = "AOC - " + client + " O Broccoli - May to Dec 2020"
#        book = spreadsheet_client.open(bookString)
#        sheet = book.worksheet("RecentCounts")
#        dataToUpdate = sheet.get_all_values()        
#
#        sheet.update_cell(len(dataToUpdate)+1, 1, flyoverDate) 
#        sheet.update_cell(len(dataToUpdate)+1, 2, ranchBlock) 
#        sheet.update_cell(len(dataToUpdate)+1, 3, sublot) 
#        
#        # This starts the lambda cloud function, which in turn starts the Amazon EC2 instance to count the crops!
#        requests.post("https://4vlpm27tvk.execute-api.us-east-1.amazonaws.com/default/agxactly-count-trigger")
#
#        # Inform the user that the count has been started!
#        count = "The count has been started.  It may take tens of minutes or hours, depending on the number of images.  The spreadsheet will be updated when the count is complete."

        
        # --------- THIS IS leftover code from when I was using a 
        # ---------- Cloud Function to count.  Have since switched to an AWS
        # ------------ EC2 instance! --
        # -----------------------------
        
        # Here we go, we will stitch the image and analyze it in 500-pixel tall
        # sections using a cloud function
                
        # Send this dictionary, telling the cloud function 'This is a stitch request' (the other dictionary 
        # entries are required to allow the function to save the resulting stitched *.jpg
        # segments with the correct filenames
        #dictToSend = ({'type': 'stitch', 'flyoverDate': flyoverDate, 'ranchBlock': ranchBlock, 'sublot': sublot, 'fileName': "no-name", 'rowToMoveTo': "0"})
        
        # The cloud function will access the "flyoverImages" folder in
        # Google Drive, and crop all the images
        # it finds there so that they have no vertically overlapping sections.
        # Then, it will save those images 
        # in Google Cloud Storage, in a specific folder.  
        # The function returns a dictionary which is necessary for the next
        # iteration of the loop.
        # This loop actually starts all functions at the same time, to avoid timeouts.
        #jsonNamesAndImages = requests.post('https://us-central1-online-library-app.cloudfunctions.net/countBroccoli', json=dictToSend)


        # Now, we parse the json payload
        #namesAndImages = jsonNamesAndImages.json()
        
        #for image, imageName in namesAndImages.items():
            
            # If there were no images found, the cloud function inputs the value 'no-rows'
            # with the key 'Row 1' in the dictionary.
            # If this key value pair is found, update the 'count' message and
            # break out of the loop
        #    if imageName == "No images":
        #        count = "There seem to have been no files to process in the Google Drive Row folders."
        #        return render_template('analyze.html', ranchesForSelection = _Ranches, result = count)

        # This is very hacky, but here's the sytem:
        # The cloud function which is triggered in this loop is great, but
        # if you feed it more than about 30 sections of image to analyze, it starts
        # to timeout, thus not returning a count figure.
        # So, to get around this, I've made duplicates of the function.
        # The loop below keeps track of how many image slices
        # it has sent to a particular version of the cloud function, and when that number
        # reaches 30, it starts sending to another version.
        # howManySlices = 0
        # functionSwitcher = 0
        # rowMover = 5
        # for image, imageName in namesAndImages.items():
        #     # if we've gotten to the point where 30 slices have been sent...
        #     if howManySlices == 30: 
        #         # tell the sendToCloudFunction function that it's time to switch
        #         functionSwitcher += 1
        #         howManySlices = 0
        #     print("sending one image")
        #     loopDictToSend =({'type': 'count', 'flyoverDate': flyoverDate, 'ranchBlock': ranchBlock, 'sublot': sublot, 'fileName': imageName, 'functionSwitcher': functionSwitcher, 'rowToMoveTo': rowMover})
        #     disThread = threading.Thread(target=sendToCloudFunction, args=[loopDictToSend])
        #     disThread.start()
        #     howManySlices += 1
        #     rowMover += 1
            
 
        #return render_template('analyze.html', ranchesForSelection = _Ranches, result = count)

    # ------------------------ This is leftover code from when I was planning to ---------
    # ------------------------ do image processing via Google Tasks ----------------------
    # ------------------------ Turns out that wouldn't be possible because it's ----------
    # ------------------------ impossible to upload numpy or openCv to Google ------------
    # ------------------------ App Engine, which Google Tasks requires -------------------
    # # Now, we put the images in the payload of a task
    # # and send that task to cloud-tasks
    # project = 'online-library-app'
    # queue = 'broccoliQueue'
    # location = 'us-central1'
    # url = 'https://online-library-app.uc.r.appspot.com/broccoliQueue'
    # payload = {'param': 'value'}
    
    # # Construct the fully qualified queue name.
    # parent = task_client.queue_path(project, location, queue)
    
    # # Construct the request body.
    # task = {
    #     "http_request": {  
    #         "http_method": tasks_v2.HttpMethod.POST,
    #         "url": url,  
    #     }
    # }
    # if payload is not None:
    #     if isinstance(payload, dict):
    #         # Convert dict to JSON string
    #         payload = json.dumps(payload)
    #         # specify http content-type to application/json
    #         task["http_request"]["headers"] = {"Content-type": "application/json"}
    
    #     # The API expects a payload of type bytes.
    #     converted_payload = payload.encode()
    
    #     # Add the payload to the request.
    #     task["http_request"]["body"] = converted_payload
        
    # task_client.create_task(request={"parent": parent, "task": task})

    #return redirect(url_for('login'))

# ---------- This is an endpoint triggered automatically by cloud scheduler, for getting the loss trend
@app.route('/getTrend/<client>', methods=['GET', 'POST'])
def getTrend(client, ranchesToView, startDate):
    
    #Just to cut down on the number of Cloud Scheduler tasks we have to set up,
    #we're going to pass all client strings to this endpoint in the 'client' variable
    #they will be dash-separated, so we'll separate them by dashes, then loop through them
    
    eachClient = client.split("-")
    
    for client in eachClient:
    
        crops_lost = 0
        percent_missing = 0
        trending = "Loss trend is flat"
        
        # let's check the period between today and 7 days previously
        firstPeriodStart = startDate - datetime.timedelta(days = 14)
        firstPeriodEnd = startDate
    
        # Get the data for this week
        gottenEntities = []
        daysToGoBack = 14
        acresThisTimePeriod = 0.0
        # We try to get some data, but if the total number of acres flown in that time period
        # is less than 100,
        # then we push back the starting date of the timeframe to inspect by 7 days
        # and try again (the ending date of the timeframe is always today)
        while daysToGoBack < 100:
            gottenEntities, a = getEntitiesAndRanchesToView(client, firstPeriodStart, firstPeriodEnd, ranchesToView, "DateFlown", True)
                   
            for entity in gottenEntities:
                if entity['Test'] == "Count":
                    acresThisTimePeriod += entity['AcresFlown']
                    
            if acresThisTimePeriod > 99:
                break
            else:
                firstPeriodStart = startDate - datetime.timedelta(days = daysToGoBack)
                daysToGoBack += 14
                acresThisTimePeriod = 0.0
        
        firstEntityCount = len(gottenEntities)
        
        a,a,a,a, TWcrops_lost, TWpercent_missing, TWpercent_missing_table, a,a,a,a,a,a,a = getCountData(gottenEntities, client)
        TWndvi_average, a,a,a,a,a = getStressData(gottenEntities)
        TWtop_event = TWpercent_missing_table[0]
        TWtop_event_percent = TWpercent_missing_table[1]
    
        # Get the data for last week
        gottenEntities = []
        daysToGoBack = 14
        acresLastTimePeriod = 0.0
        secondPeriodStart = firstPeriodStart - datetime.timedelta(days = daysToGoBack)
        secondPeriodEnd = firstPeriodStart
        while daysToGoBack < 100:
            gottenEntities, a = getEntitiesAndRanchesToView(client, secondPeriodStart, secondPeriodEnd, ranchesToView, "DateFlown", True)
            
            for entity in gottenEntities:
                if entity['Test'] == "Count":
                    acresLastTimePeriod += entity['AcresFlown']
            
            if acresLastTimePeriod > 99:
                break
            else:
                secondPeriodStart = firstPeriodStart - datetime.timedelta(days = daysToGoBack)
                daysToGoBack += 14
                acresLastTimePeriod = 0.0
        
        if len(gottenEntities) > firstEntityCount:
            gottenEntities = gottenEntities[0:firstEntityCount]
        secondEntityCount = len(gottenEntities)
        
        a,a,a,a, LWcrops_lost, LWpercent_missing, LWpercent_missing_table, a,a,a,a,a,a,a = getCountData(gottenEntities, client)
        LWndvi_average, a,a,a,a,a = getStressData(gottenEntities)  
        LWtop_event_percent = LWpercent_missing_table[1]
        
    
        
        if TWcrops_lost != "0":
            crops_lost = str(TWcrops_lost)
            percent_missing = str(TWpercent_missing)
            #eventString = "Looking at the " + str(firstEntityCount) + " most recent datapoints, the event that caused the most crop loss was <span style='color:red'><b>" + TWtop_event + "</span></b>, contributing to <b>" + str(TWtop_event_percent) + "%</b> of the loss."
    
            
        #if float(TWndvi_average) > 0:
        #    ndviString = "Looking at the " + str(firstEntityCount) + " most recent datapoints, the average NDVI score for all these ranches was <b>" + str(TWndvi_average) + "</b>."
        #else:
        #    ndviString = "There is no recent stress data on these ranches."
            
        if LWcrops_lost != "0" and TWcrops_lost != "0":
            
            comparativeCountString = "<b>" + str(LWcrops_lost) + "</b> (<b>" + str(LWpercent_missing) + "%</b>)"
    
            if float(LWpercent_missing) > float(TWpercent_missing):
                trending = "Loss is trending <span style='color:green'><b>down</b></span>"
            else:   
                 trending = "Loss is trending <span style='color:red'><b>up</b></span>"
                 
#        with ndbclient.context():
#            
#            entity = ndb.Key(lossTrend, client).get()
#            entity.loss_trend = trending
#            entity.put()        
#
#    status_code = Response(status=200)
#    return status_code
    return trending

# ----------- This is an endpoint triggered automatically by cronjobs, for updating the database ------
@app.route('/createData/<client>', methods=['GET', 'POST'])
def createData(client):
    
    list_of_lists = []
    uploadedCount = 0
    nonUploadedIncomplete = 0
    nonUploadedFormatting = 0
    nonUploadedIncompleteArray = []
    nonUploadedFormattingArray = []
    
    
    with ndbclient.context():
        
        
        # Here let's just get the acres flown data for the homepage real quick
        book = spreadsheet_client.open("AOC - Braga O Broccoli - May to Dec 2020")
        sheet = book.worksheet("StressInputs")
        sheet2 = book.worksheet("CountInputs")
        stress_acresFlown = sheet.col_values(7)
        count_acresFlown = sheet2.col_values(7)
        
        totalAcresFlown = 0.0
        for saf in range(1, len(stress_acresFlown)):
            totalAcresFlown += float(stress_acresFlown[saf])
        for caf in range(1, len(count_acresFlown)):
            totalAcresFlown += float(count_acresFlown[caf])
            
        entity = ndb.Key(acresFlown, "flown").get()
        entity.acres_flown = totalAcresFlown
        entity.put()
        
        
        
        
        query = customerData.query().filter(ndb.FloatProperty("LotSize") > 0)
        query.order(customerData.DateFlown)
        
        # in case it's T and A or church brothers
        if client == "TAndA" or client == "ChurchBrothers":
            bookString = "AOC - T&A lettuce - March 2021 start"
        else:
            # in case it's braag or betterworld
            bookString = "AOC - Braga O Broccoli - May to Dec 2020"
            
        book = spreadsheet_client.open(bookString)
        sheet = book.worksheet("StressInputs")
        sheet2 = book.worksheet("CountInputs")
        stress_lists = sheet.get_all_values()
        count_lists = sheet2.get_all_values()
        
        for slst in range(1, len(stress_lists)):
            if stress_lists[slst][0] != "":
                list_of_lists.append(stress_lists[slst])
        for clst in range(1, len(count_lists)):
            if count_lists[clst][0] != "":
                list_of_lists.append(count_lists[clst])
        
        for thisRow in range(1, len(list_of_lists)):
            splitContent = list_of_lists[thisRow]
            print(splitContent)
            incompleteEntry = False

            if (splitContent[0] == ""):
                break
            
            # Here we split the file by tab.  The resulting array is in this form:
            # Date Flown  Ranch/Block   Sublot  BlockSublotConcat  LotSize	
            #   0           1            2            3             4  
            
            # Crop  Acresflown  PlantingMethod  WetDate  HarvestDate  Test  Event  NDVIScore  NDVIChange  NDVI%Change	
            # 5       6              7            8           9        10     11      12         13          14
            
            # Count  LossToDate  Change  LossNumberAs%  
            #  15       16        17            18
            
           
            # $/Acre  Time  GbsProcessed  Gas  Miles  SaaSCost1  SaaSCost2  Subscription  Notes  Filter
            #   19     20       21         22    23      24           25         26         27     28
    
    
            # Let's make a list with all these variable names in it
            dataBitLabels = ["DateFlown", "RanchBlock", "Sublot", "BlockSublotConcat",
                             "LotSize", "Crop", "AcresFlown", "PlantingMethod", "WetDate", "HarvestDate",
                             "Test", "Event", "NDVIScore", "NDVIChange", "NDVIPercentChange",
                             "Count", "LossToDate", "CropLossSinceLastCount", "LossAsPercent",
                             "DollarsAcre", "Time", "GbsProcessed", "Notes"]
            
            if client == "BetterWorld":
                splitContent[1] = swapRanchNames(splitContent[1])
                splitContent[3] = swapRanchNames(splitContent[3])
            
            # If it's a count, then at least 0-11 and 15-18 need to have data in them
            if splitContent[10] == "Count": 
                for x in range(0, 12):    
                    if splitContent[x] == "":
                        incompleteEntry = True
                for x in range(15, 19):
                    if splitContent[x] == "":
                        incompleteEntry = True
            # If it's a stress test, then at least 0-14 need to have data in them
            if splitContent[10] == "Stress": 
                for x in range(0, 15):    
                    if splitContent[x] == "":
                        incompleteEntry = True   
            # If the test field itself is blank, something is wrong
            if splitContent[10] == "":
                incompleteEntry = True
    
            # Let's put all the bits of data into a dictionary, to make it all easier to keep track of
            dataBits = dict({})
            for label in range(0, len(dataBitLabels)):
                if (dataBitLabels[label] == "Notes"):
                    dataBits.update({dataBitLabels[label]: splitContent[27]})
                else:
                    dataBits.update({dataBitLabels[label]: splitContent[label]})

                    
            if incompleteEntry == False: 
                
                try:
                    
                    flownDate = toDateTime(splitContent[0])
                    wetDate = toDateTime(splitContent[8])
                    harvestDate = toDateTime(splitContent[9])
                    
                    if dataBits['NDVIScore'] == "":
                        dataBits['NDVIScore'] = 0.0
                    if dataBits['NDVIChange'] == "":
                        dataBits['NDVIChange'] = 0.0
                    if dataBits['NDVIPercentChange'] == "":
                        dataBits['NDVIPercentChange'] = 0.0
                    if dataBits['Count'] == "":
                        dataBits['Count'] = 0
                    if dataBits['LossToDate'] == "":
                        dataBits['LossToDate'] = 0
                    if dataBits['CropLossSinceLastCount'] == "":
                        dataBits['CropLossSinceLastCount'] = 0                    
                    if dataBits['LossAsPercent'] == "":
                        dataBits['LossAsPercent'] = 0.0                                     
                    if dataBits['GbsProcessed'] == "":
                        dataBits['GbsProcessed'] = 0.0                                     
                
                    create_customer_data(client, flownDate, dataBits['RanchBlock'], dataBits['Sublot'],
                                          dataBits['BlockSublotConcat'], float(dataBits['LotSize']), dataBits['Crop'],
                                          float(dataBits['AcresFlown']), dataBits['PlantingMethod'], wetDate, harvestDate,
                                          dataBits['Test'], dataBits['Event'], float(dataBits['NDVIScore']), float(dataBits['NDVIChange']),
                                          float(dataBits['NDVIPercentChange']), int(dataBits['Count']), int(dataBits['LossToDate']),
                                          int(dataBits['CropLossSinceLastCount']),
                                          float(dataBits['LossAsPercent']), float(dataBits['GbsProcessed']),
                                          str(dataBits['Notes']))
                    uploadedCount += 1
                    
                except:
                    
                    nonUploadedFormatting += 1
                    thisNonUploaded = splitContent[0] + " " + splitContent[1] + " " + splitContent[2] + " " + splitContent[10]
                    nonUploadedFormattingArray.append(thisNonUploaded)
                    
            else:
                
                nonUploadedIncomplete += 1
                thisNonUploaded = splitContent[0] + " " + splitContent[1] + " " + splitContent[2] + " " + splitContent[10]
                nonUploadedIncompleteArray.append(thisNonUploaded)
                
        if uploadedCount > 0:
            # Put info in the database saying "The data was updated today!"
            entity = ndb.Key(lastUpdated, client).get()
            entity.date = dateTimeToString(date.today())
            entity.put()

    return render_template('uploadSpecifics.html', uploadedCount = uploadedCount, nonUploadedIncomplete = nonUploadedIncomplete, nonUploadedFormatting = nonUploadedFormatting, nonUploadedIncompleteArray = nonUploadedIncompleteArray, nonUploadedFormattingArray = nonUploadedFormattingArray)

# ----------- This is an endpoint triggered automatically by cronjobs, for sending email notifications ------
@app.route('/sendEmail', methods=['GET', 'POST'])
def sendEmail():

    clients = []
    ranchesToView = []
    ranchesToViewForString = []
    emails = []
    
    firstEntityCount = 0
    secondEntityCount = 0
    
    combinedz = []
    
    if request.method == 'POST': 
    
        with ndbclient.context():
            query = emailNotification.query()
    
            for key in query.iter(keys_only=True):
                entity = key.get()
                
                clients.append(entity.client)
                ranchesToView.append(entity.ranches.split(" - "))
                ranchesToViewForString.append(entity.ranches)
                emails.append(entity.email.split(" - "))
                
        for e in range(0, len(clients)):   
            
            # let's check the period between today and 7 days previously
            firstPeriodStart = date.today() - datetime.timedelta(days = 7)
            firstPeriodEnd = date.today()
        
            # Get the data for this week
            gottenEntities = []
            daysToGoBack = 7
            acresThisTimePeriod = 0.0
            # We try to get some data, but if the total number of acres flown in that time period
            # is less than 100,
            # then we push back the starting date of the timeframe to inspect by 7 days
            # and try again (the ending date of the timeframe is always today)
            while daysToGoBack < 100:
                gottenEntities, a = getEntitiesAndRanchesToView(clients[e], firstPeriodStart, firstPeriodEnd, ranchesToView[e], "DateFlown", True)
                
                for entity in gottenEntities:
                    if entity['Test'] == "Count":
                        acresThisTimePeriod += entity['AcresFlown']
                        
                if acresThisTimePeriod > 99:
                    break
                else:
                    firstPeriodStart = date.today() - datetime.timedelta(days = daysToGoBack)
                    daysToGoBack += 7
                    acresThisTimePeriod = 0.0
            
            firstEntityCount = len(gottenEntities)
            
            a,a,a,a, TWcrops_lost, TWpercent_missing, TWpercent_missing_table, a,a,a,a,a,a,a = getCountData(gottenEntities, clients[e])
            TWndvi_average, a,a,a,a,a = getStressData(gottenEntities)
            TWtop_event = TWpercent_missing_table[0]
            TWtop_event_percent = TWpercent_missing_table[1]
        
            # Get the data for last week
            gottenEntities = []
            daysToGoBack = 7
            acresLastTimePeriod = 0.0
            secondPeriodStart = firstPeriodStart - datetime.timedelta(days = daysToGoBack)
            secondPeriodEnd = firstPeriodStart
            while daysToGoBack < 100:
                gottenEntities, a = getEntitiesAndRanchesToView(clients[e], secondPeriodStart, secondPeriodEnd, ranchesToView[e], "DateFlown", True)
                
                for entity in gottenEntities:
                    if entity['Test'] == "Count":
                        acresLastTimePeriod += entity['AcresFlown']
                
                if acresLastTimePeriod > 99:
                    break
                else:
                    secondPeriodStart = firstPeriodStart - datetime.timedelta(days = daysToGoBack)
                    daysToGoBack += 7
                    acresLastTimePeriod = 0.0
            
            if len(gottenEntities) > firstEntityCount:
                gottenEntities = gottenEntities[0:firstEntityCount]
            secondEntityCount = len(gottenEntities)
            
            a,a,a,a, LWcrops_lost, LWpercent_missing, LWpercent_missing_table, a,a,a,a,a,a,a = getCountData(gottenEntities, clients[e])
            LWndvi_average, a,a,a,a,a = getStressData(gottenEntities)  
            LWtop_event_percent = LWpercent_missing_table[1]
            
            ranchesString =  ranchesToViewForString[e]
            
            if TWcrops_lost != "0":
                countString = "<b>" + str(TWcrops_lost) + "</b> (<b>" + str(TWpercent_missing) + "%</b>)"
                #eventString = "Looking at the " + str(firstEntityCount) + " most recent datapoints, the event that caused the most crop loss was <span style='color:red'><b>" + TWtop_event + "</span></b>, contributing to <b>" + str(TWtop_event_percent) + "%</b> of the loss."
            else:
                countString = "There is no recent count data on these ranches."
                #eventString = ""
                
            #if float(TWndvi_average) > 0:
            #    ndviString = "Looking at the " + str(firstEntityCount) + " most recent datapoints, the average NDVI score for all these ranches was <b>" + str(TWndvi_average) + "</b>."
            #else:
            #    ndviString = "There is no recent stress data on these ranches."
                
            if LWcrops_lost != "0" and TWcrops_lost != "0":
                
                comparativeCountString = "<b>" + str(LWcrops_lost) + "</b> (<b>" + str(LWpercent_missing) + "%</b>)"

                if float(LWpercent_missing) > float(TWpercent_missing):
                    trending = "The percent of crops lost is <span style='color:green'><b>lower</b></span> than before."
                else:   
                     trending = "The percent of crops lost is <span style='color:red'><b>higher</b></span> than before."
            #else:
            #    comparativeCountString = "There is no count data from the previous period, so no comparison can be made."
                
#            if float(TWndvi_average) > 0 and float(LWndvi_average) > 0:
#                if float(LWndvi_average) < float(TWndvi_average):
#                     comparativeNdviString = "Comparing the " + str(firstEntityCount) + " most recent datapoints to the " + str(secondEntityCount) +" datapoints before them, the average NDVI score has gotten <span style='color:green'><b>higher</b></span>. The average NDVI score during the previous period was " + str(LWndvi_average) + "."
#                else:
#                     comparativeNdviString = "Comparing the " + str(firstEntityCount) + " most recent datapoints to the " + str(secondEntityCount) +" datapoints before them, the average NDVI score has gotten <span style='color:red'><b>lower</b></span>. The average NDVI score during the previous period was " + str(LWndvi_average) + "."
#            else:
#                comparativeNdviString = "There is no stress data from the previous period, so no comparison can be made."
        
            # ---- uncomment this if you want to debug the numbers -----------------------
#            emailBody = "<h1>Agxactly weekly ranch report!</h1>" \
#                "<span style='color:grey;'><h3>-- This section is for debugging purposes (usually not included in reports) --</h3>" \
#                "-- you are seeing this section because you are on the Agxactly team --" \
#                "<br>-- this is not included in reports that go out to regular clients --" \
#                "<br><br>The numbers in this report were generated by looking at flyover dates " \
#                "between " + str(firstPeriodEnd) + " and " + str(firstPeriodStart) + ", during which " + str(round(acresThisTimePeriod)) + " acres were flown (" + str(firstEntityCount) + " flyover dates), and comparing them " \
#                "to flyover dates between " + str(secondPeriodEnd) + " and " + str(secondPeriodStart) + ", during which " + str(round(acresLastTimePeriod)) + " acres were flown (" + str(secondEntityCount) + " flyover dates)</span>"\
#                "<br><br>" \
#                "<b>Ranches covered:</b> <br>" + ranchesString + " \
#                <h2>Recent loss/Past loss:</h2>" + countString + "<br>" + comparativeCountString + " \
#                <h2>Trend:</h2>" + trending
 
            #emailBody = "<h1>Agxactly weekly ranch report!</h1>" \
            #    "<b>Ranches covered:</b> <br>" + ranchesString + " \
            #    <h2>Recent loss/Past loss:</h2>" + countString + "<br>" + comparativeCountString + " \
            #    <h2>Trend:</h2>" + trending  
                
            emailBody = "<div class=''><div class='aHl'></div><div id=':ox' tabindex='-1'></div><div id=':ks' class='ii gt'><div id=':kr' class='a3s aiL msg-243268057448697561'><u></u><div style='background-color:#f4f4f4'><div style='background-color:#f4f4f4'><div style='margin:0px auto;max-width:600px'><table role='presentation' style='width:100%' cellspacing='0' cellpadding='0' border='0' align='center'><tbody><tr><td style='direction:ltr;font-size:0px;padding:20px 0px 20px 0px;text-align:center'><div class='m_-243268057448697561mj-column-per-67' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' style='vertical-align:top' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='font-size:0px;padding:0px 0px 0px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='left'><div style='font-family:Arial,sans-serif;font-size:13px;letter-spacing:normal;line-height:1;text-align:left;color:#000000'><p style='margin:10px 0'></p></div></td></tr></tbody></table></div><div class='m_-243268057448697561mj-column-per-33' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' style='vertical-align:top' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='font-size:0px;padding:0px 25px 0px 0px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='left'><div style='font-family:Arial,sans-serif;font-size:13px;letter-spacing:normal;line-height:1;text-align:left;color:#000000'></div></td></tr></tbody></table></div></td></tr></tbody></table></div><div style='margin:0px auto;max-width:600px'><table role='presentation' style='width:100%' cellspacing='0' cellpadding='0' border='0' align='center'><tbody><tr><td style='direction:ltr;font-size:0px;padding:20px 0;padding-bottom:0px;padding-top:0px;text-align:center'><div class='m_-243268057448697561mj-column-per-100' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' style='vertical-align:top' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='font-size:0px;padding:10px 25px;padding-top:0px;padding-right:0px;padding-bottom:0px;padding-left:0px;word-break:break-word' align='center'><table role='presentation' style='border-collapse:collapse;border-spacing:0px' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='width:600px'><a href='http://xstt3.mjt.lu/lnk/BAAAAXqfosUAAAAAAAAAAKpuiEIAAToSxqMAAAAAAA3O_wBgL0etYsbtCsVVSDSkbk6sYqC07QANtuU/1/9p14zJGYUjviarxlo9JDNQ/aHR0cHM6Ly93d3cuYWd4YWN0bHkuY29tL3N0YXRpYy9zaXRlLWltZy9GaW5hbCUyMEFneGFjdGx5LnBuZw' target='_blank' data-saferedirecturl='https://www.google.com/url?q=http://xstt3.mjt.lu/lnk/BAAAAXqfosUAAAAAAAAAAKpuiEIAAToSxqMAAAAAAA3O_wBgL0etYsbtCsVVSDSkbk6sYqC07QANtuU/1/9p14zJGYUjviarxlo9JDNQ/aHR0cHM6Ly93d3cuYWd4YWN0bHkuY29tL3N0YXRpYy9zaXRlLWltZy9GaW5hbCUyMEFneGFjdGx5LnBuZw&amp;source=gmail&amp;ust=1613797690387000&amp;usg=AFQjCNGeNWa9GABrhrG4tR2h2rFSmRBHkQ'><img alt='' src='https://ci3.googleusercontent.com/proxy/c7RvsiE3dz7u-4ZniCbWLjvJS1V3mWLUZgtvFMJpUdxyUcCApHfQcqqBkRZtLkTT9iyZl6oCAautdXak193VVhI1OB9zZmIZLT4E9Xxpgw4=s0-d-e1-ft#https://www.agxactly.com/static/site-img/Final%20Agxactly.png' style='border:none;border-radius:px;display:block;outline:none;text-decoration:none;height:auto;width:100%;font-size:13px' class='CToWUd' width='600' height='auto'></a></td></tr></tbody></table></td></tr><tr><td style='font-size:0px;word-break:break-word'><div style='height:50px'>&nbsp;</div></td></tr><tr><td style='font-size:0px;padding:10px 25px;word-break:break-word'><p style='border-top:solid 2px #e6e6e6;font-size:1px;margin:0px auto;width:100%'></p></td></tr></tbody></table></div></td></tr></tbody></table></div><div style='background:#ffffff;background-color:#ffffff;margin:0px auto;max-width:600px'><table role='presentation' style='background:#ffffff;background-color:#ffffff;width:100%' cellspacing='0' cellpadding='0' border='0' align='center'><tbody><tr><td style='direction:ltr;font-size:0px;padding:20px 0px 0px 0px;text-align:center'><div class='m_-243268057448697561mj-column-per-100' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' style='vertical-align:top' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='font-size:0px;word-break:break-word'><div style='height:5px'>&nbsp;</div></td></tr><tr><td style='font-size:0px;padding:0px 25px 0px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='left'><div style='font-family:Arial,sans-serif;font-size:13px;letter-spacing:normal;line-height:1;text-align:left;color:#000000'><h1 style='margin-top:10px;margin-bottom:10px;font-weight:normal'>AGXactly Weekly Ranch Report</h1></div></td></tr><tr><td style='font-size:0px;padding:0px 25px 0px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='left'><div style='font-family:Arial,sans-serif;font-size:13px;letter-spacing:normal;line-height:1;text-align:left;color:#000000'><p style='margin:10px 0;margin-top:10px'>AGXactly weekly ranch report for the following ranches:</p><p style='margin:10px 0'><br>" + ranchesString + "</b></p></div></td></tr></tbody></table></div></td></tr></tbody></table></div><div style='margin:0px auto;max-width:600px'><table role='presentation' style='width:100%' cellspacing='0' cellpadding='0' border='0' align='center'><tbody><tr><td style='direction:ltr;font-size:0px;padding:20px 0;text-align:center'><div class='m_-243268057448697561mj-column-per-33-333333333333336' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' style='vertical-align:top' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='font-size:0px;padding:10px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='left'><div style='font-family:Arial,sans-serif;font-size:16px;letter-spacing:normal;line-height:1;text-align:left;color:#000000'><p style='margin:10px 0;margin-top:10px;margin-bottom:10px'><span style='color:#55575d;font-family:Arial,Helvetica,sans-serif;font-size:16px'><b>Previous Loss</b><br><br>" + comparativeCountString + "</span></p></div></td></tr></tbody></table></div><div class='m_-243268057448697561mj-column-per-33-333333333333336' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' style='vertical-align:top' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='font-size:0px;padding:10px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='left'><div style='font-family:Arial,sans-serif;font-size:16px;letter-spacing:normal;line-height:1;text-align:left;color:#000000'><p style='margin:10px 0;margin-top:10px;margin-bottom:10px'><span style='color:#55575d;font-family:Arial,Helvetica,sans-serif;font-size:16px'><b>Loss This Time</b><br><br>" + countString + "</span></p></div></td></tr></tbody></table></div><div class='m_-243268057448697561mj-column-per-33-333333333333336' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' style='vertical-align:top' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='font-size:0px;padding:10px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='left'><div style='font-family:Arial,sans-serif;font-size:16px;letter-spacing:normal;line-height:1;text-align:left;color:#000000'><p style='margin:10px 0;margin-top:10px;margin-bottom:10px'><span style='color:#55575d;font-family:Arial,Helvetica,sans-serif;font-size:16px'><b>Loss Trend</b><br><br>" + trending + "</span></p></div></td></tr></tbody></table></div></td></tr></tbody></table></div><div style='background:#ffffff;background-color:#ffffff;margin:0px auto;max-width:600px'><table role='presentation' style='background:#ffffff;background-color:#ffffff;width:100%' cellspacing='0' cellpadding='0' border='0' align='center'><tbody><tr><td style='direction:ltr;font-size:0px;padding:20px 0px 0px 0px;text-align:center'><div class='m_-243268057448697561mj-column-per-100' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' style='vertical-align:top' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='font-size:0px;word-break:break-word'><div style='height:5px'>&nbsp;</div></td></tr><tr></div></td></tr><tr><td style='font-size:0px;padding:0px 25px 0px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='left'><div style='font-family:Arial,sans-serif;font-size:13px;letter-spacing:normal;line-height:1;text-align:left;color:#000000'><p style='margin:10px 0;margin-top:10px'>Anything else you'd like to see on this report for next time? Here are some examples:<ul><li>Top five performing ranches</li><li>Events contributing to loss</li><li>Rate of loss by ranch</li><li>Health data</li></ul><p style='margin:10px 0;margin-top:1px'>You can customize this weekly report by replying to this email directly, or by logging in to the dashboard <a href='https://www.agxactly.com/login/go'>here</a>.</p><p style='margin:10px 0;margin-bottom:10px'>&nbsp;</p></div></td></tr></tbody></table></div></td></tr></tbody></table></div><div style='margin:0px auto;max-width:600px'><table role='presentation' style='width:100%' cellspacing='0' cellpadding='0' border='0' align='center'><tbody><tr><td style='direction:ltr;font-size:0px;padding:20px 0px 20px 0px;text-align:center'><div class='m_-243268057448697561mj-column-per-100' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' style='vertical-align:top' width='100%' cellspacing='0' cellpadding='0' border='0'></table></div></td></tr></tbody></table></div><div style='margin:0px auto;max-width:600px'><table role='presentation' style='width:100%' cellspacing='0' cellpadding='0' border='0' align='center'><tbody><tr><td style='direction:ltr;font-size:0px;padding:20px 0px 20px 0px;text-align:center'><div class='m_-243268057448697561mj-column-per-100' style='font-size:0px;text-align:left;direction:ltr;display:inline-block;vertical-align:top;width:100%'><table role='presentation' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='vertical-align:top;padding:0'><table role='presentation' width='100%' cellspacing='0' cellpadding='0' border='0'><tbody><tr><td style='font-size:0px;padding:10px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='center'><div style='font-family:Arial,sans-serif;font-size:11px;letter-spacing:normal;line-height:22px;text-align:center;color:#000000'></div></td></tr><tr><td style='font-size:0px;padding:10px 25px;padding-top:0px;padding-bottom:0px;word-break:break-word' align='center'><div style='font-family:Arial,sans-serif;font-size:11px;letter-spacing:normal;line-height:22px;text-align:center;color:#000000'></div></td></tr></tbody></table></td></tr></tbody></table></div></td></tr></tbody></table></div></div><br><img src='https://ci5.googleusercontent.com/proxy/0B_3Sht57IL80lBaZ8j7XUSloNuOtoVroBi6tbMWZ6rUWZCFR-EXh8nKvgIiVzwtvzKArB3U-ccVUGXe8mYVQbNgtYosrvc4U0PGenGM06ciOxgQeAwx-Q8KqjrzIbEBPBMESpLxTea9oe_uI5FRtZNX3umnSTd0TuzEJkoH_1f3dDZMSxosPQ=s0-d-e1-ft#http://xstt3.mjt.lu/oo/BAAAAXqfosUAAAAAAAAAAKpuiEIAAToSxqMAAAAAAA3O_wBgL0etYsbtCsVVSDSkbk6sYqC07QANtuU/87625900/e.gif' alt='' style='height:1px;width:1px;border:0' class='CToWUd' width='1' height='1' border='0'><div class='yj6qo'></div><div class='adL'></div></div></div></div><div id=':pb' class='ii gt' style='display:none'><div id=':or' class='a3s aiL undefined'></div></div><div class='hi'></div></div>"           
            
            send_notification(emails[e], "Agxactly Weekly Report", "Your weekly ranches report", emailBody)
            
            combined = "This email was sent to " + ", ".join(emails[e]) + ":<br><br>" + emailBody + "<br><br>"
            combinedz.append(combined)
            
        status_code = Response(status=200)
        return status_code
                        
        #return render_template('callback.html', combinedz = combinedz)

# ----------- This is an endpoint triggered automatically by cronjobs, for checking if any  ------
# ------- user-set conditions are met, then sending an alert email if they are -------------------
@app.route('/checkConditionsAndSendAlert', methods=['GET', 'POST'])
def checkConditionsAndSendAlert():
    
    startDate = date.today() - datetime.timedelta(days = 365)
    endDate = date.today()

    
    clients = []
    ranchesToView = []
    ranchesToViewForString = []
    emails = []
    emailsAsString = []
    conditions = []
    alreadySent = []
    
    sentsToAdd = []
    atLeastOneAlert = False
    combinedz = []
    
    meetTheConditionString = ""
    
    if request.method == 'POST':
    
        with ndbclient.context():
            query = emailAlert.query()
    
            for key in query.iter(keys_only=True):
                entity = key.get()
                
                clients.append(entity.client)
                ranchesToView.append(entity.ranches.split(" - "))
                ranchesToViewForString.append(entity.ranches)
                emails.append(entity.email.split(" - "))
                emailsAsString.append(entity.email)
                conditions.append(entity.conditions.split(" - "))
                # This is a listholds all the notifications that were already sent,
                # so no duplicates are sent in the future.
                # It contains each line of the email
                alreadySent.append(entity.sent)
                
        for e in range(0, len(clients)):   
            
            ranchesString = "The ranches covered in this notification are: <b>" + ranchesToViewForString[e] + "</b>"
            
            emailBody = "<h1>Agxacty ALERT email</h1> \
                <b>Ranches covered:</b> <br>" + ranchesString + "<br><br>"
                
            allFlyoverDates_count = []
            allFlyoverDates_stress = []
                
            # Get the data for this week
            gottenEntities, a = getEntitiesAndRanchesToView(clients[e], startDate, endDate, ranchesToView[e], "DateFlown", True)
            
            a,a,a,a,a,a,a, CountData,a,a,a,a,a,a = getCountData(gottenEntities, clients[e])
            a,a,a, StressData,a,a = getStressData(gottenEntities)
            
            # In this "CountData" array, we have:
            #    0           1            2        3          4       5             6      7
            #   DateFlown   RanchBlock   Sublot   Size   WetDate   HarvestDate   Event   str-Count   
            #
            #    8                 9                          10               
            #   str-LossToDate  str-CropLossSinceLastCount   LossAsPercent
            for c in range(0, len(CountData), 11):
                # Let's put all the important count data into a dictionary
                thisFlyoverDate = dict({})
                thisFlyoverDate.update({'DateFlown': dateTimeToString(CountData[c])})
                thisFlyoverDate.update({'RanchBlock': CountData[c+1]})
                thisFlyoverDate.update({'Sublot': CountData[c+2]})
                thisFlyoverDate.update({'Event': CountData[c+6]})
                # Loss to date x 100 / (loss # as percent)
                # this formula will give us "percent lost on this flight" data!
                losssincelast = int(CountData[c+9].replace(",", ""))
                losstodate = int(CountData[c+8].replace(",", "")) * 100
                lossaspercent = float(CountData[c+10])
                percentLostThisTime = round(weird_division(losssincelast, weird_division(losstodate, lossaspercent)) * 100, 2)            
                thisFlyoverDate.update({'Crop loss on most current flight': percentLostThisTime})
                thisFlyoverDate.update({'Crop loss to date': CountData[c+10]})
                
                allFlyoverDates_count.append(thisFlyoverDate)
                
                
                
            
            # In this "StressData" array, we have:
            #   0            1              2      3           4 
            #   DateFlown   RanchBlock   Sublot   Event   NDVIScore
            #
            #   5                6             7
            #   up-down-flat   NDVIChange   NDVIPercentChange
            for s in range(0, len(StressData), 8):
                # Let's put all the important count data into a dictionary
                thisFlyoverDate = dict({})
                thisFlyoverDate.update({'DateFlown': dateTimeToString(StressData[s])})
                thisFlyoverDate.update({'RanchBlock': StressData[s+1]})
                thisFlyoverDate.update({'Sublot': StressData[s+2]})
                thisFlyoverDate.update({'Event': StressData[s+3]})
                thisFlyoverDate.update({'NDVI change since last flight': StressData[s+6]})
                
                allFlyoverDates_stress.append(thisFlyoverDate)
            
            # Now, we'll go through all the conditions set by the user and check each one
            for c in range(0, len(conditions[e])-1):
                
                # This will be a string such as "Crop loss on most current flight is greater than 3 percent."
                thisCondition = conditions[e][c]
                
                condition = thisCondition.split(" is ")[0]
                # this gives us a string like "Crop loss on most current flight"
                
                lessOrMore = thisCondition.split(" is ")[1].split(" than ")[0]
                # this gives us the word "greater" or "less"
                
                percent = float(thisCondition.split(" is ")[1].split(" than ")[1].split(" percent")[0])
                # this gives us a number like 3.2
                
                if condition == "Crop loss on most current flight":
                    # IT'S A COUNT CONDITION
                    for f in range(0, len(allFlyoverDates_count)):
                        if lessOrMore == "greater":
                            if (allFlyoverDates_count[f][condition] > percent):
                                
                                thisString = "A " + str(allFlyoverDates_count[f][condition]) + \
                                " percent crop loss was observed during an aerial count of the crops in " + \
                                allFlyoverDates_count[f]['RanchBlock'] +  " " + \
                                allFlyoverDates_count[f]['Sublot'] + ". (" + allFlyoverDates_count[f]['DateFlown'] + ")<br>"
                                
                                if (sentAlready(thisString, alreadySent[e]) == False):
                                    meetTheConditionString = meetTheConditionString + thisString
                                    sentsToAdd.append(thisString)
                                
                        else:
                            if (allFlyoverDates_count[f][condition] < percent):
                                
                                thisString = "A " + str(allFlyoverDates_count[f][condition]) + \
                                " percent crop loss was observed during a  aerial count of the crops in " + \
                                allFlyoverDates_count[f]['RanchBlock'] +  " " + \
                                allFlyoverDates_count[f]['Sublot'] + ". (" + allFlyoverDates_count[f]['DateFlown'] + ")<br>"   
                                
                                if (sentAlready(thisString, alreadySent[e]) == False):
                                    meetTheConditionString = meetTheConditionString + thisString
                                    sentsToAdd.append(thisString)
                                                       
                                
                if condition == "Crop loss to date":
                     # IT'S A COUNT CONDITION
                    for f in range(0, len(allFlyoverDates_count)):
                        if lessOrMore == "greater":
                            if (allFlyoverDates_count[f][condition] > percent):
                                
                                thisString = "The total crop loss to date in " + allFlyoverDates_count[f]['RanchBlock'] +  " " + \
                                allFlyoverDates_count[f]['Sublot'] + " is now " \
                                + str(allFlyoverDates_count[f][condition]) + \
                                " percent, according to an aerial count of the crops on " + \
                                allFlyoverDates_count[f]['DateFlown'] + ".<br>"
                                
                                if (sentAlready(thisString, alreadySent[e]) == False):
                                    meetTheConditionString = meetTheConditionString + thisString
                                    sentsToAdd.append(thisString)
                                
                        else:
                            if (allFlyoverDates_count[f][condition] < percent):
                                
                                thisString = "The total crop loss to date in " + allFlyoverDates_count[f]['RanchBlock'] +  " " + \
                                allFlyoverDates_count[f]['Sublot'] + " is now " \
                                + str(allFlyoverDates_count[f][condition]) + \
                                " percent, according to an aerial count of the crops on " + \
                                allFlyoverDates_count[f]['DateFlown'] + ".<br>"           
                                
                                if (sentAlready(thisString, alreadySent[e]) == False):
                                    meetTheConditionString = meetTheConditionString + thisString
                                    sentsToAdd.append(thisString)
                                        
                    
                if condition == "NDVI change since last flight":
                    # IT'S A STRESS CONDITION
                    for f in range(0, len(allFlyoverDates_stress)):
                        if lessOrMore == "greater":
                            if (allFlyoverDates_stress[f][condition] > percent):
                                
                                thisString = "The NDVI score of " + allFlyoverDates_stress[f]['RanchBlock'] +  " " + \
                                allFlyoverDates_stress[f]['Sublot'] + " changed by " + \
                                str(allFlyoverDates_stress[f][condition]) + " percent, according to a stress survey" \
                                " carried out on " + allFlyoverDates_stress[f]['DateFlown'] + ".<br>" 
                                
                                if (sentAlready(thisString, alreadySent[e]) == False):
                                    meetTheConditionString = meetTheConditionString + thisString
                                    sentsToAdd.append(thisString)
                                                 
                        else:
                            if (allFlyoverDates_count[f][condition] < percent):
                                
                                thisString = "The NDVI score of " + allFlyoverDates_stress[f]['RanchBlock'] +  " " + \
                                allFlyoverDates_stress[f]['Sublot'] + " changed by " + \
                                str(allFlyoverDates_stress[f][condition]) + " percent, according to a stress survey" \
                                " carried out on " + allFlyoverDates_stress[f]['DateFlown'] + ".<br>" 
                                
                                if (sentAlready(thisString, alreadySent[e]) == False):
                                    meetTheConditionString = meetTheConditionString + thisString
                                    sentsToAdd.append(thisString)
    
            
                if "due to" in condition:
                    # IT'S AN EVENT CONDITION
                    
                    whichEvent = condition.split(" to ")[1]
                    
                    for f in range(0, len(allFlyoverDates_count)):
                        if lessOrMore == "greater":
                            if ((allFlyoverDates_count[f]['Crop loss on most current flight'] > percent) and (allFlyoverDates_count[f]['Event'] == whichEvent)):
                                
                                thisString = allFlyoverDates_count[f]['Event'] +  " caused a crop loss of " + \
                                str(allFlyoverDates_count[f]['Crop loss on most current flight']) + \
                                " percent in " + allFlyoverDates_count[f]['RanchBlock'] +  " " + \
                                allFlyoverDates_count[f]['Sublot'] + " on " + \
                                allFlyoverDates_count[f]['DateFlown'] + ".<br>"
                                
                                if (sentAlready(thisString, alreadySent[e]) == False):
                                    meetTheConditionString = meetTheConditionString + thisString
                                    sentsToAdd.append(thisString)
                                
                                
                        else:
                            if ((allFlyoverDates_count[f]['Crop loss on most current flight'] < percent) and (allFlyoverDates_count[f]['Event'] == whichEvent)):
                                
                                thisString = allFlyoverDates_count[f]['Event'] +  " caused a crop loss of " + \
                                str(allFlyoverDates_count[f]['Crop loss on most current flight']) + \
                                " percent in " + allFlyoverDates_count[f]['RanchBlock'] +  " " + \
                                allFlyoverDates_count[f]['Sublot'] + " on " + \
                                allFlyoverDates_count[f]['DateFlown'] + ".<br>"
                                
                                if (sentAlready(thisString, alreadySent[e]) == False):
                                    meetTheConditionString = meetTheConditionString + thisString
                                    sentsToAdd.append(thisString)
    
                if len(sentsToAdd) > 0:
                    
                    atLeastOneAlert = True
                    emailBody = emailBody + "You set an alert to be generated if: <b>" + thisCondition \
                        + "</b>.  <span style='color:red'>That condition has been met.</span> \
                            <br>Here are the details:<br><br>" + meetTheConditionString + "<br><br>"
                    
                    thisKey = clients[e] + emailsAsString[e] + ranchesToViewForString[e]
                    with ndbclient.context():
                        entity = ndb.Key(emailAlert, thisKey).get()
                        entity.sent = entity.sent + sentsToAdd
                        entity.put()
                    
                meetTheConditionString = ""
                                
            # Send email here!  Still in the "clients" loop
            if (atLeastOneAlert == True):
                
                combined = "This email was sent to " + ", ".join(emails[e]) + ":<br><br>" + emailBody + "<br><br>"
                combinedz.append(combined)
                
                # Realized that empty notification mails were getting sent, so added this if statement
                
                # This is the length of everything after the word "details:" (if no information
                # exists in the email, this will be about 24 characters)
                lengthAfterDetails = len(emailBody) - emailBody.index("details:")
                if lengthAfterDetails > 30: # 30 is just arbitrary, it's actually more like 24
                    f = send_notification(emails[e], "Agxactly ALERTS", "An Alert email from Agxactly", emailBody)
                    atLeastOneAlert = False
            
            # Reset the conditions string
            meetTheConditionString = ""
            
        status_code = Response(status=200)
        return status_code  
        #return render_template('callback.html', combinedz = combinedz)


# ----------------- Here are the actual pages for the website --------------------------
@app.route('/create', methods=['GET', 'POST'])
def create():

#    with ndbclient.context():
#        create_secure_account("agxactly-admin", "agx4ever", "Braga")
#        create_secure_account("agxactly", "fly.fly.fly", "Braga")
#        create_secure_account("betterworld", "precision", "BetterWorld")
#        create_secure_account("debug", "debug", "Braga")
#        create_secure_account("gevans@agxactly.com", "agx4ever", "Braga")
#        create_secure_account("rcole@agxactly.com", "agx4ever", "Braga")
#        create_secure_account("tgillies@agxactly.com", "agx4ever", "Braga")
#        create_secure_account("josh.ruiz@churchbrothers.com", "ChurchBrothers", "ChurchBrothers")
#        create_secure_account("pvogl@agxactly.com", "agx4ever", "TAndA")
#        create_view_preferences("debug")
#        create_view_preferences('agxactly')
#        create_view_preferences('betterworld')
#        create_view_preferences('debug')
#        create_view_preferences('gevans@agxactly.com')
#        create_view_preferences('rcole@agxactly.com')
#        create_view_preferences('tgillies@agxactly.com')
#        create_view_preferences("pvogl@agxactly.com")
#        create_view_preferences("josh.ruiz@churchbrothers.com")
    return redirect(url_for('index'))

@app.route('/postDoor', methods=['GET', 'POST'])
def postDoor():
    
    message = None
    
    if request.method == 'POST':
        
        try:
        
            with ndbclient.context():
                entity = ndb.Key(linkedInPost, request.form['id']).get()
                
                newPosts = request.form['content']
                
                # add wrapper and postFrame tags to the iframes
                taggedPosts = ""
                postList = newPosts.split("<iframe")
                for p in range(1, len(postList)):
                    taggedPosts += "<div class='wrapper'><div class='postFrame'><iframe" + postList[p] + "</div></div>"
                
                entity.content = taggedPosts.replace("\"", "'").replace("\n", "").replace("\r", "")
                entity.put()
                
                message = "The post data you just uploaded will now appear on the homepage."
                
            return render_template("postDoor.html", message = message)
        except:
            message = "Your ID was incorrect.  Please try again!"
            return render_template("postDoor.html", message = message)
            
    return render_template("postDoor.html", message = message)
        



@app.route('/v2', methods=['GET', 'POST'])
def indexNewLayout():
    
    show_modal = False
    
    with ndbclient.context():
        # get the crops saved tally for the homepage
        entity = ndb.Key(cropsSaved, "saved").get()
        tcs = entity.saved
        
        # get the acres flown tally for the homepage
        entity = ndb.Key(acresFlown, "flown").get()
        totalAcresFlown = entity.acres_flown
        
        # get the linkedin post for the homepage
        entity = ndb.Key(linkedInPost, "rcole").get()
        linked = entity.content
    
    # Index is where users are re-routed upon logging out,
    # so just to make sure, let's try to log out users
    # when they arrive at the index page
    # If the session variables exist (meaning the user has come from the dashboard)
    if session.get('client') and session.get('username'):
        try:
            logout_user()   
            # erase the session variables
            session['client'] = ""
            session['username'] = ""
        except:
            pass
        
        
    if request.method == "POST":
        
        if request.form['typeOfPost'] == "contact":
        
            name = request.form['name']
            email = request.form['email']
            organization = request.form['organization']
            role_title = request.form['role_title']
            size = request.form['size'] 
            location = request.form['location']
            checks = request.form.getlist('items')
             
            send_email(name, email, organization, role_title, size, location, checks)
            show_modal = True
            
        if request.form['typeOfPost'] == "enter":
            
            guess = request.form['guess']
            #name = request.form['linkedinname']
            contestemail = request.form['contestemail']
            details = request.form['details']
            
            send_entry(guess, contestemail, details)
            show_modal = True
           
    return render_template('indexNewLayout.html', taf = '{:,}'.format(round(totalAcresFlown, 2)), li = linked, show_modal = show_modal, tcs = '{:,}'.format(tcs))



















@app.route('/', methods=['GET', 'POST'])
def index():
    
    show_modal = False
    
    with ndbclient.context():
        # get the crops saved tally for the homepage
        entity = ndb.Key(cropsSaved, "saved").get()
        tcs = entity.saved
        
        # get the acres flown tally for the homepage
        entity = ndb.Key(acresFlown, "flown").get()
        totalAcresFlown = entity.acres_flown
        
        # get the linkedin post for the homepage
        entity = ndb.Key(linkedInPost, "rcole").get()
        linked = entity.content
    
    # Index is where users are re-routed upon logging out,
    # so just to make sure, let's try to log out users
    # when they arrive at the index page
    # If the session variables exist (meaning the user has come from the dashboard)
    if session.get('client') and session.get('username'):
        try:
            logout_user()   
            # erase the session variables
            session['client'] = ""
            session['username'] = ""
        except:
            pass
        
        
    if request.method == "POST":
        
        if request.form['typeOfPost'] == "contact":
        
            name = request.form['name']
            email = request.form['email']
            organization = request.form['organization']
            role_title = request.form['role_title']
            size = request.form['size'] 
            location = request.form['location']
            checks = request.form.getlist('items')
             
            send_email(name, email, organization, role_title, size, location, checks)
            show_modal = True
            
        if request.form['typeOfPost'] == "enter":
            
            guess = request.form['guess']
            #name = request.form['linkedinname']
            contestemail = request.form['contestemail']
            details = request.form['details']
            
            send_entry(guess, contestemail, details)
            show_modal = True
           
    return render_template('index.html', taf = '{:,}'.format(round(totalAcresFlown, 2)), li = linked, show_modal = show_modal, tcs = '{:,}'.format(tcs))

@app.route('/login/<error>', methods=['GET', 'POST'])
def login(error):#we put the username and client in session variables in this step
    
    if error == "go":
        error = None
    
    if request.method == 'POST':
        try:
            with ndbclient.context():
                query = secureAccount.query().filter(secureAccount.username == request.form['username'])
                for key in query.iter(keys_only=True):
                    entity = key.get()
    
                    if (sha256_crypt.verify(request.form['password'], entity.password) == True):
                        
                        # put the client name and username in the session variable so we can access it from the 
                        # next page, too (dashboard)
                        session['client'] = entity.client
                        session['username'] = request.form['username']
                        
                        tz = timezone('EST')
                        easternTimeNow = datetime.datetime.now(tz)
                        
                        # This is a csv string that will go into the database, its structure is as follows:
                            
                        # username, logintime, ipaddress, os, browser
                        
                        # This info will be pulled out and displayed on the admin portal of the 
                        # website
                        loginInfoString = []
                        loginInfoString.append(request.form['username'] + "," + easternTimeNow.strftime("%m-%d-%Y at %H:%M:%S EST") + "," + str(request.remote_addr) + "," + request.user_agent.platform + "," + request.user_agent.browser)
                                               
                        loginRecordEntity = ndb.Key(loginRecord, "login").get()
                        loginRecordEntity.login_record = loginRecordEntity.login_record + loginInfoString
                        loginRecordEntity.put()
                        
                        login_user(entity, remember=True)
                        
                        v = request.form['version']
                        if v == "simple":
                            
                            return redirect(url_for('portal', which = "simplePortal.html"))
                        
                        if v == "static":
                        
                            return redirect(url_for('portal', which = "staticPortal.html"))
                        
                        if v == "responsive":
                            
                            return redirect(url_for('portal', which = "portal.html"))
                else:
                    error = 'Invalid Credentials.'
        except:
            error = 'That username does not exist.'
            
    return render_template('login.html', error=error)

@app.route('/adminLogin/<error>', methods=['GET', 'POST'])
def adminLogin(error):
    
    if error == "go":
        error = None
    
    if request.method == 'POST':
        try:
            with ndbclient.context():
                query = secureAccount.query().filter(secureAccount.username == request.form['username'])
                for key in query.iter(keys_only=True):
                    entity = key.get()
        
                    if (sha256_crypt.verify(request.form['password'], entity.password) == True):
                        
                        # put the client name and username in the session variable so we can access it from the 
                        # next page, too (dashboard)
                        session['client'] = entity.client
                        session['username'] = request.form['username']
                        
                        login_user(entity, remember=True)
                            
                        return redirect(url_for('adminPortal'))
               
                else:
                    error = 'Invalid Credentials.'
        except:
            error = 'That username does not exist.'
            
    return render_template('adminLogin.html', error=error)

@app.route('/adminPortal', methods=['GET', 'POST'])
@login_required
def adminPortal():
    
    allRecordsForPage = dict({})
    
    with ndbclient.context():
    
        loginRecordEntity = ndb.Key(loginRecord, "login").get()
        allRecords = loginRecordEntity.login_record
        # this 'allRecords' is a bunch of csv strings in a list
        # username, logintime, ipaddress, os, browser
        
        for r in range(0, len(allRecords)):
            # here we make a list of one of those csv strings
            thisRowOfLogins = allRecords[r].split(",")
            
            theseAllRecordsForPage = dict({})

            # then we put that list into a dictionary
            theseAllRecordsForPage.update({"username": thisRowOfLogins[0]})
            theseAllRecordsForPage.update({"login_time": thisRowOfLogins[1]})
            theseAllRecordsForPage.update({"ip_address": thisRowOfLogins[2]})
            theseAllRecordsForPage.update({"os": thisRowOfLogins[3]})
            theseAllRecordsForPage.update({"browser": thisRowOfLogins[4]})        
            
            # then we put that dictionary into a bigger dictionary
            allRecordsForPage.update({str(r): theseAllRecordsForPage})
    
    return render_template('adminPortal.html', allRecordsForPage = json.dumps(allRecordsForPage))

@app.route('/portal/<which>', methods=['GET', 'POST'])
@login_required
def portal(which):
    
    client = session['client']
    
    if client == "Braga":
        owner = "Peter Cling"
        companyName = "Braga Fresh/ASA Organics"
        cropType = "O Broccoli"
    elif client == "BetterWorld":
        owner = "B. Moore"
        companyName = "Better World Farms, LLC"
        cropType = "Broccoli"
    elif client == "TAndA":
        owner = "Mr. T"
        companyName = "T & A"
        cropType = "Lettuce"
    elif client == "ChurchBrothers":
        owner = "Josh Ruiz"
        companyName = "Church Brothers"
        cropType = "Romaine"
    
    comparisonStartDate = "7/1/2020"
    comparisonEndDate = dateTimeToString(date.today())
    comparisonDateOfChange = dateTimeToString(date.today() - datetime.timedelta(days = 7))
    comparison_activities = ["Cultivation", "Roboweeder", "Sidedress", "Weeding", "Planting"]
    
    futureDate = dateTimeToString(date.today() + datetime.timedelta(days = 14))
    
    existingNotifications = ""
    notes = None
    
    historicalDataChecked = False
    currentOrAll = "Currently planted"
    
    startDate = datetime.date(2020, 7, 1)
    #endDate = datetime.date(2020, 7, 10)

    endDate = date.today()
    ranchesToView = ["All"]
    
    
    modalChecks = dict({})
    viewPreferenceChecks = dict({})
    
    # If the user is in the simple portal, they have the option to customize their dashboard view
    # All their preferences are stored in the database between logins.
    # Let's get their view preferences here, so we can pass them into the front end
    
    with ndbclient.context():
        
        # The view preferences might not exist yet, so try and get it
        # If there's an error, it means it doesn't exist, so create it.
        try:
            entity = ndb.Key(viewPreferences, session['username']).get()
        except:
            create_view_preferences(session['username'])
        finally:
        
            viewPreferenceChecks.update({"expectedCountW": entity.expectedCountW})
            viewPreferenceChecks.update({"actualCountW": entity.actualCountW})
            viewPreferenceChecks.update({"totalCurrentLossW": entity.totalCurrentLossW})
            viewPreferenceChecks.update({"flyoverNotesW": entity.flyoverNotesW})
            viewPreferenceChecks.update({"lossTrendW": entity.lossTrendW})
            viewPreferenceChecks.update({"lossOverTimeW": entity.lossOverTimeW})
            viewPreferenceChecks.update({"topFiveW": entity.topFiveW})
            viewPreferenceChecks.update({"contributingActivitiesW": entity.contributingActivitiesW})
            viewPreferenceChecks.update({"contributingActivitiesChartW": entity.contributingActivitiesChartW})
            viewPreferenceChecks.update({"eventsPieChartW": entity.eventsPieChartW})
            viewPreferenceChecks.update({"eventsChartW": entity.eventsChartW})
            viewPreferenceChecks.update({"eventsOverTimeW": entity.eventsOverTimeW})
            viewPreferenceChecks.update({"ndviAverageW": entity.ndviAverageW})
            viewPreferenceChecks.update({"ndviAverageByEventW": entity.ndviAverageByEventW})
            viewPreferenceChecks.update({"ndviAveragePerDateW": entity.ndviAveragePerDateW})
            viewPreferenceChecks.update({"ndviChangeW": entity.ndviChangeW})
            viewPreferenceChecks.update({"ndviOverTimeW": entity.ndviOverTimeW})
    
    show_feedback_modal = False
    
    trending = ""
    
    if request.method == "GET":
        
        error = None
  
        gottenEntities, ranches_for_ui = getEntitiesAndRanchesToView(client, startDate, endDate, ranchesToView, "DateFlown", historicalDataChecked)
        
        land_acres, acres_flown, expected_crops, latest_crop_count, \
        crops_lost, percent_missing, percent_missing_table, overall_table, \
        crops_lost_per_date_flown, top_five_ranch_crops_lost, \
        top_five_ranch_crops_lost_as_percent, bottom_five_ranch_crops_lost, \
        bottom_five_ranch_crops_lost_as_percent, crops_lost_for_simple_portal = getCountData(gottenEntities, client)
        
        if (which == "simplePortal.html"):
            
#            with ndbclient.context():
#        
#                entity = ndb.Key(lossTrend, client).get()
#                trending = entity.loss_trend
            
            trending = getTrend(client, ranchesToView, endDate)
            
        # just put the crops saved figure into the cropsSaved database entry here real quick
        # ONLY if the number is bigger than last time
        cropsSavedInteger = int((float(land_acres.replace(',', "")) * 44000) * .05)
        with ndbclient.context():
            entity = ndb.Key(cropsSaved, "saved").get()
            if cropsSavedInteger > entity.saved:
                entity.saved = cropsSavedInteger
                entity.put()
                
            # While we have nbdclient context, let's check if the ranch report feedback has already been gotten
            # if it hasn't, populate the modal and show it
            try:
                
                entity = ndb.Key(ranchReportPreferences, session['username']).get()
                if entity.asked == False:
                    show_feedback_modal = True
                    
                modalChecks.update({"lossData": entity.currentPastLost})
                modalChecks.update({"lossTrend": entity.lossTrend})
                modalChecks.update({"topFive": entity.fiveBestPerforming})
                modalChecks.update({"bottomFive": entity.fiveWorstPerforming})
                modalChecks.update({"healthData": entity.stressHealthData})
                modalChecks.update({"contributingActivities": entity.activitiesData})
                modalChecks.update({"additional": entity.anythingElse})
                
            except:
                
                pass
            
        
        rateOfLossChart = getRateOfChangeData(gottenEntities, client, "count")
        event_rateOfLossChart = getRateOfChangeData(gottenEntities, client, "events")
        
        event_analysis_table, event_analysis_pie_chart, fictitious_events, targetValues = getEventAnalysisData(gottenEntities, client)
        
        ndvi_average, ndvi_acres_flown, ndvi_event_and_average_table, \
        ndvi_overall_table, ndvi_score_per_date, ndvi_changes = getStressData(gottenEntities)
        
        stressOverTimeChart = getStressOverTimeData(gottenEntities, client)

        acres_flown_per_date_flown = getActivityData(gottenEntities)
        
        comparison_cards = getComparisonsCards(client)

        planning_patches = getPlanningData()
        
        existingNotifications = getNotificationsData(client)
        existingAlerts = getAlertsData(client)
        
        notes = getNotes(gottenEntities, client)
        
        with ndbclient.context():
            entity = ndb.Key(lastUpdated, client).get()
            updated = entity.date

        return render_template(which, client = client, \
                                   owner = owner, companyName = companyName, cropType = cropType, \
                                   error = error, u = updated, \
                                   currentTab = "Overview", \
                                   start_date = dateTimeToString(startDate), \
                                   end_date = dateTimeToString(endDate), \
                                   land_acres = land_acres, \
                                   acres_flown = acres_flown, \
                                   expected_crops = expected_crops, \
                                   latest_crop_count = latest_crop_count, \
                                   crops_lost = crops_lost, \
                                   crops_lost_for_simple_portal = crops_lost_for_simple_portal, \
                                   percent_missing = percent_missing, \
                                   trending = trending, \
                                   percent_missing_table = percent_missing_table, \
                                   overall_table = overall_table, \
                                   rateOfLossChart = rateOfLossChart, \
                                   crops_lost_per_date_flown = crops_lost_per_date_flown, \
                                   top_five_ranch_crops_lost = top_five_ranch_crops_lost, \
                                   eventAnalysisTable = event_analysis_table, \
                                   eventAnalysisPieChart = event_analysis_pie_chart, \
                                   fictitious_events = fictitious_events, \
                                   event_rateOfLossChart = event_rateOfLossChart, \
                                   targetValues = targetValues, \
                                   NDVIAverage = ndvi_average, \
                                   NDVIAcresFlown = ndvi_acres_flown, \
                                   PackagedNDVIEventAndAverage = ndvi_event_and_average_table, \
                                   PackagedNDVIOverall = ndvi_overall_table, \
                                   AverageNDVIScorePerDate = ndvi_score_per_date, \
                                   stressOverTimeChart = stressOverTimeChart, \
                                   AcresFlownPerDateFlown = acres_flown_per_date_flown, \
                                   ranchesForUi = ranches_for_ui, \
                                   top_five_ranch_crops_lost_as_percent = top_five_ranch_crops_lost_as_percent, \
                                   NDVIChanges = ndvi_changes, \
                                   bottom_five_ranch_crops_lost = bottom_five_ranch_crops_lost, \
                                   bottom_five_ranch_crops_lost_as_percent = bottom_five_ranch_crops_lost_as_percent, \
                                   comparisonStartDate = comparisonStartDate, \
                                   comparisonEndDate = comparisonEndDate, \
                                   comparisonDateOfChange = comparisonDateOfChange, \
                                   cropsForComparison = ["Broccoli"], \
                                   activitiesForComparison = comparison_activities, \
                                   ComparisonCards = comparison_cards, \
                                   patchesAndInfo = planning_patches, \
                                   futureDate = futureDate, \
                                   existingNotifications = existingNotifications, \
                                   existingAlerts = existingAlerts, \
                                   show_feedback_modal = show_feedback_modal, \
                                   modal_checks = json.dumps(modalChecks), \
                                   view_preference_checks = json.dumps(viewPreferenceChecks), \
                                   notes = notes, \
                                   historicalDataChecked = historicalDataChecked, \
                                   currentOrAll = currentOrAll)

    if request.method == "POST":
        
        error = None
        
        tabShowing = request.form['tabShowing']
                    
        
        if request.form['typeOfPost'] == "filter":
            startDate = toDateTime(request.form['startDate'])
            endDate = toDateTime(request.form['endDate'])
            ranchesToView = request.form.getlist('rtv[]')
            
            # If the historical data checkbox was checked, we should have gotten a one-value list from
            # the above variable assignment--it will be ['historicalData'].
            # Also, however, the list may be empty, so we'll use a try-catch statement here
            
    
            if 'historicalData' in request.form:
                historicalDataChecked = True
                currentOrAll = "Current and historical"
            else:
                historicalDataChecked = False
            
        if request.form['typeOfPost'] == "show_all":
            startDate = toDateTime(request.form['startDate'])
            endDate = toDateTime(request.form['endDate'])
            ranchesToView = ["All"]           
            
                    
        if request.form['typeOfPost'] == "addEvent":
            eventToAdd = request.form['fictitiousEventName']
            percentToAdd = request.form['fictitiousEventPercent']
            
            with ndbclient.context():
                create_user_defined_event(client, eventToAdd, percentToAdd)
                
        if request.form['typeOfPost'] == "deleteEvent":
            e = request.form['fictitiousEventName']
            p = request.form['fictitiousEventPercent']   
            
            with ndbclient.context():

                query = userDefinedEvent.query().filter(ndb.StringProperty("client") == client).filter(ndb.StringProperty("event") == e).filter(ndb.FloatProperty("percent") == float(p))
                for key in query.iter(keys_only=True):
                    key.delete()    
                    
        if request.form['typeOfPost'] == "setTargets":
            
            targetEvents = ['cultivation', 'roboweeder', 'weeding', 'weather', 'sidedress', 'planting', 'disease']
            targetValues = []
            
            for event in range(0, len(targetEvents)):
                formID = targetEvents[event] + "Target"
                targetValues.append(request.form[formID])
            
            with ndbclient.context():
                for event in range(0, len(targetEvents)):
                    thisKey = client + targetEvents[event]
                    # If the entity exists already, it gets updated
                    try:
                        entity = ndb.Key(targetLossPercent, thisKey).get()
                        entity.target_percent = float(targetValues[event])
                        entity.put()
                    # If it doesn't it gets created with a 0.0 value
                    except:
                        create_target_loss_percent(client, targetEvents[event], 0.0)
            
        if request.form['typeOfPost'] == "updateWeeklyRanchReport":
        
            checks = request.form.getlist('items')
            additional = request.form['additional']

            with ndbclient.context():
                # The client wants to update their ranch report preferences.
                # All the selected checks are in the checks variable, and any random additional
                # requests are in the additional variable.
                try:
                    
                    entity = ndb.Key(ranchReportPreferences, session['username']).get()
                    
                    checksList = ["lossData", "lossTrend", "topFive", "bottomFive", "healthData", "contributingActivities"]
                    boolsList = [False, False, False, False, False, False]
                                        
                    # go through each check and update the database with the results
                    for c in range(0, len(checks)):
                        
                        boolsList[checksList.index(checks[c])] = True
                        
                    entity.currentPastLost = boolsList[0]
                    entity.lossTrend = boolsList[1]
                    entity.fiveBestPerforming = boolsList[2]
                    entity.fiveWorstPerforming = boolsList[3]
                    entity.stressHealthData = boolsList[4]
                    entity.activitiesData = boolsList[5]
    
                    # everything has been updated, we can now set the 'asked' variable to "true"
                    # so the customer is not asked again
                    entity.asked = True
                    entity.put()
                    
                    # now we send the email to myself to notify me that a ranch report 
                    # customization-request has come in
                    send_ranch_report_customization_request(session['username'], checks, additional)
                                            
                except:
                    
                    pass           
        
        
        gottenEntities, ranches_for_ui = getEntitiesAndRanchesToView(client, startDate, endDate, ranchesToView, "DateFlown", historicalDataChecked)
        
        
        land_acres, acres_flown, expected_crops, latest_crop_count, \
        crops_lost, percent_missing, percent_missing_table, overall_table, \
        crops_lost_per_date_flown, top_five_ranch_crops_lost, \
        top_five_ranch_crops_lost_as_percent, bottom_five_ranch_crops_lost, \
        bottom_five_ranch_crops_lost_as_percent, crops_lost_for_simple_portal = getCountData(gottenEntities, client)
        
        if (which == "simplePortal.html"):
            
#            with ndbclient.context():
#        
#                entity = ndb.Key(lossTrend, client).get()
#                trending = entity.loss_trend
            
            trending = getTrend(client, ranchesToView, endDate)
        
        rateOfLossChart = getRateOfChangeData(gottenEntities, client, "count")
        event_rateOfLossChart = getRateOfChangeData(gottenEntities, client, "events")
        
        event_analysis_table, event_analysis_pie_chart, fictitious_events, targetValues = getEventAnalysisData(gottenEntities, client)
        
        ndvi_average, ndvi_acres_flown, ndvi_event_and_average_table, \
        ndvi_overall_table, ndvi_score_per_date, ndvi_changes = getStressData(gottenEntities)
        
        stressOverTimeChart = getStressOverTimeData(gottenEntities, client)

        acres_flown_per_date_flown = getActivityData(gottenEntities)
        
        comparison_cards = getComparisonsCards(client)

        planning_patches = getPlanningData()
        
        existingNotifications = getNotificationsData(client)
        existingAlerts = getAlertsData(client)
        
        notes = getNotes(gottenEntities, client)
            
        with ndbclient.context():
            entity = ndb.Key(lastUpdated, client).get()
            updated = entity.date

        return render_template(which, client = client, \
                                   owner = owner, companyName = companyName, cropType = cropType, \
                                   error = error, u = updated, \
                                   currentTab = tabShowing, \
                                   start_date = dateTimeToString(startDate), \
                                   end_date = dateTimeToString(endDate), \
                                   land_acres = land_acres, \
                                   acres_flown = acres_flown, \
                                   expected_crops = expected_crops, \
                                   latest_crop_count = latest_crop_count, \
                                   crops_lost = crops_lost, \
                                   crops_lost_for_simple_portal = crops_lost_for_simple_portal, \
                                   percent_missing = percent_missing, \
                                   trending = trending, \
                                   percent_missing_table = percent_missing_table, \
                                   overall_table = overall_table, \
                                   rateOfLossChart = rateOfLossChart, \
                                   crops_lost_per_date_flown = crops_lost_per_date_flown, \
                                   top_five_ranch_crops_lost = top_five_ranch_crops_lost, \
                                   eventAnalysisTable = event_analysis_table, \
                                   eventAnalysisPieChart = event_analysis_pie_chart, \
                                   fictitious_events = fictitious_events, \
                                   event_rateOfLossChart = event_rateOfLossChart, \
                                   targetValues = targetValues, \
                                   NDVIAverage = ndvi_average, \
                                   NDVIAcresFlown = ndvi_acres_flown, \
                                   PackagedNDVIEventAndAverage = ndvi_event_and_average_table, \
                                   PackagedNDVIOverall = ndvi_overall_table, \
                                   AverageNDVIScorePerDate = ndvi_score_per_date, \
                                   stressOverTimeChart = stressOverTimeChart, \
                                   AcresFlownPerDateFlown = acres_flown_per_date_flown, \
                                   ranchesForUi = ranches_for_ui, \
                                   top_five_ranch_crops_lost_as_percent = top_five_ranch_crops_lost_as_percent, \
                                   NDVIChanges = ndvi_changes, \
                                   bottom_five_ranch_crops_lost = bottom_five_ranch_crops_lost, \
                                   bottom_five_ranch_crops_lost_as_percent = bottom_five_ranch_crops_lost_as_percent, \
                                   comparisonStartDate = comparisonStartDate, \
                                   comparisonEndDate = comparisonEndDate, \
                                   comparisonDateOfChange = comparisonDateOfChange, \
                                   cropsForComparison = ["Broccoli"], \
                                   activitiesForComparison = comparison_activities, \
                                   ComparisonCards = comparison_cards, \
                                   patchesAndInfo = planning_patches, \
                                   futureDate = futureDate, \
                                   existingNotifications = existingNotifications, \
                                   existingAlerts = existingAlerts, \
                                   show_feedback_modal = show_feedback_modal, \
                                   modal_checks = json.dumps(modalChecks), \
                                   view_preference_checks = json.dumps(viewPreferenceChecks), \
                                   notes = notes, \
                                   historicalDataChecked = historicalDataChecked, \
                                   currentOrAll = currentOrAll)

def toBool(v):
    
    if v == "true":
        return True
    return False

@app.route('/updateViewPreferences', methods=['GET', 'POST'])
def updateViewPreferences():
    
    if request.method == 'POST':
        
        with ndbclient.context():

            entity = ndb.Key(viewPreferences, session['username']).get()
            entity.expectedCountW = toBool(request.form['expectedCountW'])
            entity.actualCountW = toBool(request.form['actualCountW'])
            entity.totalCurrentLossW = toBool(request.form['totalCurrentLossW'])
            entity.flyoverNotesW = toBool(request.form['flyoverNotesW'])
            entity.lossTrendW = toBool(request.form['lossTrendW'])
            entity.lossOverTimeW = toBool(request.form['lossOverTimeW'])
            entity.topFiveW = toBool(request.form['topFiveW'])
            entity.contributingActivitiesW = toBool(request.form['contributingActivitiesW'])
            entity.contributingActivitiesChartW = toBool(request.form['contributingActivitiesChartW'])
            entity.eventsPieChartW = toBool(request.form['eventsPieChartW'])
            entity.eventsChartW = toBool(request.form['eventsChartW'])
            entity.eventsOverTimeW = toBool(request.form['eventsOverTimeW'])
            entity.ndviAverageW = toBool(request.form['ndviAverageW'])
            entity.ndviAverageByEventW = toBool(request.form['ndviAverageByEventW'])
            entity.ndviAveragePerDateW = toBool(request.form['ndviAveragePerDateW'])
            entity.ndviChangeW = toBool(request.form['ndviChangeW'])
            entity.ndviOverTimeW = toBool(request.form['ndviOverTimeW'])
            entity.put()

    status_code = Response(status=200)
    return status_code

@app.route('/chartsToImages', methods=["GET", "POST"])
def chartsToImages():
    
    if request.method == 'POST':

        with ndbclient.context():
            
            client = request.form['client']
            
            entity = ndb.Key(chartImages, client).get()
            entity.eventsPieChart = request.form['eventsPieChart']
            entity.put()
            
    status_code = Response(status=200)
    return status_code









        
        
        
        

@app.route('/deleteComparison', methods=['GET', 'POST'])
def deleteComparison():
    
    ComparisonCards = ""
    
    if request.method == 'POST':
        
        title = request.form['title']
        text = request.form['text']
        client = request.form['client']
            
        with ndbclient.context():
            
            # Here we get all the saved comparison cards to populate the 'Comparisons' tab
            query = comparisonCard.query().filter(ndb.StringProperty("client") == str(client))
            for key in query.iter(keys_only=True):
                entity = key.get()
                
                if entity.title == title and entity.text == text:
                    key.delete()
                else:
                
                    if "Positive change" in entity.title:
                        thisTitle = entity.title.replace("Positive change", "<span style='color:green'>Positive change</span>")
                    else:
                        thisTitle = entity.title.replace("Ineffective change", "<span style='color:orange'>Ineffective change</span>")
                    
                    ComparisonCards = ComparisonCards + "<div class='card'> \
        	     			<div class='comparison-card'> \
        				    	<div class='comparison-card-container'> \
        					    	<div class='comparison-title'>" + thisTitle + "</div> \
        						    <div class='comparison-text'>" + entity.text + "</div> \
                                     <input type='button' class='dashboard-button' onclick=\"deleteComparison('" + entity.title + "', '" + entity.text + "')\" value='delete'> \
                                <div> \
        			    	</div> \
        	    		</div>"
                    
        return render_template('comparisonCardStack.html', ComparisonCards = ComparisonCards)

@app.route('/saveComparison', methods=['GET', 'POST'])
def saveComparison():

    ComparisonCards = ""
    
    if request.method == 'POST':
        
        title = request.form['title']
        text = request.form['text']
        client = request.form['client']
            
        with ndbclient.context():
            create_new_comparison_card(client, title, text)
            
            # Here we get all the saved comparison cards to populate the 'Comparisons' tab
            query = comparisonCard.query().filter(ndb.StringProperty("client") == str(client))
            for key in query.iter(keys_only=True):
                entity = key.get()
                
                if "Positive change" in entity.title:
                    thisTitle = entity.title.replace("Positive change", "<span style='color:green'>Positive change</span>")
                else:
                    thisTitle = entity.title.replace("Ineffective change", "<span style='color:orange'>Ineffective change</span>")
                
                ComparisonCards = ComparisonCards + "<div class='card'> \
    	     			<div class='comparison-card'> \
    				    	<div class='comparison-card-container'> \
    					    	<div class='comparison-title'>" + thisTitle + "</div> \
    						    <div class='comparison-text'>" + entity.text + "</div> \
                                 <input type='button' class='dashboard-button' onclick=\"deleteComparison('" + entity.title + "', '" + entity.text + "')\" value='delete'> \
                            <div> \
    			    	</div> \
    	    		</div>"
                    
        return render_template('comparisonCardStack.html', ComparisonCards = ComparisonCards)

@app.route('/compare', methods=['GET', 'POST'])
def compare():
    
    if request.method == 'POST':
        
        client = request.form['client']
        comparisonCrop = request.form['crop']
        comparisonPlantingMethod = request.form['plantingMethod']
        comparisonActivity = request.form['activity']
        comparisonStartDate = toDateTime(request.form['comparisonStartDate'])
        comparisonEndDate = toDateTime(request.form['comparisonEndDate'])
        comparisonDateOfChange = toDateTime(request.form['comparisonDateOfChange'])
        CdForAxisMarkerOne = fromDateTime(comparisonDateOfChange)
        CdForAxisMarkerTwo = fromDateTime(toDateTime(request.form['comparisonDateOfChange']) + datetime.timedelta(days = 1))
        comparisonNote = request.form['comparisonNote']
        
        ranchesToView = request.form.getlist('ranches[]')
        
        gottenEntities, ranches_for_ui = getEntitiesAndRanchesToView(client, comparisonStartDate, comparisonEndDate, ranchesToView, "DateFlown", True)
        
        comparison_line_chart, comparison_bar_chart, \
        comparison_message, comparison_note, comparison_activities, \
        comparison_cards = getComparisonData(client, comparisonStartDate, comparisonEndDate, comparisonCrop, comparisonPlantingMethod, comparisonActivity, comparisonDateOfChange, comparisonNote, gottenEntities, ranchesToView)
        
        return render_template('comparisonArea.html', \
                               client = client, \
                               comparisonStartDate = dateTimeToString(comparisonStartDate), \
                               comparisonEndDate = dateTimeToString(comparisonEndDate), \
                               comparisonDateOfChange = dateTimeToString(comparisonDateOfChange), \
                               CdForAxisMarkerOne = CdForAxisMarkerOne, \
                               CdForAxisMarkerTwo = CdForAxisMarkerTwo, \
                               comparisonLineChart = comparison_line_chart, \
                               comparisonBarChart = comparison_bar_chart, \
                               comparisonMessage = comparison_message, \
                               comparisonNote = comparison_note, \
                               cropsForComparison = ["Broccoli"], \
                               activitiesForComparison = comparison_activities, \
                               comparisonActivity = comparisonActivity, \
                               ComparisonCards = comparison_cards)

@app.route('/createNotification', methods=['GET', 'POST'])
def createNotification():  
    
    Notifications = ""
    
    if request.method == 'POST':
        
        client = request.form['client']
        ranchesString = request.form['ranches']
        emailString = request.form['email']
        
        with ndbclient.context():
            create_email_notification(client, emailString, ranchesString)
            
            # Now we have to create (if not created already) a ranchReportsPreferences entity in the database,
            # one for each email address in the string
            for e in range(0, len(emailString.split(" - "))-1):
                create_ranch_report_preferences(emailString.split(" - ")[e])
            
            
            # Here we get all the saved comparison cards to populate the 'Comparisons' tab
            query = emailNotification.query().filter(ndb.StringProperty("client") == str(client))
            for key in query.iter(keys_only=True):
                entity = key.get()
                
                Notifications = Notifications + "<div class='card'> \
    	     			<div class='notification-card'> \
    				    	<div class='notification-card-container'> \
    					    	<div class='notification-title'><span style='color:OrangeRed'><b>Recipients:</b></span> " + entity.email + "</div> \
    						    <div class='notification-text'><span style='color:OrangeRed'><b>Ranches included in report:</b></span> " + entity.ranches + "</div> \
                                 <input type='button' class='dashboard-button' onclick=\"deleteNotification('" + entity.ranches + "', '" + entity.email + "')\" value='delete'> \
                            </div> \
    			    	</div> \
    	    		</div>"
        
        
        return render_template('existingNotificationStack.html', existingNotifications = Notifications)

@app.route('/deleteNotification', methods=['GET', 'POST'])
def deleteNotification():  
    
    Notifications = ""
    
    if request.method == 'POST':
        
        client = request.form['client']
        ranchesString = request.form['ranches']
        emailString = request.form['email']
        
        with ndbclient.context():
        
            # Here we get all the saved notifications, then delete the one in question
            query = emailNotification.query().filter(ndb.StringProperty("client") == str(client))
            for key in query.iter(keys_only=True):
                entity = key.get()
                
                if entity.ranches == ranchesString and entity.email == emailString:
                    key.delete()
                    
                    # As we're deleting the notification, we should also delete the notification preferences
                    for e in range(0, len(emailString.split(" - "))-1):
                        ndb.Key(ranchReportPreferences, emailString.split(" - ")[e]).delete()
                        
                else:
                
                    Notifications = Notifications + "<div class='card'> \
        	     			<div class='notification-card'> \
        				    	<div class='notification-card-container'> \
        					    	<div class='notification-title'><span style='color:OrangeRed'><b>Recipients:</b></span> " + entity.email + "</div> \
        						    <div class='notification-text'><span style='color:OrangeRed'><b>Ranches included in report:</b></span> " + entity.ranches + "</div> \
                                     <input type='button' class='dashboard-button' onclick=\"deleteNotification('" + entity.ranches + "', '" + entity.email + "')\" value='delete'> \
                                </div> \
        			    	</div> \
        	    		</div>"
        
        
        return render_template('existingNotificationStack.html', existingNotifications = Notifications)

@app.route('/createAlert', methods=['GET', 'POST'])
def createAlert():  
    
    Alerts = ""
    
    if request.method == 'POST':
        
        client = request.form['client']
        ranchesString = request.form['ranches']
        emailString = request.form['email']
        conditionsString = request.form['conditions']
        
        with ndbclient.context():
            create_email_alert(client, emailString, ranchesString, conditionsString)
            
            # Here we get all the saved comparison cards to populate the 'Comparisons' tab
            query = emailAlert.query().filter(ndb.StringProperty("client") == str(client))
            for key in query.iter(keys_only=True):
                entity = key.get()
                
                Alerts = Alerts + "<div class='card'> \
    	     			<div class='alert-card'> \
    				    	<div class='alert-card-container'> \
    					    	<div class='alert-title'><span style='color:#bd4271'><b>Recipients:</b></span> " + entity.email + "</div> \
    						    <div class='alert-text'><span style='color:#bd4271'><b>Ranches included in alert:</b></span> " + entity.ranches + "</div> \
                                <div class='alert-text'><span style='color:#bd4271'><b>Condition(s):</b></span> " + entity.conditions + "</div> \
                                 <input type='button' class='dashboard-button' onclick=\"deleteAlert('" + entity.ranches + "', '" + entity.email + "')\" value='delete'> \
                            </div> \
    			    	</div> \
    	    		</div>"
        
        
        return render_template('existingAlertStack.html', existingAlerts = Alerts)

@app.route('/deleteAlert', methods=['GET', 'POST'])
def deleteAlert():  
    
    Alerts = ""
    
    if request.method == 'POST':
        
        client = request.form['client']
        ranchesString = request.form['ranches']
        emailString = request.form['email']        
        
        with ndbclient.context():
            
            # Here we get all the saved comparison cards to populate the 'Comparisons' tab
            query = emailAlert.query().filter(ndb.StringProperty("client") == str(client))
            for key in query.iter(keys_only=True):
                entity = key.get()
                
                if entity.ranches == ranchesString and entity.email == emailString:
                    key.delete()
                else:
                
                    Alerts = Alerts + "<div class='card'> \
        	     			<div class='alert-card'> \
        				    	<div class='alert-card-container'> \
        					    	<div class='alert-title'><span style='color:#bd4271'><b>Recipients:</b></span> " + entity.email + "</div> \
        						    <div class='alert-text'><span style='color:#bd4271'><b>Ranches included in alert:</b></span> " + entity.ranches + "</div> \
                                    <div class='alert-text'><span style='color:#bd4271'><b>Condition(s):</b></span> " + entity.conditions + "</div> \
                                     <input type='button' class='dashboard-button' onclick=\"deleteAlert('" + entity.ranches + "', '" + entity.email + "')\" value='delete'> \
                                </div> \
        			    	</div> \
        	    		</div>"
        
        
        return render_template('existingAlertStack.html', existingAlerts = Alerts)

    

@app.route('/planning', methods=['GET', 'POST'])
def planning():  
    
    return render_template('planningPractice.html')

   
    
    






















    
if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True, threaded=True)