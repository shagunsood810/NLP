#!/usr/bin/env python
# coding: utf-8

# In[1]:


############################################################################################

#Importing the necessary packages 
import nltk
import random
import re
from nltk.tokenize import word_tokenize, RegexpTokenizer
from nltk.tag import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk import FreqDist

#Dictionary used to expand contractions in input text
CONTRACTION_DICT = {
                "aren't": "are not",
                "there's": "there is",
                "can't": "can not",
                "they'd": "they had",
                "couldn't": "could not",
                "they'll": "they will",
                "didn't": "did not",
                "they're": "they are",
                "doesn't": "does not",
                "they've": "they have",
                "i'd": "I had",
                "where's": "where is",  
                "i'm": "I am",
                "who'd": "who had",
                "i've": "I have",
                "who'll": "who will",
                "what's": "what is"
            }

#Words banks for different categories of feelings to generate appropriate replies
HAPPY_BANK = ["good", "well", "happy", "wonderful", "cheerful", "contented", "delighted", "ecstatic", "elated", "glad", "joyful", "joyous"]

SAD_BANK = ["worry", "worried", "pain", "painful", "unhappy", "sad", "down", "low", "low-spirited", "tragic", "depressed", "depressing", "dismal", "grievous", "deplorable" ,"bad", "lamentable", "sorry", "terrible", "awful"]

DANGER_BANK = ["suicide", "kill", "hurt", "murder", "die"]

POSITIVE_BANK = ["yes", "true", "right", "correct"]

NEGATIVE_BANK = ["no","not", "wrong", "incorrect", "false","hate"]


#Dictionary used to swap the pronouns in the input for Eliza's reply
PRONOUN_SWAP = {"i":"you", 
                "me":"you",
                "my":"your", 
                "you":"me",
                "your":"my"
            }

#Dictionaries for responses given by Eliza when a word matches in the corresponding word bank.
happy_responses = {
                1: "I'm glad to hear you are feeling that way. Is everything else going well?",
                2: "That is a good way to be. Is this how you usually feel?",
                3: "Is there anything in particular that is making you feel that way?"
            } 

sad_responses = {
                1: "I'm sorry to hear you are feeling that way.  What is troubling you?",
                2: "That isn't great. Is something bothering you?",
                3: "Is there anything in particular that is making you feel that way?"
            }

positive_responses = {
                1: "You seem very positive.",
                2: "Are you sure?",
                3: "You are pretty confident."
            } 

negative_responses = {
                1: "You seem very negative.",
                2: "Are you sure?",
                3: "That sounds pretty definite."
            }

#Initiating output and conversation initiator variables
conversation_initated = ''
output = ''

"""
 Method: remove_punc
 Input: string
 Output: string
 This function removes punctuation from a string.
"""
def remove_punc(text):
    tokenizer = RegexpTokenizer(r'\w+')
    no_punc = tokenizer.tokenize(text.lower())
    return ' '.join(no_punc)

"""
 Method: tokenize_words
 Input: string
 Output: list
 This function tokenizes the words in the string
 and returns them in a list.
"""
def tokenize_words(text):
    words = nltk.word_tokenize(text)
    return words

"""
 Method: remove_stop_words
 Input: list
 Output: list
 This function removes stop words from the list.
"""
def remove_stop_words(words):
    stops = set(stopwords.words('english'))
    no_stops = []
    # iterate through the tokenized words and rmove stop words
    for word in words:
        # if the word is not a stop word, append it to the list
        if word not in stops:
            no_stops.append(word)
    return no_stops

"""
 Method: clean
 Input: string
 Output: list
 This function removes punctuation, tokenizes the words,
 and removes the stop words.
"""
def clean(text):
    
    # remove punctuation
    text = remove_punc(text)
    
    # tokenize words
    words = tokenize_words(text)
    
    return words

"""
 Method: check_for_danger
 Input: string
 Output: string
 This function performs word spotting for ech 
 'dangerous' word as identified in the DANGER_BANK.
 If one of these words is spotted, a set response 
 is returned as a string.
"""
def check_for_danger(text):
    words = clean(text)
    # iterate through the tokenized words
    for word in words:
        #if the word is in the danger bank, return the following string
        if word in DANGER_BANK:
            return "I'm concerned you are thinking about that. Perhaps you should call 911."
    return ''

"""
 Method: process_name
 Input: string
 Output: string
 This function takes a string, performs word spotting
 for common phrases when stating one's name and 
 removes them. It strips white space, capitalizes,
 and returns the name inputted.
"""
def process_name(text):
    #Removing contractions and punctuations in the input
    text = remove_contractions(text)
    text = remove_punc(text)    
    
    #checking for introduction phrases using regex
    if re.match(r'.*(my name is |i am |i am called |i go by ).*',text):
        text = re.sub(r'.*(my name is|i am|i am called|i go by) (.+)', r'\2', text)
    
    #Returning the name with first letter capitalized.
    return text.capitalize()

"""
 Method: process_feeling
 Input: string
 Output: string
 This function takes a string and performs word 
 spotting for words in the word banks. 
 If found, a response is randomly selected from the 
 appropriate bank.
"""
def process_feeling(text):
    # clean the text
    feelings = clean(text)
    # generate random number
    randomNum = random.randrange(1, 3) 
    # iterate through the tokenized words
    for word in feelings:
        # check negative bank
        if word in POSITIVE_BANK:
            # get random positive response from positive responses dictionary
            return positive_responses.get(randomNum)
        # check negative bank
        elif word in NEGATIVE_BANK:
            # get random negative response from negative responses dictionary
            return negative_responses.get(randomNum)
        # check the happy bank
        elif word in HAPPY_BANK:
            # get random happy response from happy responses dictionary
            return happy_responses.get(randomNum)
        # check sad bank
        elif word in SAD_BANK:
            # get random sad response from sad responses dictionary
            return sad_responses.get(randomNum)
    #Returns a generic reply if none of the above conditions generate a reply
    return("Tell me more.")

"""
 Method: check_for_gibberish
 Input: string
 Output: boolean
 This function takes a string, cleans the text and 
 using tokenized words it checks if the input given is
 meaningful or not.
"""        
def check_for_gibberish(text):
    words = clean(text)
    words = remove_stop_words(words) 
    # iterate through the tokenized words
    for word in words:
        # the word is not found in the library, return true
        if not wordnet.synsets(word): 
            return True
    return False

"""
 Method: swap_pronouns
 Input: string
 Output: string
 This function takes a string and replaces any pronouns
 (keys) found in the prounoun swap object with key value 
 pairs, with their corresponding pronoun (value).
""" 
def swap_pronouns(text):
    words = tokenize_words(text)
    newText = []
    # iterate through the tokenized words
    for word in words:
        found = False
        # iterate through the pronoun swap items
        for key, value in PRONOUN_SWAP.items():
            # if found, append value 
            if word == key:
                newText.append(value)
                found = True
        # if the pronoun is not found, append the original word
        if found == False:
            newText.append(word)  
    return ' '.join(newText)

"""
 Method: remove_contractions
 Input: string
 Output: string
 This function takes a string and replaces any contractions
 (keys) found in the contraction dict object with key value 
 paris, with their corresponding equivalent (value) without 
 contractions.
""" 
def remove_contractions(text):
    text = text.lower()
    words = text.split()
    newText = []
    # iterate through the tokenized words
    for word in words:
        found = False
        # iterate through the pronoun swap items
        for key, value in CONTRACTION_DICT.items():
            # if found, append value
            if word == key:
                newText.append(value)
                found = True
        # if the contraction is not found, append the original word
        if found == False:
            newText.append(word)           
    return ' '.join(newText)

"""
 Method: spot_word
 Input: string
 Output: boolean
 This function takes a string, cleans the text and 
 uses the tokenized words to check if the words are 
 present in any of the word banks. If matched, it returns true, else returns false.
""" 
def spot_word(text):
    words = clean(text)
    # iterate through the tokenized words
    for word in words:
        #Checking if the word is present in any of the word banks
        if word in HAPPY_BANK or word in SAD_BANK or word in POSITIVE_BANK or word in NEGATIVE_BANK:
            return True
    return False

"""
 Method: initiate_conversation
 Input: string
 Output: string
 This function takes a string and passes it to process_name to
 extract the user's name.  It formulates a response with the user's
 name embedded and additionally asks a question.
""" 
def initiate_conversation(text):
    # Reply to the user with their name and ask how the user is doing 
    global userName 
    userName = process_name(text)
    
    if not userName or text == ' ':
        return ""
    elif re.match(r'[A-z]', userName):
        return "Hi " + userName + ". How are you feeling?"
    else:
        return ""

"""
 Method: process_response
 Input: string
 Output: string
 This function takes a string and formulates a question based upon
 user input using word spotting or regular expression matching following
 this order: 
 1) check for exit words  
 2) check for danger words
 3) Word spotting
 4) Sentence transformation
 5) check for a one word answer 
 6) check for gibberish 
 7) check for a particularly lengthy answer.
"""     
def process_response(text):
    #Pre-processing the input 
    text = remove_contractions(text)
    text = remove_punc(text)
    words = clean(text)
    
    #Check if the user wants to quit and respond with a closing sentence.
    if re.match(r'.*(bye|quit|exit).*', text):
        return "Bye. Have a nice day!"
    
    # check for 'danger' words
    danger = check_for_danger(text)
    if danger:
        return danger
    
    # check for regular expression matches and respond with a question
    if re.match(r'(I|i) want\b([\sA-z]+)*', text):
        x = re.match(r'(I|i) want\b([\sA-z]+)*', text)
        return 'Why do you want' + x[2] + '?'
    elif re.match(r'(I|i) (can not|cannot)\b([\sA-z]+)*', text):
        x = re.match(r'(I|i) (can not|cannot)\b([\sA-z]+)*', text)
        return "Why can't you" + x[3] + "?" 
    elif re.match(r'(I|i).*you', text):
        x = swap_pronouns(text)
        return "Why do " + x + "?"
    elif re.match(r'(I am|I|i|i am)\s(feeling|feel)\s([\sA-z]+)*', text) or spot_word(text):
        return process_feeling(text)
    
    # tokenize the words
    words = nltk.word_tokenize(text)
    
    # check for a lengthy answer
    if len(words) > 15:
        return "Could you restate that?"
    
    # check for gibberish/non sensical words
    if check_for_gibberish(text) == True:
        return "I am not sure I understand. Could you elaborate?"   
    
    # check for a one word answer
    if len(words) == 1:
        return "Tell me more about that."

    return "Could you expand on that?"

# greet the user and ask for their name
print("[Eliza] Hello! I am Eliza, your psychotherapist for the day. What is your name?")

# collect the input
response = input('[User] ')

# while response is not "quit" or "bye" or "exit" continue to the conversation
while not re.match(r'.*(quit|bye|exit).*',response.lower()):
    #Checking if conversation was initiated
    if not conversation_initated:
        #Looping until the conversation is initiated
        while not conversation_initated:
            output = initiate_conversation(response)
            #If conversation is initiated set the conversation_intitiated variable
            if output:
                conversation_initated = 'Y'
            #If there was no output from initiate_response method then asking to re-enter name
            else:
                output = "I didn't get your name. Could you please enter your name again?"
                print('[Eliza] ' + output)
                response = input('[User] ')
                
    else:
        #Taking the user input to continue conversation
        if not userName.strip(): 
            text = 'User' 
        else: 
            text = userName
        response = input('['+ text +'] ')
        #Calling the process_response method to generate a response
        output = process_response(response)
    
    #Printing the response of Eliza
    print('[Eliza] ' + output)

#If user wants to quit immediately, respond with a closing sentence.
if not output:
    print('[Eliza] Bye. Have a nice day!')

        
    

