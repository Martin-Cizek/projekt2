# -*- coding: utf-8 -*-
"""
BULLS AND COWS GAME

Created on Tue Aug 17 12:13:41 2021

@author: Martin Cizek
"""
import random
import csv

WELCOME_SCREEN = """Hi there!
-----------------------------------------------
I've generated a random 4 digit number for you.
The number  contains  4 unique  digits and does
not start with 0.

Let's play a bulls and cows game!
-----------------------------------------------
Enter a number:
-----------------------------------------------
"""
SEPARATOR = "-----------------------------------------------"


def GenSecretNumStr():
    reslt=str(random.randint(1, 9))
    for i in range(3):
        while True:
            dig = random.randint(0, 9)
            if not(str(dig) in reslt):
                reslt += str(dig)
                break
    return reslt

def CheckInputValidity(input_str):
    reslt = False
    if input_str.isnumeric():
        if input_str[0]=='0':
            print("The entered number can not begin with 0.")
        elif len(input_str)<4:
            print("The entered number must contain 4 digits.")
        else:
            reslt = True
            for ch in input_str:
                if input_str.count(ch)>1:
                    print("The entered number contains duplicate digits.")
                    reslt = False
                    break
    else:
        print("You have entered a non-numeric character.")
    return reslt

def FindBullsCows(input_str, secret_str):
    bulls_cows = dict()
    bulls_cows['bulls'] = 0
    bulls_cows['cows'] = 0
    for ch in input_str:
        if ch in secret_str:
            if input_str.index(ch)==secret_str.index(ch):
                bulls_cows['bulls'] += 1
            else:
                bulls_cows['cows'] += 1
    return bulls_cows

def SaveGameResults(rnd_num_str, NAtt):
    with open('game_stats.csv', 'a', newline='') as csvfile:
        reslt_writer = csv.writer(csvfile, delimiter=' ')
        reslt_writer.writerow([rnd_num_str] + [str(NAtt)])

def ReadGameStats(NAtt):
    GameStats=dict()
    GameStats['N_worse_or_equal'] = 0
    GameStats['N_games'] = 0
    try:
        with open('game_stats.csv', 'r', newline='') as csvfile:
            reslt_reader = csv.reader(csvfile, delimiter=' ')                
            for row in reslt_reader:
                GameStats['N_games'] += 1
                if int(row[1]) > NAtt:
                    GameStats['N_worse_or_equal'] += 1
    except:
        GameStats['N_worse_or_equal'] = 0
        GameStats['N_games'] = 0    
    return GameStats 

def main():        
    print(WELCOME_SCREEN)
    RndNumStr = GenSecretNumStr()    
    GameRunning = True
    NumAttempts = 0
    while GameRunning:
        InputValid = False
        while not(InputValid):      
              KbdInput = input(">>>")          
              if (KbdInput=='q' or KbdInput=='Q'):
                   GameRunning = False
                   InputValid = True
                   print(f"'{KbdInput}' pressed, exiting the game.")
                   print(f"The secret number was {RndNumStr}.")
                   break               
              InputValid = CheckInputValidity(KbdInput)
              if not(InputValid):
                  print("Please try again")                  
        if GameRunning:            
            reslt = FindBullsCows(KbdInput, RndNumStr)
            NumAttempts += 1
            if reslt['bulls']<4:
                print(f"{reslt['bulls']} bull{'s' if reslt['bulls']!=1 else ''}, "
                      f"{reslt['cows']} cow{'s' if reslt['cows']!=1 else ''}")
                print(SEPARATOR)
            else:
               print("Correct, you've guessed the right number\n"
                     f"in {NumAttempts} attempt{'s' if NumAttempts!=1 else ''}!")
               print(SEPARATOR)
               if NumAttempts==1:
                   print("Lucky one;)")
               elif NumAttempts<=5:
                   print("That's excellent!")
               elif NumAttempts<=7:
                   print("That's outstanding.")
               elif NumAttempts<=11:
                   print("That's average.")
               else:
                   print("That's not so good.")                                  
               print(SEPARATOR)
               GameRunning = False
               GameStats = ReadGameStats(NumAttempts)
               if GameStats['N_games']>0:
                   print("This was better than "
                         f"{GameStats['N_worse_or_equal']} of {GameStats['N_games']} "
                         "previous games")
               SaveGameResults(RndNumStr, NumAttempts)
    print("Goodbye!")

if __name__ == "__main__":
    main()              
                               
    
                