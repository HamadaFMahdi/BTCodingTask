# BT Coding Task
Essentially, I was required to code up a program that would recieve notifications in a stream from different nodes then be able to deduce the status of the nodes. These notifications would indicate the current status of a node either explicitly or implicitly. 

There are two versions of the program based on my two different interpretations of the task, more specifically my interpretation of how to interpret ambiguous notifications.

### If you can only choose one of these, please choose Version B.

## Version A

In this version, I print an unknown notification line whenever an ambiguous notification is identified, even if the node status becomes apparent later on. 

## Version B

In this version, I print an unknown notification only if a node has an unknown status after processing the entire input.

## My general assumptions 

Essentially the code takes each notification and checks if the node that sent the notification exists in nodeNamesTracker. If it doesn't then it adds it else it will update the status. If the notification contains an implicit node it will do the same for the implicit node.
With regards to the ambiguous notifications, I assumed that since the node times are syncronised to within 50 milliseconds of each other then if we recieve 2 notifications about a node, one implying that it is ALIVE and the other implying it is DEAD or visa versa and they were created by 2 DIFFERENT nodes, then if the notifications were created within 50 milliseconds of each other we can't be sure which one was created first thus deeming the notification ambiguous.
Also, I assumed that the Monitoring System Time Stamps on the nodes must be in ascending order.

## To run the program please use the command line: 
## $ python NodeUpdaterSystemB.py inputfile.txt


### Apologies, I did not have time to code up a test.py where I test the programs out. I have run my own manual tests however so they do work based on the assumptions I have given
