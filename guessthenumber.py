import random
import time
import threading
import math

score = 0
level = 1
countdown_event = threading.Event()
global time_up
time_up = None
global time_left
time_left = 0
last_level = 30

def add_sub(lvl, operand):
    random_1 = random.randint(lvl + 1, (lvl + 2 ) * (round(lvl/2) + 1))
    random_2 = random.randint(lvl + 1, (lvl + 2 ) * (round(lvl/2) + 1))
    question = str(random_1) + " " + operand + " " + str(random_2)
    if operand == "+" and lvl != 5 or lvl < 5:
        answer = int(random_1 + random_2)
    else:
        answer = int(random_1 - random_2)
    return question, answer

def mult_div(lvl, operand):
    random_2 = random.randint(lvl - 8, (lvl - 8) * 2)
    if operand == "*" and lvl != 15 or lvl < 15:
        random_1 = random.randint(lvl - 8, (lvl - 8) * 2)
        answer = int(random_1 * random_2)
        question = str(random_1) + " * " + str(random_2)
    else:
        random_1 = random_2 * random.randint(lvl - 8, (lvl - 8) * 2)
        answer = int(random_1 / random_2)
        question = str(random_1) + " / " + str(random_2)
    return question, answer

def exp_log(lvl, operand):
    random_1 = random.randint(20 - lvl, lvl - 19)
    if operand == "^" and lvl != 25 or lvl < 25:
        random_2 = random.randint(0 + round(lvl / 5 - 4), round(lvl / 4) - 4)
        answer = int(random_1 ** random_2)
        question = str(random_1) + " ^ " + str(random_2)
    else:
        if random_1 == 0 or random_1 == 1 or random_1 == -1:
            random_1 = 2
        answer = random.randint(1, level - 23)
        random_2 = random_1 ** answer
        question = str(random_1) + " log " + str(random_2)
    return question, answer

def countdown():
    global time_up
    global time_left
    time_up = False
    seconds = 10
    while seconds > 0 and not countdown_event.is_set():
        time.sleep(1)  # Could be more accurate but there's no visible countdown so it should suffice
        seconds -= 1
        time_left = seconds
        if seconds == 0:
            countdown_event.set()
            time_up = True
            print("Too late\n" + loose())

def final_score():
    global score
    score += level * level

def loose():
    final_score()
    return "The right answer is: " + str(operation[1]) + "\nYou got: " + str(round(score)) + " points, better luck next time!"
    
# Let the game start!
print("GUESS THE NUMBER")

if input("Press enter to start or write y for Rules ") == "y":
    print("Rules: Every 5th level will add a new operation, points are based on speed and the level you reach.\nEach level is 10 seconds long. Your goal is to reach level 30. Good luck!")
    input("Press enter to continue")

print("Level 1: ")
while level <= 30:

    if level < 5:
        operations = [add_sub(level, "+")]
    elif level == 5:
        operations = [add_sub(level, "-")]
    elif level > 5 and level < 10:
        operations = [add_sub(level, random.choice(["-", "+"]))]
        
    if level >= 10 and level < 15:
        operations = [mult_div(level, "*")]
    elif level == 15:
        operations = [mult_div(level, "/")]
    elif level > 15 and level < 20:
        operations = [mult_div(level, random.choice(["*", "/"]))]
        
    if level >= 20 and level < 25:
        operations = [exp_log(level, "^")]
    elif level == 25:
        operations = [exp_log(level, "log")]
    elif level > 25 and level != 30:
        operations = [exp_log(level, random.choice(["^", "log"]))]
        
    if level == 30:
        operations = [add_sub(1, "+")]

    operation = random.choice(operations)
    print(operation[0])

    # Multiple threads for simultanious input and countdown
    countdown_event.clear()
    countdown_thread = threading.Thread(target=countdown)
    countdown_thread.start()
    user_input = None
    while not user_input and not time_up:
        user_input = input()
    score += time_left
    countdown_event.set()
    countdown_thread.join()
    if time_up:
        break
    
    # Prevent crashes from faulty input
    try:
        user_input = int(user_input)
        input_int = True
    except ValueError:
        input_int = None
        print("Error: NaN")
        break

    if int(user_input) == operation[1] and level != last_level:
        level += 1
        print("Level " + str(level) + ": ")
    elif level == last_level:
        final_score()
        score += time_left
        print("Congratulations, you won!\nYour score is: " + str(score))
        level += 1
    else:
        print(loose())
        break
