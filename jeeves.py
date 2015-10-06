import webbrowser  #import webbrowser so we can access websites
import logging
import os
#################################################################################################################### loading phase
def load():
    print "#!# Opening res.txt..."
    try:
        temp=open("res.txt","r")
        print "#+# Opened res.txt"
        dictionary=organize(temp)
        temp.close()
        return dictionary
    except IOError as e:
        logging.Logger.error(e)
        raise
    

def organize(item):
    dictionary={}  #empty dictionary in which we store website shortcut name and link
    info=item.read().splitlines()  #I think this is pretty much self explanatory
    for line in info:  #we break the document to lines, filter spaces and separate bookmark name with bookmark link
        if " " in line == True:
            line.remove(" ")
        bookmark = line.split(",") #we collect raw data and start saving it to a dictionary
        assert len(bookmark)==2, "Invalid raw bookmark length"
        dictionary[bookmark[0]]=bookmark[1] #[0] is for bookmark name and [1] for link
    return dictionary
        
######################################################################################################################            
def workflow():
    dictionary=load()  #we load some resources we'll need later
    while True:
        print "#!# Can I help you sir?"
        print "#?#",
        order=raw_input()
        if order=="":
            print "#!# Exiting..."
            break
        order=order.split()
        if order[0]!="help":  #we have to explicitly ask for help because it's len is 1 so it would return an error at the line below
            try:
                command,arg=order[0],order[1]  #we separate command and argument
            except:
                print "Invalid instructions!"
                continue
            if command=="mb":
                print "#!# Enter web address you want to bind to this bookmark"
                print "#?#",
                addr=raw_input()
                dictionary=makeBookmark(dictionary, arg, addr)
            elif command=="ob":
                openBookmark(dictionary,arg)
            elif command=="mbg":
                makeBookmarkGroup(arg)
            elif command=="obg":
                openBookmarkGroup(arg)
        else:
            help()
##################################################SINGLE BOOKMARK COMMANDS####################################################################
def makeBookmark(dictionary=dict,name=str,addr=str):
    dictionary[name]=addr
    output=""
    stream=open("res.txt","w")
    for key in dictionary:
        output+=key+","+dictionary[key]+"\n"
    stream.write(output)
    stream.close()
    print "#+# Bookmarking complete"
    return dictionary

def openBookmark(dictionary=dict,name=str):
    if name in dictionary:
        webbrowser.open(dictionary[name])
    else:
        print "#-# Bookmark not in the database"
        
################################################################################################################################################
    

def help():
    print "#!# Opening help..."
    try:
        help=open("help.txt","r").read()
        print help
    except IOError as e:
        logging.Logger.error(e)
        raise
    
#####################################################BOOKMARK GROUP COMMANDS###################################################################
def makeBookmarkGroup(name):
    output=""
    print "#!# Press enter after each website"
    print "#!# Press enter on blank to stop and save"
    print "#!# Start entering websites:"
    print "#?#",
    website=raw_input()
    try:
        stream=open(os.path.join("groups",name+".txt"),"w")
    except IOError as e:
        logging.Logger.error(e)
        raise
    while website!="":
        output+=website+"\n"
        print "#!# %s added"%website
        print "#?#",
        website=raw_input()
    else:
        print "#!# No further instructions sent. Saving websites to bookmark file..."
        try:
            stream.write(output)
            print "#!# Successfully saved!"
        except IOError as e:
            print "#-# Write failed!"
            logging.Logger.error(e)
            raise
        
    stream.close()
def openBookmarkGroup(name):
    print "#!# Attempting to open %s"%name
    try:
        stream=open(os.path.join("groups",name+".txt"),"r").read().splitlines()
        print "#+# Bookmark found! Opening links..."
    except IOError as e:
        print "#-# Bookmark not found, try making one!"
        return
    for link in stream:
        webbrowser.open(link)
###############################################################################################################################################    
workflow()