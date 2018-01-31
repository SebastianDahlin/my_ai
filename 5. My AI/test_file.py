'''This file containts the tests for all functions'''
import pickle
import my_ai_main
import person_module

#Import example Tom Hanks from pickle
with open('ex_people.pkl', 'rb') as input:
    PERSON = pickle.load(input)

# def test_process_content():
#     assert my_ai_main.process_content("How old is Tom Hanks?") != ""

def test_find_occurences():
    assert person_module.find_occurences("Charlie Parker","(") == []
    assert person_module.find_occurences("Charlie Parker (1921-1954)","(") == [15]
    assert person_module.find_occurences("Charlie Parker (1921-1954)",")") == [25]

def test_is_number():
    assert person_module.is_number("3") is True
    assert person_module.is_number("3.4") is False
    assert person_module.is_number("M") is False
    
def test_who_is_person(capsys):
    my_ai_main.who_is_person(PERSON)
    out = capsys.readouterr()
    assert out != ""
    