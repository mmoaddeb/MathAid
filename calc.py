#!/usr/bin/env python2
from random import randrange
from time import strftime
from itertools import izip

# The version of the program
version = "0.02"

# Constants representing the different operations/modes
ADDITION = 1
SUBTRACTION = 2
MULTIPLICATION = 3
DIVISION = 4
EXPONENTS = 5
QUESTION = 6

# Constants representing the user's choices
YES = 1
NO = 2

#########################################################################################
# HELPER FUNCTION FOR FUNCTIONS THAT TAKE KEYBOARD INPUT
def verify_selection (prompt="> "):
	"""
	DESCRIPTION:
		Ensures that the value given by the user can be converted into an int/float value by
		making the user re-enter a value when invalid input is detected
	PARAMS:
		prompt - the prompt to show to the user
	RETURNS:
		data - the valid value that the user entered in the form of int
	"""
	data = ""
	
	while not data.isdigit ():
		data = raw_input (prompt)
		
	data = int (data)
	
	return data

#########################################################################################
def select_mode ():
	"""
	DESCRIPTION:
		Asks the user to choose what they would like to practice
	RETURNS:
		selection - what the user wants to practice
	"""
	selection = -1
	
	while selection > 5 or selection < 1:
		print "Select what you would like to practice:"
		print "\t1 - Addition"
		print "\t2 - Subtraction"
		print "\t3 - Multiplication"
		print "\t4 - Division"
		print "\t5 - Exponents"
		
		selection = verify_selection ()
		
	return selection
	
#########################################################################################	
def select_range ():
	"""
	DESCRIPTION:
		Asks the user to select the range of numbers that they would like to practice with
	RETURNS:
		 min_val - the minimum value that the user wants
		 max_val - the maximum value that the user wants
	"""
	selection = NO
	
	min_val = 0
	max_val = 0
	
	while selection is NO:
		print "Select the range of numbers to practice with:"
		min_val = verify_selection ("\tMinimum value (inclusive): ")
		max_val = verify_selection ("\tMaximum value (inclusive): ")
		
		while max_val <= min_val:
			print "The maximum value has to be greater than the minimum!"
			max_val = verify_selection ("\tMaximum value (inclusive): ")
			
		print "Do you want the range from %d to %d?" % (min_val, max_val)
		print "\t1 - YES"
		print "\t2 - NO"
		
		selection = verify_selection ()
		
		while selection != YES and selection != NO:
			print "Do you want the range from %d to %d?" % (min_val, max_val)
			print "\t1 - YES"
			print "\t2 - NO"
		
			selection = verify_selection ()
			
	return min_val, max_val
	
###########################################################################################
def select_numb_problems ():
	"""
	DESCRIPTION:
		Asks to user to pick how many problems they would like to solve in this session
	RETURNS:
		selection - the number of problems the user wants to solve in this session
	"""
	selection = 0
	
	while selection <= 0:
		selection = verify_selection ("How many problems would you like to solve? ")
		
	return selection
	
############################################################################################
def generate_question (selection, numb_probs, minimum, maximum):
	"""
	DESCRIPTION:
		Creates problems for the user to solve based the type of problem the user
		wants to solve and the range of values he or she wants
	PARAMS:
		selection - The type of operation the user would like to practice
		numb_probs - the number of problems the user wants to practice
		minimum - the smallest number the user wants to practice with
		maximum - the biggest number the user wants to practice with
	RETURNS:
		user_answer - a list of numbers containing what the user answered to each problem
		correct_answer - a list of numbers containing the actual answer to each problem
		question - a list containing string representation of each question the user answered
	"""
	correct_answer = []
	user_answer = []
	question = []
	
	text_format = {
		ADDITION : "%d + %d = ?",
		SUBTRACTION : "%d - %d = ?",
		MULTIPLICATION : "%d * %d = ?",
		DIVISION : "%d / %d = ?",
		EXPONENTS : "%d ^ %d = ?",
		QUESTION : "%d %s %d %s"
	}
	
	for item in xrange (0, numb_probs):
		numb1 = float (randrange (minimum, maximum + 1))
		numb2 = float (randrange (minimum, maximum + 1))
		
		actual_answer = 0
		given_answer = 0
			
		if selection is ADDITION:
			actual_answer = numb1 + numb2
			question.append (text_format[ADDITION] % (numb1, numb2))
			given_answer = float (raw_input (text_format[QUESTION] % (numb1, "+", numb2, "= ")))
			
		elif selection is SUBTRACTION:
			actual_answer = numb1 - numb2
			question.append (text_format[SUBTRACTION] % (numb1, numb2))
			given_answer = float (raw_input (text_format[QUESTION] % (numb1, "-", numb2, "= ")))
			
		elif selection is MULTIPLICATION:
			actual_answer = numb1 * numb2
			question.append (text_format[MULTIPLICATION] % (numb1, numb2))
			given_answer = float (raw_input (text_format[QUESTION] % (numb1, "*", numb2, "= ")))
			
		elif selection is DIVISION:
			if numb2 == 0: 
				numb2 = 1
			actual_answer = numb1 / float (numb2)
			question.append (text_format[DIVISION] % (numb1, numb2))
			given_answer = float (raw_input (text_format[QUESTION] % (numb1, "/", numb2, "= ")))
			
		elif selection is EXPONENTS:
			actual_answer = numb1 ** float (numb2)
			question.append (text_format[EXPONENTS] % (numb1, numb2))
			given_answer = float (raw_input (text_format[QUESTION] % (numb1, "^", numb2, "= ")))
				
		correct_answer.append (actual_answer)
		user_answer.append (given_answer)
		
	return user_answer, correct_answer, question		
			
############################################################################################
def check_answers (user_answer, correct_answer):
	"""
	DESCRIPTION:
	   Takes a list of user answers and the correct answers to the
	   generated problem and calculates the number of correct and wrong
	   answers. It also flags the problem number that had an incorrect answer
	PARAMS:   
	   user_answer - the list/tuple of answers the user gave to each problem
	   correct_answer - the list/tuple of the actual answer to the problems the user was given
	RETURNS:
	   numb_correct - int representation of the number of questions answered correctly
	   numb_wrong - int representation of the number of questions answered incorrectly
	   mistakes - a list containing the problem numbers that were answered incorrectly  
	"""
	numb_correct = 0
	numb_wrong = 0
	
	mistakes = []
	
	index = 0

	for given, actual in izip (user_answer, correct_answer):
		if given != actual:
			numb_wrong += 1
			mistakes.append (index)
		else:
			numb_correct += 1
			
		index += 1
		
	return numb_correct, numb_wrong, mistakes
	
#############################################################################################
def store_results (numb_correct, numb_wrong, question, loc_mistakes, given_answer, actual_answer):
	"""
	DESCRIPTION:
		Creates the 'Results.txt' file that stores the time and date of the practice session along with the 
		questions that had to be answered in that session. The user's answer and the correct answer can also be 
		seen with a 'MISTAKE' label placed next to problems where the user entered the incorrect answer. The same
		file is used to store the results of all the sessions.
	PARAMS:
		numb_correct - int representing how many questions the user answered correctly in this session
		numb_wrong - int representing how many questions the user answered incorrectly in this session
		question - a list containing the string representation of all the questions the user was asked
		loc_mistakes - a list containing the problem numbers that were answered incorrectly
		given_answer - a list containing the answers that the user provided to each problem
		actual_answer - a list containing the correct answers to the problems that the user had to answer
	"""
	with open ("Results.txt", "a") as results:
		results.write ("--------------------------------------------------\n")
		results.write (strftime ("%c") + "\n")
		results.write ("--------------------------------------------------\n")
		results.write ("Correctly answered: %d problems\n" % numb_correct)
		results.write ("Incorrectly answered: %d problems\n\n" % numb_wrong)
		
		for i in xrange (len (question)):
			results.write ("%d) %s\n" % (i + 1, question[i]))
			# If the problem was flagged as answered incorrectly
			# write a 'MISTAKE' label next to it
			if i in loc_mistakes:
				results.write ("****MISTAKE****\n")
			results.write ("Your answer: %.2f\n" % given_answer[i])
			results.write ("The correct answer: %.2f\n\n" % actual_answer[i])
		results.write ("*** END OF SESSION ***\n\n")
		
#############################################################################################
def main ():
	print "\n*** For each selection, enter its number and press enter ***\n"
	
	selection = select_mode ()
	minimum, maximum = select_range ()
	numb_problems = select_numb_problems ()
	given_answer, actual_answer, question = generate_question (selection, numb_problems, minimum, maximum)
	numb_correct, numb_wrong, loc_mistakes = check_answers (given_answer, actual_answer)
	
	# Store the results of the session in a file called 'Results.txt' 
	store_results (numb_correct, numb_wrong, question, loc_mistakes, given_answer, actual_answer)
	
	print "-" * 74
	print "* Number of correct answers =", numb_correct
	print "* Number of wrong answers =", numb_wrong	
	print "* Check the corresponding 'Results.txt' file for more details"
	print "-" * 74
	print "\n\tThank You for using Math Aid, Version %s\n" % version

#################################################################################################

if __name__ == "__main__":
	main ()
