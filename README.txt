This is the README file for A0290532J's submission
Email: e1325138@u.nus.edu

== Python Version ==

I'm using Python Version <3.10.12 or 3.10.7> for
this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.

Algorithm:

Phase 1: Get the set of all unique terms (vocabulary set) as 4-gram units from input file 
+ Read the input file and retrieve all the lines
+ Initialize the empty hashmap initially, with key being the unique term and value being 0
+ Iterate through all the lines of the input file, for each line, convert it the list of 4-gram units
+ Iterate through every single 4-grams unit of the list, and update the dictionary accordingly

Phase 2: Build language models
+ Initialize the empty hashmap to contain all language models
+ Iterate through the every single line of the input file
+ Find the label of the text (language) by slicing the line from the beginning of text to index of the first space
+ Check if label not yet exist in hashmap, add the label as new key and the corresponding value being the output of part 1
+ Convert the rest of line into a list of 4-gram units
+ Iterate through this list of 4-gram units, and update the hashmap by increment the occurrencs of each term by 1

Phase 3: Add one smoothing and recalculate the probabilistic values
+ After phase 2, we have a hashmap with key being language models, and values being hashmap with unique terms as key and values as their occurrencs (count-base)
+ We need to convert this count-base to probabilistic-based using some computation, but before getting to that, we need to implement add-one smoothing
+ Add-one smoothing:
    + Iterate through every language of language model hashmap
    + Iterate through every terms, and increment its count by 1
+ Calculate probabilistic values:
    + Similarly, iterate through every language and term and divide each term count by the total of all 4-gram units of that language

Phase 4: Implement prediction by assign labels to testing set using trained language models
+ Read the input test file to retrieve all the lines 
+ Get the set of unique terms as we did earlier 
+ Iterate through every line:
    + Convert the line into the list of 4-gram units
    + Initialize the hashmap with key being all languages, value being set 1 at first, this hashmap to keep track of probabilistic values of that line
    + Iterate through every single terms of the list, for every term:
        + If it exist in set of unique terms, we update the probabilistic values all languages based on language models we trained
    + We assign the label which is the language with highest probabilistic value to that line and write the result to the output file


== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

To implement the algorithm, I have defined a couple of additional functions to ensure the clarity and readability (you can refer to build_test_LM.py for more details)

1. convert_string_to_list_of_terms 
=> this function takes in an input string and return a list of N-gram units

2. dict_of_all_unique_terms_all_languages
=> this function takes in all lines of input file and return a dictionary with the keys as the unique terms in all lines

3. convert_file_to_dict_language_models
=> this function takes in an input file and return language models

4. update_the_dict_with_smoothing
=> this function takes in language models and implement add-one smoothing

5. calculate_probability_for_language_models
=> this function takes in language models and convert it to probabilistic base instead of count base

6. find_key_with_highest_values
=> this function takes in hashmap (dictionary) with key being the languages and values being probabilistic values, return the language with highest probability
Logic for this function: If the ratio of number of matching terms over the number of unique terms across all models less than 0.5, the program classifies that text as "other language", otherwise assigns the language with the highest probabilistic values to it. 

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] I, A0290532J, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0290532J, did not follow the class rules regarding homework
assignment, because of the following reason:

Not applicable, because I followed the class rules thoroughly

I suggest that I should be graded as follows:

Not applicable

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

I referred to this website on Decimal module for working with decimals to resolve the issues with small probabilistic result
https://docs.python.org/3/library/decimal.html

I did not consult anyone to complete this assignment
