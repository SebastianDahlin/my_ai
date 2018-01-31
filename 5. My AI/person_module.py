import nltk
import pickle
import wikipedia
import data_handler


def is_number(number):
    '''This function returns True if argument is a number, False otherwise'''
    try:
        int(number)
        return True
    except ValueError:
        return False

def find_occurences(string, character):
    '''This function returns the place of a specific character in a string'''
    return [i for i, letter in enumerate(string) if letter == character]

def wikipedia_lookup(name):
    '''This function returns a wikipedia page object and handles ambiguity'''
    good = False
    while not good:
        try:
            wiki_page = wikipedia.page(name)
            good = True
        except wikipedia.exceptions.DisambiguationError as e:
            alternative = e.options
            for i in enumerate(alternative):
                print(str(i) + ". "+ alternative[i])
            name = -1
            while name not in range(0, len(alternative)):
                name = int(input("Select an alternative: "))
            wiki_page = wikipedia.page(alternative[name])
            good = True
        except wikipedia.exceptions.PageError:
            print("Found nothing on person.")
            wiki_page = ""
            break
    return wiki_page


def person_info(name): 
    '''This function gets information and returns information about a person as an object'''
    person = Person() # Create an object of the person class
    person = data_handler.check_and_read_from_db(name, person) # Check if name exists in db and in that case returns a populated person object
    if person.full_name != "":
        return person
    else:
        print("Looking up information on wikipedia for %s" % (name))
        subject = wikipedia_lookup(name)
        if subject == "":
            return person
        else:
            person.full_name = subject.title
            wiki_summary = subject.summary
            person.summary = subject.summary
            sent_tokenized = nltk.sent_tokenize(wiki_summary)
            word_tokenized = nltk.word_tokenize(wiki_summary)
            first_sentence = sent_tokenized[0]
            last_bracket_list = find_occurences(first_sentence, ")")
            birth_year_sent = first_sentence[first_sentence.find("(")+1:last_bracket_list[-1]]
            word_list = nltk.word_tokenize(birth_year_sent)
            num_list = list([w for w in word_list if is_number(w)])
            num_list = [w for w in num_list if int(w) > 1000 and int(w) < 2050]
            num_list.sort()
            person.birth_year = int(num_list[0])

            #### Decide the gender
            he_count = list([w for w in word_tokenized if w == "he"])
            she_count = list([w for w in word_tokenized if w == "she"])
            if len(he_count) > len(she_count):
                person.set_gender("male")
            else:
                person.set_gender("female")
            if len(num_list) > 1 and birth_year_sent.count("–") > 0:
                person.death_year = int(num_list[1])
                person.deceased = True

            if person.full_name == "Tom Hanks":
                with open('ex_people.pkl', 'wb') as output:
                    tom_hanks = person
                    pickle.dump(tom_hanks, output, pickle.HIGHEST_PROTOCOL)
                del tom_hanks


            ##Return the person class object
            data_handler.data_table_people(person)
            return person
    
class Person:
    '''This class holds information about the person'''
    def __init__(self):
        self.full_name = ""
        self.first_name = ""
        self.last_name = ""
        self.birth_year = ""
        self.birth_place = ""
        self.death_year = ""
        self.death_place = ""
        self.gender = ""
        self.gender_nick = ""
        self.deceased = False
        self.summary = ""

    def set_gender(self, gender):
        '''This function sets the gender and also the gender nick'''
        self.gender = gender
        if gender == "male":
            self.gender_nick = "he"
        else:
            self.gender_nick = "she"
