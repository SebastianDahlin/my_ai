import datetime
import time
import nltk
import person_module
from geotext import GeoText

'''Trying to update git from the HP'''

# Classes
class Question:
    '''This class holds information about the given question'''
    def __init__(self):
        self.kind = []
        self.adjective = []
        self.verb = []
        self.person = ""
        self.country = []
        self.city = []
        self.time = ""
        self.company = ""
        self.bool = False

#Functions
# def process_content(question):
#     '''This function takes a string and returns a list of tuples {word, nltk definition}'''
#     word_list = nltk.word_tokenize(question)
#     tagged = nltk.pos_tag(word_list)
#     return tagged

def for_print(sents):
    '''This function takes string(s) and prints proper capitalized sentences'''
    sent_list = nltk.sent_tokenize(sents)
    concat_sents = ""
    for sent in sent_list:
        concat_sents += sent[0].capitalize() + sent[1:] + " "
    print(concat_sents)
 
def fill_quest(quest, user_input):
    '''This function looks in the tags of the analysed sentence and fills the quest object'''
    # Create a word list from user input
    word_list = nltk.word_tokenize(user_input)
    # Check each word if they are a city or country (Since GeoText is broken!)
    for word in word_list:
        place = GeoText(word)
        if place.cities:
            quest.city = place.cities
        if place.countries:
            quest.country = place.countries
    # Remove country and city names and put them in the quest object
    word_list = [word for word in word_list if word not in quest.city + quest.country]
    # Tagg the remaining list with nltk postagger
    tagged = nltk.pos_tag(word_list)


    try:
        for tag in tagged:
            print(tag)
            if tag[1] in ["WRB", "WP"]:
                quest.kind = tag
                print(str(tag[1]))
            if tag[1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
                quest.verb.append(tag[0])
            if tag[1] in ["JJ", "VB"]:
                quest.adjective.append(tag[0])
            if tag[1] in ["NN", "NNP"]:
                if quest.person == "":
                    quest.person = tag[0]
                else:
                    quest.person += " " + tag[0]
    except Exception as exception:
        print(str(exception)) 

    if (tagged[0][0]).lower() in ["is", "was", "were", "has", "have"]:
            quest.bool = True
            print("Bool question: %s" % (quest.bool))

def analyse_and_answer(quest):
    '''This function analyses the quest object'''
    print(quest.kind)
    #People questions
    if quest.person != "":
        person = person_module.person_info(quest.person)
        if quest.kind and quest.kind[1] == "WP": # Who is person question.
            who_is_person(person)
        if quest.kind and quest.kind[1] == "WRB": # How or When person question
            if quest.kind[0].lower() == "how":
                how_is_person(quest, person)
            if quest.kind[0].lower() == "when":
                when_is_person(quest, person)
        if quest.bool is True: # Boolean person question.
            boolean_person(quest, person)

###Below are all special def cases for answers
def who_is_person(person):
    '''This function prints the summary of a person'''
    print(person.summary)
def how_is_person(quest, person):
    '''This function respondes to how questions'''
    if "old" or "age" or "born" in quest.adjective:
        if "born" in quest.adjective and person.birth_year != "":
            for_print("%s was born the year %s." % (person.full_name, person.birth_year))
        if "age" or "old" in quest.adjective:
            for i in quest.adjective:
                print(i)
            if person.deceased is False and person.birth_year != "":
                for_print("%s is %s years old." % (person.full_name, (datetime.datetime.now().year - person.birth_year)))
            if person.deceased is True:
                for_print("%s is deceased, died in %s, at an age of %s." %(person.full_name, person.death_year, (person.death_year-person.birth_year)))
def when_is_person(quest, person):
    '''This function responds to when questions'''
    if "born" in quest.verb or quest.adjective:
        for_print("%s was born the year %s." %(person.full_name, person.birth_year))
    if "die" in quest.verb or quest.adjective:
        if person.deceased is True:
            for_print("%s died in %s" % (person.full_name, person.death_year))
        if person.deceased is False:
            for_print("%s is alive and is %s years old." % (person.full_name, (datetime.datetime.now().year - person.birth_year)))
def boolean_person(quest, person):
    '''This function responds to yes/no questions with the correct statement'''
    if "dead" or "alive" in quest.adjective:
        if "dead" or "alive" in quest.adjective:
            if person.deceased is True:
                if "dead" in quest.adjective:
                    statement = "yes"
                else:
                    statement = "no"
                for_print("%s, %s is deceased. %s died in %s, at an age of %s." % (statement, person.full_name, person.gender_nick, person.death_year, (person.death_year-person.birth_year)))
            if person.deceased is False:
                if "alive" in quest.adjective:
                    statement = "yes"
                else:
                    statement = "no"
                for_print("%s, %s is alive. %s was born in %s and is currently %s years old." % (statement, person.full_name, person.gender_nick, person.birth_year, (datetime.datetime.now().year - person.birth_year)))
    

#Main program
def main():
    '''This is the main program'''
    user_input = input("Ask a question: ")
    quest = Question()
    fill_quest(quest, user_input)
    analyse_and_answer(quest)
if __name__ == "__main__":
    main()
    