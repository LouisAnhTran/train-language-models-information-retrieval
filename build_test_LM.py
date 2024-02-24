#!/usr/bin/python3

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from decimal import Decimal # this module enable more robust handling of decimals number in Python to get around small probabilistic numbers issues

import re
import nltk
import sys
import getopt
import copy

# this variable can be set dynamically to create language models with different N and complexity
N_GRAM=4

def build_LM(in_file):
    """
    build language models for each label
    each line in in_file contains a label and a string separated by a space
    """
    print("building language models...")
    print(f'The input file name is: {in_file}')

    # This is an empty method
    # Pls implement your code below
    with open(in_file,'r',encoding='utf-8') as file:
        language_models=convert_file_to_dict_language_models(file)
        return language_models

# this function takes in an input string and return a list of N-gram units
def convert_string_to_list_of_terms(input_string):
    return [tuple(input_string[i:i+4]) for i in range(len(input_string)-N_GRAM+1)]

# this function takes in all lines of input file and return a dictionary with the keys being the unique terms in all lines
def dict_of_all_unique_terms_all_languages(lines):
    result_dict={}
    for line in lines:
        line=line.strip() # remove punctuation
        index_first_space=line.find(" ") # find the index of first space, so we can split the label
        list_of_term=convert_string_to_list_of_terms(line[index_first_space+1:])
        for item in list_of_term:
            if item not in result_dict:
                result_dict[item]=0
    return result_dict

# this function takes in an input file and return language models
def convert_file_to_dict_language_models(file):
    language_models={}
    lines=file.readlines()
    dict_all_unique_terms=dict_of_all_unique_terms_all_languages(lines)

    for line in lines:
        line=line.strip() # remove punctuation
        index_first_space=line.find(" ") # find the index of first space, so we can split the label
        language=line[:index_first_space] # get the language of the line
        if language not in language_models: 
            language_models[language]=copy.deepcopy(dict_all_unique_terms) # we must use deep copy, otherwise the change in one model will be reflected in other models
        list_of_term=convert_string_to_list_of_terms(line[index_first_space+1:])
        for term in list_of_term:
            language_models[language][term]=language_models[language][term]+1 # update the term occurences in that line

    update_the_dict_with_smoothing(language_models) # call this function to implement add-one smoothing
    calculate_probability_for_language_models(language_models) # after the implementation of add-one smoothing, run this function to convert it to probabilistic numbers
    return language_models

# this function takes in language models and implement add-one smoothing
def update_the_dict_with_smoothing(language_models):
    for language in language_models.keys():
        for term in language_models[language]:
            language_models[language][term]+=1 # simply add one for every term

# this function takes in language models and convert it to probabilistic value base instead of count base
def calculate_probability_for_language_models(language_models):
    for language in language_models:
        total=0
        for count in language_models[language].values():
            total+=count
        for term in language_models[language]:
            language_models[language][term]/=total

def test_LM(in_file, out_file, LM):
    """
    test the language models on new strings
    each line of in_file contains a string
    you should print the most probable label for each string into out_file
    """
    print("testing language models...")
    set_of_all_unique_terms=set(list(LM.values())[0].keys()) # first retrieve the set of all unique terms across all models

    # This is an empty method
    # Pls implement your code below
    # read from input file
    with open(out_file, 'w') as file_write:
        with open(in_file,'r',encoding='utf-8') as file:
            lines=file.readlines()
            for line in lines:
                number_of_mathching=0 # initalize this variable to keep track of number of matching terms in each line, which facilitates the classification of an input string to "other" label
                line=line.strip()
                term_of_line=convert_string_to_list_of_terms(line)
                no_of_line_terms=len(term_of_line)
                dict_probability_all_models={country:Decimal(1) for country in LM} # initialize this variable to keep track of the accumulated probablity of each line across all models

                for term in term_of_line:
                    if term in set_of_all_unique_terms:
                        number_of_mathching+=1 # if term exists in set of unique terms, increment number of matching by 1
                        for country in LM:
                            dict_probability_all_models[country]*=Decimal(LM[country][term]) # update the probability across all languages

                file_write.write(f'{find_key_with_highest_values(dict_probability_all_models,number_of_mathching,no_of_line_terms)} {line}\n') 

# this function takes in hashmap (dictionary) with key being the languages and values being probabilistic values, return the language with highest probability  
def find_key_with_highest_values(dict_of_probabilites,no_of_matching,no_of_line_terms):
    max_values=max(list(dict_of_probabilites.values()))
    # if the ratio of number of matching terms over the number of unique terms across all models less than 0.5, the program classifies that text as "other language", otherwise assigns the language with the highest probabilistic value to it. 
    return "other" if (no_of_matching/no_of_line_terms)<0.5 else [key for key,value in dict_of_probabilites.items() if value==max_values][0]

def usage():
    print(
        "usage: "
        + sys.argv[0]
        + " -b input-file-for-building-LM -t input-file-for-testing-LM -o output-file"
    )


input_file_b = input_file_t = output_file = None
try:
    opts, args = getopt.getopt(sys.argv[1:], "b:t:o:")
except getopt.GetoptError:
    usage()
    sys.exit(2)
for o, a in opts:
    if o == "-b":
        input_file_b = a
    elif o == "-t":
        input_file_t = a
    elif o == "-o":
        output_file = a
    else:
        assert False, "unhandled option"
if input_file_b == None or input_file_t == None or output_file == None:
    usage()
    sys.exit(2)

LM = build_LM(input_file_b)
test_LM(input_file_t, output_file, LM)
