# Genshin Lyre Project
The Genshin Lyre Project is a command-line based script that allows users to play Genshin Impact's Windsong Lyre on Windows.

## Installation
To install and use the Genshin Lyre Project, follow these steps:

1) Clone the repository: `git clone git@github.com:stanX19/genshin_lyre.git`
2) Install the required dependencies: `pip install -r requirements.txt`
3) Run the genshin_lyre.py script: `py genshin_lyre.py`
4) You can now start using the script.


## getting started
1) type in the command `set`
2) type in `1`
3) follow the instructions and hover your cursor above your **running** genshin app
4) press `space` as instructed.
5) your genshin app loaction has been recorded, now input a song index, e.g. `1`
6) you will see the screen changing into the genshin game, press `shift`, **then** `k`
7) the song will start playing, exit play mode using `shift` **then** `i`
8) go back to the running `genshin_lyre` interface
9) you can now enter a new command
10) you can enter `help` to display the list of available commands and their usage.

## Usage
Here are some additional instructions and features you can explore with the Genshin Lyre Project:

##### Basics:
        
        To enter something means typing something in and press enter at the end
        (Y/n/q) ------------means yes, no or quit , type in
                            'y' for yes, 'n' or anything else for no and 'q' for quit
        Xxx is missing------you need to include xxx

##### Enter Commands:

    Play commands:
        song index or song name to start playing
        'i' ----------------to exit; enter 'list' to show song list
        'key' --------------followed by a index to view raw keys
                                    # try 'space' or 'raw' for different format
        'notification' -----followed by 'yes' or 'no' to toggle notification
        'loop' -------------followed by 'on' or 'off' to toggle song loop function
        'speed' ------------followed by a multiplying factor e.g. '1.5x' for 1.5 times faster
        'reset' ------------reset play speed and turn off loop
        'reset all'---------reset all settings to default

    Songs handling:
        'stats' ------------print stats of a song
        'test' -------------to test existing/new score
        'test list'---------Access test folder
                          - 'midi list'
                          - 'nightly list'   Also works the same
                          - 'score list'
	'midi'--------------to access midi files folder
        'edit' -------------followed by an index or name to edit existing scores in test mode
                                # it is highly recommended to use edit function for score editing as it wont affect the
                                  original score and has various functions
        'delete' -----------to recycle songs, note: you need to remove song from 'order.txt' before deleting
                                # 'order' to access order
    Scores creating:
        'test' -------------to test existing/new score
        'new' --------------to create new score with random name
	'new midi'----------import a midi file which can be played, the midi can be:
                            -- a midi file that ends with '.mid'
                            -- a nightly composed file, it ends with '.json'

        Scores editing:
                    During score editing there are some syntax that needs to be followed
                    : brackets must be closed because program reads everything inside a bracket as one
                    Example --(AGCB)--S--D-- will become ["-","-","AGCB","-","-","S","-","-","D","-","-"]
                              ‾‾‾‾‾‾                              ‾‾‾‾‾‾
            Syntax:
                        the program reads the score and go to the next key one by one
                        there are no rest between two adjacent keys

                "-" ---------------means rest for specific seconds
                 A ----------------press "A"
                (ABC) -------------play "ABC" at the same time
                (beat xxx) --------means change time rested per "-" in seconds
                ($$) --------------means nodes that can be skipped to by pressing
                                       'up key' to the previous ($$)
                                       'down key' to the next ($$)
                                   # if theres no more node afterwards the song will end

            Special Key Combinations:
                    Ctrl + Shift + A : edit number of dashes in all lines
                    Ctrl + Shift + E : export sectioned score as nightly file
                    Shift + N : Start/Open current txt
                    N + S : bound mp3 to test score
                    Ctrl + z : Start/open a previous version of the test file (Undo)

    Order editing:
        'order' to edit displayed song order
        'edit order' or 'add order' add songs through command
        'by time' to sort song list by time created
        'by order' to sort song list by order

    Others:
        'cls' to clear screen
        'dark' and 'bright' for dark mode and light mode respectively
        'set' to change permanent settings, You can change:
		>> Genshin app coordinate (the place clicked after selecting a song to play)
                >> width of song list (max_name_length)


##### While playing:

        Play function will be locked after three seconds of not being used
        This is to prevent keys being accidentally pressed while exploring
        (and saving system resources)

        Lock manually using '='
        'shift' to unlock

    When unlocked:
        'k' to play from the start of song
        '[' to continue playing from where you stopped
        '<' for previous song, '>' for next song
        'i' to exit play mode and choose new song

    When song is playing:
        'up' key to go to the previous node
        'down' key to go to the next node
        'left' arrow key to wind back
        'right' arrow key to fast foward

## Technical stuff

It utilizes the `keyboard` and `pyautogui` libraries to simulate keyboard events at an administrator level.

The script provides a command prompt-like interface for song selection and also includes a simple graphical user interface (GUI) when playing a song.



