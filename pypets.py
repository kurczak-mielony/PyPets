import tkinter as tk
from tkinter import messagebox
import random, time, sys, sqlite3, os

#PyPets
#By Kurczak Mielony

def apsched():
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        return False
    except ModuleNotFoundError:
        print("APScheduler, a vital component to the game, is being installed. After its installation, Python will exit.\nRestarting the game will not yield this message again unless there was an error in the installation.\nThank you.\n\n")
        os.system("py -3 -m pip install apscheduler > apscheduler_install.txt" if os.name == 'nt' else "pip3 install --user apscheduler > apscheduler_install.txt")
        print("The game will try to automatically relaunch itself. Please wait.\n\n\n")
        return True

flag = apsched()
if flag: os.system(f"TIMEOUT 2 > nul && python {os.path.abspath(__file__)}" if os.name == 'nt' else f"sleep 2 && python {os.path.abspath(__file__)}")
else: from apscheduler.schedulers.background import BackgroundScheduler #This backwards approach seems to work on installing APScheduler even on computers without it, as well as removing any name errors.

hunger = random.randint(0,100)
happiness = random.randint(0,100)
dirtiness = random.randint(0, 100)
sick = False
#Right now, these stats don't mean anything. But later on, when the pets portion part of the database is complete,
#these will be saved per pet, and no longer just be randomly generated.

username = "" #Done to prevent name errors later on.

def statupdate():
    global hunger, happiness, sick, dirtiness, after_id, w, root
    happyface = ": )"; neutralface = ": |"; sadface = ": ("
    if happiness > 74: face = happyface
    elif happiness > 49: face = neutralface
    else: face = sadface
    label = f"STATISTICS:\nHunger: {hunger}/100\nHappiness: {happiness}/100 {face}\nDirtiness: {dirtiness}/100\nSick: {sick}"
    w.config(text=label)
    after_id = root.after(1000, statupdate)

def med_button():
    global sick, after_id2, root, medicine
    if sick: medicine.grid(column=0, row=3, sticky='we')
    else: medicine.grid_remove()
    after_id2 = root.after(1000, med_button)

def deletionprotocol():
    global after_id, after_id2
    if messagebox.askokcancel("Quit", "Do you really want to quit the PyPets GUI?"):
        root.after_cancel(after_id)
        root.after_cancel(after_id2)
        root.destroy()

conn = sqlite3.connect('pypets.db')
c = conn.cursor()

def statgain(stat, statgain, adjective):
    if stat+statgain > 100:
        statgain = 100-stat
        stat = 100
    else: stat = stat+statgain
    if statgain == 1: statgain = f"{statgain} {adjective} point"
    else: statgain = f"{statgain} {adjective} points"
    return statgain, stat

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

def play():
    global happiness
    adj = "happiness"
    happinessgain = random.randint(1,10)
    game = random.choice(("played a nice game of fetch", "chased each other around", "enjoyed the sights at the park"))
    happinessgain, happiness = statgain(happiness, happinessgain, adj)
    print(f"You and your pet spent some time together and you {game}. Your pet gained {happinessgain}. It is now at {happiness}/100 {adj} points.\n")

def display_stats():
    global hunger, happiness, dirtiness, sick
    stats = f"Hunger is currently {hunger}/100\nHappiness is currently {happiness}/100\nDirtiness is currently {dirtiness}/100\n"
    if sick: stats+="Your pet is currently sick.\n"
    print(stats)

def background():
    global hunger
    if hunger != 0:
        value = "Your pet lost 5 hunger.\n"
        if hunger < 60: value+="Your pet is very hungry. You should feed it!\n"
        hunger-=5
        print(value)
    else: return

def dirty():
    global dirtiness, sick
    activities = ("played in the mud", "went digging through the trash", "had an accident in the house")
    activity = random.choice(activities); adj = "dirtiness"
    dirtinessgain = random.randint(1, 5)
    dirtinessgain, dirtiness = statgain(dirtiness, dirtinessgain, adj)
    toprange = 101; bottomrange = 90; sicknessfactor = 2
    while not sick:
        print(f"{toprange} | {bottomrange} || {sicknessfactor}")
        if dirtiness in range(bottomrange, toprange):
            sicknessprobability = random.randint(1, sicknessfactor)
            print(sicknessprobability)
            if sicknessprobability == 1: sick = True; break
            else: sick = False; break
        if bottomrange != 0:
            print("Here.")
            bottomrange-=10
            toprange-=10
            sicknessfactor+=2
            continue
        else: break
    display = f"Yuck! Your pet {activity} and gained {dirtinessgain}! It is now at {dirtiness}/100 {adj} points.\n"
    if sick: display+="Your pet has contracted an illness. You can remedy this by applying medication to your pet.\n"
    print(display)

def selection(inpt, num, letter):
        if inpt == str(num) or inpt.upper().strip() == letter: return True

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
            user = input("Please enter the number of the user you would like to play as, enter \'E\' or \'ESC\' to exit the selection process, or enter \'C\' to create a new user.\n")
            if user.strip() in [str(x[0]) for x in users]:
                c.execute('SELECT name FROM pypetusers WHERE userid=?', (int(user.strip()),))
                username = c.fetchone()
                return True
            elif user.upper().strip() == "C":
                name = input("Please enter a user name to be known by. This can be changed later.\n")
                c.execute('INSERT INTO pypetusers VALUES (NULL, (?))', (name,))
                conn.commit()
                print("The new user was successfully created.\n\n")
                continue
            elif user.upper().strip() == "E" or user.upper().strip() == "ESC": return False
            else:
                print("Please either choose the number corresponding to a user or \'C\'.")
                continue

def username_edit():
    global username
    c.execute('SELECT userid FROM pypetusers WHERE name=?', username)
    #Normally, the syntax for inserting variables into a query is to put it into a tuple, which is still being done, but implictly.
    #If you look at game(), you'll see that when the username is printed, it's username[0], because the data is already in a tuple!
    userid = c.fetchone()[0]
    newusername = input("Please choose a new username to be known as. If you'd like to cancel this operation, press enter.")
    if newusername == "": return
    else: c.execute('UPDATE pypetusers SET name=? WHERE userid=?', (newusername, userid))
    print("Done. Your name has been edited.")
    c.execute('SELECT name FROM pypetusers WHERE userid=?', (userid,))
    username = c.fetchone()
    conn.commit()

def clearscreen():
    if os.name == 'nt': os.system('cls')
    else: os.system('clear')

def administer():
    global sick
    sick = False
    print("Your pet was cured of its ailment!\n")

def game():
    scheduler = BackgroundScheduler()
    global username, sick, w, root, medicine
    if userselection():
        try:
            print(f"You are now playing as {username[0]}.")
            scheduler.add_job(background, 'interval', seconds=30, jitter=5)
            scheduler.add_job(dirty, 'interval', seconds=10, jitter=5)
            scheduler.start()
            while True:
                choicetext = "What would you like to do?\n1. F eed your pet\n2. P lay with your pet\n3. S how current stats\n4. C lear the screen\n5. E dit your name\n6. M ain menu\n7. O pen a GUI\n"
                if sick: choicetext+="8. A dminister medication\n"
                choice = input(choicetext)
                if selection(choice, 1, "F"): feedpet()
                elif selection(choice, 2, "P"): play()
                elif selection(choice, 3, "S"): display_stats()
                elif selection(choice, 4, "C"): clearscreen()
                elif selection(choice, 5, "E"): username_edit()
                elif selection(choice, 6, "M"): scheduler.shutdown(); break
                elif selection(choice, 7, "O"):
                    root = tk.Tk(); root.title("PyPets!")
                    w = tk.Label(root, text="")
                    playpet = tk.Button(root, text="Play with your pet", command=play)
                    feed = tk.Button(root, text="Feed your pet", command=feedpet)
                    clear = tk.Button(root, text="Clear the shell", command=clearscreen)
                    medicine = tk.Button(root, text="Administer medication", command=administer)
                    w.grid(row=0, column=1, rowspan=4, sticky='we',padx=5, pady=5)
                    feed.grid(row=0, column=0, sticky='we'); playpet.grid(row=1,column=0, sticky='we'); clear.grid(column=0, row=2, sticky='we')
                    root.protocol("WM_DELETE_WINDOW", deletionprotocol)
                    statupdate()
                    med_button()
                    root.mainloop()
                elif selection(choice, 8, "A") and sick: administer()
                else: print("Please choose the number or letter corresponding to the activity.\n")
        except (KeyboardInterrupt, SystemExit):
                scheduler.shutdown()
    else: return

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
