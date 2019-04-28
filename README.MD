PyPets is a game in Python that is meant for the joy (the minimal amount that you can get out of it, anyway) of the operating user.

DEPENDENCIES:
APScheduler;
Standard libraries (random, sqlite3, tkinter, etc: see main file for full list.): (should come prepackaged, but you never know.)

When starting up, the game may automatically install APScheduler, a dependency of the game.
If you use a Windows-based operating system, you will have to manually relaunch the game.
Otherwise, the game will automatically relaunch itself.

When the game first begins, you will be prompted to enter a user name.
If you are unsatisfied with the username you change, you are able to later change it as of Game Update 1. You may create as many users as you desire, limited only by the amount of space you want to dedicate to the generated .db file.

After creating a user (or even multiple), you can choose a user to play as in the menu.
This will actually matter in later stages, but for now, all stats are randomly generated upon starting the game part of the game.
In the game, there is the following menu:

1. F eed your pet - This option, self-explanatorily, feeds your pet and raises its hunger.Available in the GUI.
2. P lay with your pet - This option, also self-explanatorily, allows you to play with your pet and raise its happiness. Available in the GUI.

[Side note: As of 4/17/19, at least, happiness does not actually go down. So...]

3. S how current stats - Most of these are actually pretty self-explanatory. This displays your pets current stats. Available in the GUI, but not as an option; it is displayed by default.
4. C lear the screen - Clears the screen. This uses the 'clear' command on most Operating Systems, but 'cls' on Windows-based systems. This makes a difference, as 'clear' allows you to scroll up and see history. Also, you know, they don't work cross platform. That makes a difference too. Available in the GUI.
5. E dit your name - Change your username. Pressing enter cancels the operation. Not available in the GUI.
6. M ain Menu - This returns you to the main menu that you saw when you first started the game. Not available in the GUI.
7. O pen a GUI - Opens a Graphical User Interface in a new window. Has limited functionality compared to the shell (cannot administer medication or edit name.) Not available in the GUI... for obvious reasons.
8. A dminister medication - Previously 'G ive your pet medicine,' this option appears if the pet is sick. Choosing it removes the pet's sickness and hides the option. Not available in the GUI.

If you find any bugs or errors in the game that you're fairly certain aren't supposed to happen, please submit an issue or something.
I'm not entirely sure how Github works, so you'd know what to do.

Thanks for reading, and enjoy the game! I'd enjoy hearing your ideas on it!
