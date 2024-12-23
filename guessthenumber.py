import random as ra
import time
import threading

global time_up
global time_left
global high_score
high_score = 0 # Could be stored in a file
last_level: int = 30
playing: bool = True

def add_sub(lvl):
    lo = lvl + 1
    hi = (lvl + 2)*(round(lvl / 2) + 1)
    random_1 = ra.randint(lo,hi)
    random_2 = ra.randint(lo,hi)
    if lvl < 5:
        answer = int(random_1 + random_2)
        operand = '+'
    else:
        answer = int(random_1 - random_2)
        operand = '-'
    question = f"{random_1} {operand} {random_2}"
    return question, answer

def mult_div(lvl):
    lo = lvl - 8
    hi = (lvl - 8) * 2
    random_2 = ra.randint(lo,hi)
    if  lvl < 15:
        random_1 = ra.randint(lo,hi)
        answer = int(random_1 * random_2)
        question = f"{random_1} * {random_2}"
    else:
        answer = ra.randint(lo,hi)
        random_1 = random_2 * answer
        question = f"{random_1} / {random_2}"
    return question, answer

def exp_log(lvl):
    random_1 = ra.randint(20 - lvl, lvl - 19)
    if lvl < 25:
        random_2 = ra.randint(round(lvl / 5 - 4), round(lvl / 4) - 4)
        answer = int(random_1 ** random_2)
        question = f"{random_1} ^ {random_2}"
    else:
        if random_1 in (-1, 0, 1):
            random_1 = 2
        answer = ra.randint(1, level - 23) # Breaks if level is allowed <23
        tran = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        random_2 = random_1 ** answer # Needs to be declared before random_1
        random_1 = str(random_1).translate(tran)
        question = f"log{random_1} ({random_2})"
    return question, answer

def countdown():
    global time_up
    global time_left
    time_up = False
    seconds = 10
    while seconds > 0 and not countdown_event.is_set():
        time.sleep(0.1)
        seconds -= 0.1
        time_left = round(seconds, 1)
    if seconds <= 0:
        time_up = True
        countdown_event.set()
        print(f"Too late... {loose(score)}")

def final_score(score):
    global high_score
    score += level * level
    if score > high_score:
        high_score = score
    return score

def loose(score):
    global high_score
    return f"The right answer is {ops[1]} \nScore: {final_score(score)} \nHigh-score: {high_score}"

def get_user_input():
    global user_input
    user_input = input()

# Let the game commence!
if __name__ == '__main__':
    print("GUESS THE NUMBER")
    while playing is True: # The game loop
        score: int = 0
        level: int = 1
        countdown_event = threading.Event()
        time_up = None

        if input("Press enter to start or write y for Rules ") == "y":
            input("Rules: Every 5th level will add a new operation, points are based on speed and the level you reach.\nEach level is 10 seconds long. Your goal is to reach level 30. Good luck!")
        if level != 1 | score != 0:
            print("You whish...") # For the hackers
            break

        print("Level 1: ")
        while level <= 30: # The level loop
            if level < 5:
                ops = add_sub(level)
            elif level < 10:
                ops = add_sub(level)
            elif level < 20:
                ops = mult_div(level)
            elif level < 30:
                ops = exp_log(level)
            elif level == 30:
                level = last_level
                ops = add_sub(1, "+")
            print(ops[0])

            # Threads to handle the countdown and user input simultaneously
            countdown_event.clear()
            countdown_thread = threading.Thread(target=countdown)
            countdown_thread.start()

            input_thread = threading.Thread(target=get_user_input)
            input_thread.start()

            user_input = None
            while not countdown_event.is_set():
                if input_thread.is_alive():
                    input_thread.join(0.1)
                if user_input is not None:
                    countdown_event.set()
                    break
            countdown_thread.join()
            if time_up:
                break

            # Check if the user input is correct
            try:
                user_input = int(user_input)
            except ValueError:
                print("Error: NaN") # Not a number
            if user_input == ops[1] and level is not last_level:
                level += 1
                print(f"Level {level}:")
                score += int(time_left)
            elif level is last_level:
                level += 1
                print(f"Congratulations, you won!\nScore: {final_score(score)} \nHigh-score: {high_score}")
            else:
                print(loose(score))
                if input("Press enter to play again") != '':
                    playing = False
                break
