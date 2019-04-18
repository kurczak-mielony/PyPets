#PyPets
#By Kurczak Mielony
import random, time, sys, sqlite3, os
def apsched():
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        return False
    except ModuleNotFoundError:
        print("APScheduler, a vital component to the game, is being installed. After its installation, Python will exit.\nRestarting the game will not yield this message again unless there was an error in the installation.\nThank you.\n\n")
        os.system('pip3 install --user apscheduler')
        if os.name != "nt":
            print("The game will try to automatically relaunch itself. Please wait."+("\n"*3))
            return True
        else: exit()
flag = apsched()
if flag: os.system(f"sleep 2 && python {os.path.abspath(__file__)}")
else: from apscheduler.schedulers.background import BackgroundScheduler #This backwards approach seems to work on installing APScheduler even on computers without it, as well as removing any name errors.

hunger = random.randint(80,100)
happiness = random.randint(80,100)
dirtiness = random.randint(50, 100)
sick = False; sicknessfactor = 2

username = ""

conn = sqlite3.connect('pypets.db')
c = conn.cursor()

def background():
    global hunger
    if hunger != 0:
        value = "Your pet lost 5 hunger.\n"
        if hunger < 60: value+="Your pet is very hungry. You should feed it!\n"
        hunger-=5
        print(value)
    else: return

def selection(inpt, num, letter):
        if inpt == str(num) or inpt.upper().strip() == letter: return True

def statgain(stat, statgain, adjective):
    if stat+statgain > 100:
        statgain = 100-stat
        stat = 100
    else: stat = stat+statgain
    if statgain == 1: statgain = f"{statgain} {adjective} point"
    else: statgain = f"{statgain} {adjective} points"
    return statgain, stat

def dirty():
    global dirtiness, sick, sicknessfactor
    activities = ("played in the mud", "went digging through the trash", "had an accident in the house")
    activity = random.choice(activities); adj = "dirtiness"
    dirtinessgain = random.randint(1, 5)
    dirtinessgain, dirtiness = statgain(dirtiness, dirtinessgain, adj)
    toprange = 101; bottomrange = 90
    while True:
        if dirtiness in range(bottomrange, toprange):
            sicknessprobability = random.randint(1, sicknessfactor)
            if sicknessprobability == 1: sick = True; break
            else: sick = False; break
        if bottomrange != 0:
            bottomrange-=10
            toprange-=10
            sicknessfactor+=2
            continue
        else: break
    display = f"Yuck! Your pet {activity} and gained {dirtinessgain}! It is now at {dirtiness}/100 {adj} points.\n"
    if sick: display+="Your pet has contracted an illness. You can remedy this by applying medication to your pet.\n"
    print(display)

def userselection():
    global username
    while True:
        while True:
            try:
                c.execute('SELECT * FROM pypetusers')
                break
            except sqlite3.OperationalError:
                c.execute('CREATE TABLE pypetusers (userid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
                continue
        users = c.fetchall()
        if len(users) == 0:
            print("It appears there are no users registered yet.")
            name = input("Please enter a user name to be known by. This can be changed later.\n")
            c.execute('INSERT INTO pypetusers VALUES (NULL, (?))', (name,))
            conn.commit()
            continue
        else:
            print("Available users:")
            for item in users:
                print(f"{item[0]}. {item[1]}")
            user = input("Please enter the number of the user you would like to play as, or enter \'C\' to create a new user.\n")
            if user.strip() in [str(x[0]) for x in users]:
                c.execute('SELECT name FROM pypetusers WHERE userid=?', (int(user),))
                username = c.fetchone()
                break
            elif user.upper().strip() == "C":
                name = input("Please enter a user name to be known by. This can be changed later.\n")
                c.execute('INSERT INTO pypetusers VALUES (NULL, (?))', (name,))
                conn.commit()
                print("The new user was successfully created.\n\n")
                continue
            else:
                print("Please either choose the number corresponding to a user or \'C\'.")
        break

def display_stats():
    global hunger, happiness, dirtiness, sick
    stats = f"Hunger is currently {hunger}/100\nHappiness is currently {happiness}/100\nDirtiness is currently {dirtiness}/100\n"
    if sick: stats+="Your pet is currently sick.\n"
    print(stats)

def game():
    userselection()
    scheduler = BackgroundScheduler()
    global username, sick
    try:
        print(f"You are now playing as {username[0]}.")
        scheduler.add_job(background, 'interval', seconds=30, jitter=5)
        scheduler.add_job(dirty, 'interval', seconds=30, jitter=5)
        scheduler.start()
        while True:
            choicetext = "What would you like to do?\n1. F eed your pet\n2. P lay with your pet\n3. S how current stats\n4. C lear the screen\n5. M ain menu\n"
            if sick: choicetext+="6. G ive your pet medicine"
            choice = input(choicetext)
            if selection(choice, 1, "F"): feedpet()
            elif selection(choice, 2, "P"): play()
            elif selection(choice, 3, "S"): display_stats()
            elif selection(choice, 4, "C"): os.system('cls' if os.name == 'nt' else 'clear')
            elif selection(choice, 5, "M"):
                scheduler.shutdown()
                break
            elif selection(choice, 6, "G") and sick: sick = False; print("Your pet was cured of its ailment!\n")
            else: print("Please choose the number or letter corresponding to the activity.\n")
    except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()

def play():
    global happiness
    adj = "happiness"
    happinessgain = random.randint(1,10)
    game = random.choice(("played a nice game of fetch", "chased each other around", "enjoyed the sights at the park"))
    happinessgain, happiness = statgain(happiness, happinessgain, adj)
    print(f"You and your pet spent some time together and you {game}. Your pet gained {happinessgain}. It is now at {happiness}/100 {adj} points.\n")

def feedpet():
    global hunger
    adj = "food"
    if hunger == 100:
        print("Your pet is already at max hunger.")
        return
    food = random.choice(("a nice steak", "a plate of pancakes", "a fish"))
    hungergain = random.randint(1,10)
    hungergain, hunger = statgain(hunger, hungergain, adj)
    print(f"You fed your pet {food} and it gained {hungergain}! It is now at {hunger}/100 {adj} points.\n")

def mainmenu():
    main_menu = """ _______  __   __  _______  _______  _______  _______
|    _  ||  |_|  ||    _  ||    ___||__   __||  _____|                   __
|   |_| ||       ||   |_| ||   |___    | |   | |_____                   /\\/\'-,
|    ___||_     _||    ___||    ___|   | |   |_____  |          ,--\'\'\'\'\'   /-
|   |      |   |  |   |    |   |___    | |    _____| |    ____,\'.  )       \\___
|___|      |___|  |___|    |_______|   |_|   |_______|   \'\"\"\"\"\"------\'\"\"\"`-----\'
\n"""
    print(main_menu)
    while True:
        select = input("\nWhat would you like to do?\n1. S elect a user\n2. E xit the game\n")
        if selection(select, 1, "S"): game()
        elif selection(select, 2, "E"): return
        else: print("Please choose an option.\n")

if not flag: mainmenu()
