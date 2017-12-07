#ASSUMPTIONS
#Essentially the code takes each notification and checks if the node that sent
#the notification exists in nodeNamesTracker. If it doesn't then it adds it
#else it will update the status. If the notification contains an implicit nodes
#it will do the same for the implicit node.
#With regards to the ambiguous notifications, I assumed that since the node times
#are syncronised to within 50 milliseconds of each other then if we recieve 2 notifications
#about a node, one implying that it is ALIVE and the other implying it is DEAD
#or visa versa and they were created by 2 DIFFERENT nodes, then if the notifications
#were created within 50 milliseconds of each other we can't be sure which one was created first
#thus deeming the notification ambiguous.
#Also, if we have multiple ambiguous notifications in a row then I assumed that
#they will all give an ambiguous result.

#ASSUMPTIONS for B:
#In this version I print "UNKNOWN NOTIFICATION" at the end once I know
#that a notification resulted in an UNKNOWN status for a node.

import sys

def monitoringSystemTimeStampIsValid(notification):
    mSTimeStamp = notification[0]
    if(len(mSTimeStamp)==13 and mSTimeStamp.isdigit()):
        return True
    else:
        return False

def nodeTimeStampIsValid(notification):
    nodeTimeStamp = notification[1]
    if(len(nodeTimeStamp)==13 and nodeTimeStamp.isdigit()):
        return True
    else:
        return False

def isAValidShortNotification(notification):
    eventDetail = notification[3]
    if(len(notification)==4 and eventDetail=="HELLO"):
        return True
    else:
        return False

def isAValidLongNotification(notification):
    eventDetail = notification[3]
    if((len(notification)==5 and eventDetail=="LOST") or (len(notification)==5 and eventDetail=="FOUND")):
        return True
    else:
        return False

def inputIsValid(notification):
  #First checking if the time stamps are valid
  if(monitoringSystemTimeStampIsValid(notification) and nodeTimeStampIsValid(notification)):
      if(isAValidShortNotification(notification)):
        return True
      elif(isAValidLongNotification(notification)):
        return True
  else:
    return False

def changeInStatus(nodeNameIndex, statusWillNowBe):
    currentStatus = nodeStatusTracker[nodeNameIndex][1]
    if (currentStatus != statusWillNowBe):
        return True
    else:
        return False

def updateNode(notification, nodeNameIndex, statusWillNowBe, detailsOfEvent):
    latestMSTimeStamp = notification[0]
    latestNodeTimeStamp = notification[1]
    oldStatus = 1
    oldMSTimeStamp = 2
    oldDetailsOfEvent = 3
    oldNodeTimeStamp = 4
    nodeStatusTracker[nodeNameIndex][oldStatus] = statusWillNowBe
    nodeStatusTracker[nodeNameIndex][oldMSTimeStamp] = latestMSTimeStamp
    nodeStatusTracker[nodeNameIndex][oldDetailsOfEvent] = detailsOfEvent
    nodeStatusTracker[nodeNameIndex][oldNodeTimeStamp] = latestNodeTimeStamp

def nodeChecker(notification, nodeNameToUpdate, statusWillNowBe, detailsOfEvent):
  nodeName = notification[nodeNameToUpdate]
  #This try method with the .index function I took from online. I did'nt know
  #how to catch the error when the index did't exist. In JavaScript it would usually
  #return -1.
  try:
    nodeNameIndex=nodeNamesTracker.index(nodeName)
  except ValueError:
    mSTimeStamp = notification[0]
    nodeTimeStamp = notification[1]
    nodeNamesTracker.append(nodeName)
    #The node time stamo has been appended to help check for ambiguity.
    nodeStatusTracker.append([nodeName, statusWillNowBe, mSTimeStamp, detailsOfEvent, nodeTimeStamp])
  else:
    if not changeInStatus(nodeNameIndex, statusWillNowBe):
        updateNode(notification, nodeNameIndex, statusWillNowBe, detailsOfEvent)
    elif changeInStatus(nodeNameIndex, statusWillNowBe):
        #Now we will check for ambiguity
        oldNodeTimeStamp = 4
        previousEventIndex = 3
        previousSourceNodeIndex = 0
        latestNodeTimeStamp = 1
        #This part is to make sure that the previous source node and the
        #current source node are not the same. Otherwise it wouldn't be ambiguous
        previousEvent = nodeStatusTracker[nodeNameIndex][previousEventIndex]
        previousEvent_splitted = previousEvent.split(" ")
        detailsOfEvent_splitted = detailsOfEvent.split(" ")
        previousSourceNode = previousEvent_splitted[0]
        currentSourceNode = detailsOfEvent_splitted[0]

        tSFromPreviousNotificationNode = int(nodeStatusTracker[nodeNameIndex][oldNodeTimeStamp])
        tSFromCurrentNotificationNode = int(notification[latestNodeTimeStamp])
        #This is my assumption. If two nodes send a notification about another
        #node, one saying that he is ALIVE and the other saying he is DEAD
        #or visa versa. Then if the nodes were created within 50 milliseconds of each other
        #then we can't be sure which one was created first thus deeming the notification ambiguous.
        if((tSFromCurrentNotificationNode - tSFromPreviousNotificationNode < 50) and (currentSourceNode != previousSourceNode)):
            updateNode(notification, nodeNameIndex, "UNKNOWN", detailsOfEvent)
            #In this version I print this whenever a notification is deemed
            #ambiguous even if the node status is known after progressing through
            #the rest of the notifications.
        else:
            updateNode(notification, nodeNameIndex, statusWillNowBe, detailsOfEvent)

#The notification events come in two types.
def definingTheDetailsOfEvent(notification):
    sourceNode = notification[2]
    event = notification[3]
    if(isAValidShortNotification(notification)):
       return sourceNode + " " + event
    elif(isAValidLongNotification(notification)):
       implicitNode = notification[4]
       return sourceNode + " " + event + " " + implicitNode

def aNodeWasFound(notification):
    event = notification[3]
    return True if event == "FOUND" else False

def aNodeWasLost(notification):
    event = notification[3]
    return True if event == "LOST" else False

def statusWillNowBeDeterminer(notification):
  detailsOfEvent = definingTheDetailsOfEvent(notification)
  #It will update for the source node as this is alive in all cases
  sourceNode = 2
  statusWillNowBe = "ALIVE"
  nodeChecker(notification, sourceNode ,statusWillNowBe ,detailsOfEvent)
  #If it is a longer notification it will update for the implicit node
  if(isAValidLongNotification(notification)):
    implicitNode = 4
    if(aNodeWasFound(notification)):
      statusWillNowBe = "ALIVE"
      nodeChecker(notification, implicitNode, statusWillNowBe, detailsOfEvent)
    elif(aNodeWasLost(notification)):
      statusWillNowBe = "DEAD"
      nodeChecker(notification, implicitNode, statusWillNowBe, detailsOfEvent)

def useNodeTimeStamp(notification):
    nodeTimeStamp = notification[1]
    return int(nodeTimeStamp)


def nodeStatuses():
    #Using ":4" to remove the node Time Stamp at the end of the node statuses
    #The node Time Stamp was appended (line 48) to check for ambiguity in nodeChecker
    return "\n".join(map(lambda x: " ".join(x[:4]), nodeStatusTracker))


#MAIN

nodeNamesTracker = []

#This array will contain the output
nodeStatusTracker = []

#Reading from an input text file which is inputed as an argument in the command line
#I also took this concept from online. I didn't know how to read from a file
# or allow it to be placed as an argument in the command line.
file = open(sys.argv[1], 'r')
notificationsStream = file.readlines()

#Removing the '\n' that appears when extracting the data from the file
for x in range(len(notificationsStream)):
    notificationsStream[x]=notificationsStream[x].replace("\n","")

notificationsStream_splitted = map(lambda x: x.split(" "), notificationsStream)

#Validating inputs
#Checking that the Monitoring system's time stamps are in ascending order
if not mSTimeStampsInAscendingOrder(notificationsStream_splitted):
    sys.exit("Monitoring System's Time Stamps not in order")
#validating that each notification is in the correct format
for notification in notificationsStream_splitted:
    if not inputIsValid(notification):
        sys.exit("Invalid Notification Found")

#I wanted the notifications sorted using the node times so that I can check for
#ambiguity later.
#I took the concept of using a function as a key in .sort from online.
notificationsStream_splitted.sort(key=useNodeTimeStamp)

#After each notification I update the status of the nodes if anything has changed.
for notification in notificationsStream_splitted:
    statusWillNowBeDeterminer(notification)

for node in nodeStatusTracker:
    status = node[1]
    if(status=="UNKNOWN"):
        print "UNKNOWN NOTIFICATION"

print nodeStatuses()
