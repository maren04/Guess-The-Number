import random as ra
import time
import threading

playing: bool = True
global high_score
high_score = 0
global time_up
global time_left
last_level: int = 30

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
        random_1 = random_2 * ra.randint(lo,hi)
        answer = int(random_1 / random_2)
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
        answer = ra.randint(1, level - 23)
        random_2 = random_1 ** answer
        tran = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        random_1 = str(random_1).translate(tran)
        question = f"log{random_1} ({random_2})"
    return question, answer

def countdown():
    global time_up
    global time_left
    time_up = False
    seconds = 10
    while seconds > 0 and not countdown_event.is_set():
        time.sleep(0.1)  # Could be more accurate but there's no visible countdown so it should suffice
        seconds -= 0.1
        time_left = seconds
        if seconds == 0:
            countdown_event.set()
            time_up = True
            print(f"Too late... {loose(score, high_score)}")

def final_score(score):
    global high_score
    score += level * level
    if score > high_score:
        high_score = score
    return score

def loose(score):
    global high_score
    return f"The right answer is {ops[1]} \nScore: {final_score(score)} \nHigh-score: {high_score}"

# Let the game start!
if __name__ == '__main__':
    while playing is True:
        playing = False
        score: int = 0
        level: int = 1
        countdown_event = threading.Event()
        time_up = None
        time_left = 0

        print("GUESS THE NUMBER")
        if input("Press enter to start or write y for Rules ") == "y":
            input("Rules: Every 5th level will add a new operation, points are based on speed and the level you reach.\nEach level is 10 seconds long. Your goal is to reach level 30. Good luck!")
        if level == 1:
            print("Level 1: ")
        else:
            print("You whish...")
            break
        while level <= 30:
            if level < 5:
                ops = add_sub(level)
            elif level < 10:
                ops = add_sub(level)
            if level >= 10 and level < 15:
                ops = mult_div(level)
            elif level >= 15 and level < 20:
                ops = mult_div(level)
            if level >= 20 and level < 25:
                ops = exp_log(level)
            elif level >= 25 and level < 30:
                ops = exp_log(level)
            if level == 30:
                level = last_level
                ops = add_sub(1, "+")
            print(ops[0])

            countdown_event.clear()
            countdown_thread = threading.Thread(target=countdown)
            countdown_thread.start()
            user_input = None
            while not user_input and not time_up:
                user_input = input()
            countdown_event.set()
            countdown_thread.join()
            if time_up:
                break
            
            try:
                user_input = int(user_input)
            except ValueError:
                print("Error: NaN")
            if user_input == ops[1] and level is not last_level:
                level += 1
                print(f"Level {level}:")
                score += int(time_left)
            elif level is last_level:
                level += 1
                print(f"Congratulations, you won!\nScore: {final_score(score)} \nHigh-score: {high_score}")
            else:
                print(loose(score))
                break

        if input("Press enter to play again") == '':
            playing = True
