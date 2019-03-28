'''
Copyright (c) 2019 Python Forensics and Chet Hosmer

Permission is hereby granted, free of charge, to any person obtaining a copy of this software
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial 
portions of the Software.

 ProperNames Demonstration
 Version 1.3
 January 2019

 Requirement: Python 2.7.x

 usage:
 stdin | python properNames.py 

 Script will process the piped data

'''

''' LIBRARY IMPORT SECTION '''

# import standard module sys
import sys

# import the regular expression library in order to filter out unwanted characters
import re

# import datetime method from Standard Library
from datetime import datetime

''' STOP WORDS LIST DEFINITION SECTION '''

# COMMON STOP WORDS LIST
# What are stop_words: Words which are typically filtered 
# out when processing natural language data (text)
# feel free to add additional words to the list

STOP_WORDS =["able","about","above","accordance","according",
            "accordingly","across","actually","added","affected",
            "affecting","affects","after","afterwards","again",
            "against","almost","alone","along","already","also",
            "although","always","among","amongst","announce",
            "another","anybody","anyhow","anymore","anyone",
            "anything","anyway","anyways","anywhere","apparently",
            "approximately","arent","arise","around","aside",
            "asking","auth","available","away","awfully","back",
            "became","because","become","becomes","becoming",
            "been","before","beforehand","begin","beginning",
            "beginnings","begins","behind","being",
            "believe","below","beside","besides","between",
            "beyond","both","brief","briefly","came","cannot",
            "cause","causes","certain","certainly","come",
            "comes","contain","containing","contains","could",
            "couldnt","date","different","does","doing","done",
            "down","downwards","during","each","effect","eight",
            "eighty","either","else","elsewhere","end",
            "ending","enough","especially","even","ever",
            "every","everybody","everyone","everything",
            "everywhere","except","fifth","first","five",
            "followed","following","follows","former","formerly",
            "forth","found","four","from","further",
            "furthermore","gave","gets","getting",
            "give","given","gives","giving","goes",
            "gone","gotten","happens","hardly","has","have",
            "having","hence","here","hereafter","hereby",
            "herein","heres","hereupon","hers","herself",
            "himself","hither","home","howbeit","however",
            "hundred","immediate","immediately","importance",
            "important","indeed","index","information",
            "instead","into","invention","inward","itself",
            "just","keep","keeps","kept","know","known",
            "knows","largely","last","lately","later","latter",
            "latterly","least","less","lest","lets","like",
            "liked","likely","line","little","look","looking",
            "looks","made","mainly","make","makes","many",
            "maybe","mean","means","meantime","meanwhile",
            "merely","might","million","miss","more","moreover",
            "most","mostly","much","must","myself","name",
            "namely","near","nearly","necessarily","necessary",
            "need","needs","neither","never","nevertheless",
            "next","nine","ninety","nobody","none","nonetheless",
            "noone","normally","noted","nothing","nowhere",
            "obtain","obtained","obviously","often","okay",
            "omitted","once","ones","only","onto","other",
            "others","otherwise","ought","ours","ourselves",
            "outside","over","overall","owing","page","pages",
            "part","particular","particularly","past","perhaps",
            "placed","please","plus","poorly","possible","possibly",
            "potentially","predominantly","present","previously",
            "primarily","probably","promptly","proud","provides",
            "quickly","quite","rather","readily","really","recent",
            "recently","refs","regarding","regardless",
            "regards","related","relatively","research",
            "respectively","resulted","resulting","results","right",
            "run","said","same","saying","says","section","see",
            "seeing","seem","seemed","seeming","seems","seen",
            "self","selves","sent","seven","several","shall",
            "shed","shes","should","show","showed","shown",
            "showns","shows","significant","significantly",
            "similar","similarly","since","slightly","some",
            "somebody","somehow","someone","somethan",
            "something","sometime","sometimes","somewhat",
            "somewhere","soon","sorry","specifically","specified",
            "specify","specifying","still","stop","strongly",
            "substantially","successfully","such","sufficiently",
            "suggest","sure","take","taken","taking","tell",
            "tends","than","thank","thanks","thanx","that",
            "thats","their","theirs","them","themselves","then",
            "thence","there","thereafter","thereby","thered",
            "therefore","therein","thereof","therere",
            "theres","thereto","thereupon","there've","these",
            "they","think","this","those","thou","though","thought",
            "thousand","through","throughout","thru","thus",
            "together","took","toward","towards","tried","tries",
            "truly","trying","twice","under","unfortunately",
            "unless","unlike","unlikely","until","unto","upon",
            "used","useful","usefully","usefulness","uses","using",
            "usually","value","various","very","want","wants",
            "was","wasnt","welcome","went","were","what","whatever",
            "when","whence","whenever","where","whereafter","whereas",
            "whereby","wherein","wheres","whereupon","wherever",
            "whether","which","while","whim","whither","whod",
            "whoever","whole","whom","whomever","whos","whose",
            "widely","will","willing","wish","with","within","without",
            "wont","words","world","would","wouldnt",
            "your","youre","yours","yourself","yourselves"] 

''' DEFINING PSUEDO CONSTANTS SECTION '''

# PSUEDO CONSTANTS, Feel Free to change the minimum and maximum name length
MIN_SIZE = 4      # Minimum length of a proper name
MAX_SIZE = 20     # Maximum length of a proper name

''' EXTRACT PROPER NAMES SECTION '''

def ExtractProperNames(theString, dictionary):
    ''' Input String to search, Output Dictionary of Proper Names '''
    
    # Extract each continuous string of characters
    
    wordList = theString.split()
    
    # Now, let's determine which words are possible proper names
    #     and create a list of them.

    '''
    For this example words are considered possible proper names if they are 
    1) Title case
    2) Meet the minimum and maximum length criteria
    3) The word is NOT in the stop word list
    
    The Python built in string method string.istitle() is used to identify title case
    '''
    
    for eachWord in wordList:
        
        if eachWord.istitle() and len(eachWord) >= MIN_SIZE and len(eachWord) <= MAX_SIZE and eachWord.lower() not in STOP_WORDS:
            
            '''
            if the word meets the specified conditions it is added to the properNamesDictionary
            '''
            try:
                # if the word exists in the dictionary then 
                # add 1 to the occurances 
                cnt = properNamesDictionary[eachWord]
                properNamesDictionary[eachWord] = cnt + 1
            except:
                # If the word is not yet in the dictionary
                # add it and set the number of occurances to 1
                properNamesDictionary[eachWord] = 1
        else:
            # otherwise loop to the next possible word
            continue
    
    # the function returns the created properNamesDictionary
    
    return properNamesDictionary

# End Extract Proper Names Function

''' MAIN PROGRAM ENTRY SECTION '''

'''
Main program for Extract Proper Names
'''
if __name__ == "__main__":
    
    ''' Main Program Entry Point '''
    
    print("\nPython Proper Name Extraction ")
    print("Python Forensics, Inc. \n")
    print("Script Started", str(datetime.now()))
    print()

    # Create empty dictionary
    properNamesDictionary = {}
    
    for eachLine in sys.stdin:
        
        txt = re.sub("[^A-Za-z']", ' ', eachLine)
    
        '''
        Call the ExtractProperNames function which returns
        a Python dictionary of possible proper names along with
        the number of occurances of that name.
             
        This function performs all the heavy lifting of extracting out
        each possible proper name
        
        '''
        properNamesDictionary = ExtractProperNames(txt, properNamesDictionary)

    # Once all the standard input lines are read
    # the value is the number of occurrences of the proper name
    
    # This approach will print out the possible proper names with
    # the highest occurrence first

    ''' PRINT RESULTING POSSIBLE PROPER NAMES SECTION '''

    print()

    for eachName in sorted(properNamesDictionary, key=properNamesDictionary.get, reverse=True):
        print('%4d'  % properNamesDictionary[eachName],end="")
        print( '%20s' % eachName)
    
    print("\n\nScript Ended", str(datetime.now()))
    print()
    

# End Main Function

