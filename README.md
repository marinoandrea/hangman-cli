# hangman-software-testing

[![Build Status](https://www.travis-ci.com/marinoandrea/hangman-software-testing.svg?token=oQZSVvHp9LbB8M8icK4Z&branch=main)](https://www.travis-ci.com/marinoandrea/hangman-software-testing)
[![codecov](https://codecov.io/gh/marinoandrea/hangman-software-testing/branch/main/graph/badge.svg?token=0PZNNSXFL5)](https://codecov.io/gh/marinoandrea/hangman-software-testing)

Project repository for the Software Testing course at VU

# Choose a topic
In this project, we chose to create the Hangman Game.
For this, we will adopt the Test Driven Development approach in an Agile setting.


# Software Requirements Specification

## **Introduction**
Hangman is a game that is played with two players.
One player (thinker) chooses a word and the other player (guesser) aims to guess what word the player chose, by guessing one character at a time.
The guesser knows the length of the word that the thinker chose, and there is a limit on the number of wrong characters that the guesser can guess.
If the character is in the word, the thinker fills in all the occurrences of the word.
If it is not in the word, it is wrong and the thinker writes down the character.

In this project, the thinker of the game will be implemented, such that the guesser can guess the words that only the thinker knows.


### *Purpose*
The purpose of this SRS document is to define the requirements of a hangman game and the software to interface with the game. The requirements must contain all information required to write an implementation, derive tests for the implementation, and test an implementation.

This document is intended for implementers(testing and developing) of this specification and for anyone evaluation an implementation implementing this specification.

### *Scope*
There is one software product: the hangman game. This product performs
the interaction with the Player and the management of a game.
The hangman game does not keep a leaderboard or any other statistics not required for a game instance. In addition, the game can only be played on one machine and the game product is not responsible for any kind of network communication.

The goal of the hangman game product is to provide an application to play the similar named game.

### *Definitions*

- **Player**: The user that will use the system to guess words.

- **Difficulty**: <!-- NOTE: we have different options, damian proposed to use this https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html letter classification in order to rank each word using the sum of its components frequency --> 
An extremely complex algorithm is used to divide words in certain classes, based on their probability of being guessed in the game of Hangman.

- **Lives**: The limit of the number of wrong guesses that the Player can make. 

- **State**: The state of the system describes the to be guessed word, all the wrongly guessed characters, the current progress of the word, the number of Lives and the configuration options.

- **Game instance**: A Game instance starts when a word has been chosen by the system and it ends when the Player has either guessed the word, or lost all its Lives while guessing the words.

- **Game Character**: A Game Character is defined as an ASCII character in the range 65 - 90 and 97 - 122.

- **Game Word**: A Game Word is any string containing only Game Characters.

- **Game Dictionary**: A collection of files embedded in the program that contain lists of words classified by their *Difficulty*. 

### *References*

### *Overview*
___
## **Overall description**

### *Product perspective*
The hangman game product is completely self-contained.


#### *System interfaces*
Since the hangman game product is completely self-contained there are no system interfaces.

#### User interfaces

The Players will interface with the program using the command line. 
The Player can start a new game simply by running the binary that will be provided.

The Player can customize the game using the following command line options:
- `-m --min-length` a number specifying the minimum word length that can be randomly selected. It defaults to 2
- `-M --max-length` a number specifying the maximum word length that can be randomly selected. It defaults to undefined
- `-l --lives` a number between 1 and 10 that specifies the number of lives for the next game, defaults to 10
- `-d --difficulty` a number between 1 and 10 that specifies the difficulty for the next game, defaults to 5
<!-- - `-j --jargon` one of: 'computer science', 'mathematics', 'english', defaults to 'english'. -->

On initialization, the program will print basic instructions and rules to the standard output. 
The Player will then be able to choose wether to start a game or to gracefully terminate the application. 

After the game has started, the program will prompt the Player to specify a single character or to guess the full word on each turn. It will then print a graphical representation of the hangman state followed by one of these responses:
- **Error** message
- **Success** message

The possible messages are specified in the 'Functions' section.

When a Player reaches its end (by win/lose conditions), they get notified by an end game message. After the game is over the program prompts the Player to choose whether to start a new game or to terminate the application gracefully. 

#### Hardware interfaces
N/A

#### Software interfaces
<!-- TODO: Describe operating system??? -->

#### Communications interfaces
N/A

#### Memory constraints 
The user's machine should have a minimum of 50Mb of free RAM in order to run this application.
This constraint accounts for both the Python runtime size and the program size. 

#### Operations
N/A

#### Site adaptation requirements


### *Product functions*

### *User characteristics*

### *Constraints*
- The system should only make use of standard libraries.

### *Assumptions and dependencies*

### *Apportioning of requirements*
<!-- won't haves (but may have in the future) -->

The system could potentially have a more involved difficulty configuration setting, choosing from a list of words that belong to that difficulty level.
___
## **Specific requirements**

### *External interfaces*

### *Functions* 
<!-- (functional requirements) -->
- The system shall read Player-provided command-line arguments as specified in the `User Interfaces` section on startup. If a certain option is repeated (that is, there is more than one argument for a given option), the system shall use the last value. 
    - Upon receiving the `-m` or `--minimum-length` option followed by an argument, as long as the program is running, the system shall not pick words with a length lower than the argument. 
    If the provided value is larger than the specified `--maximum-length`, the system shall producean error message and gracefully quit.
    If the provided value is larger than the maximum word length in the game's dictionary then the system shall produce an error message and gracefully quit.
    If the provided value is not an integer, it is less or equal to 2, or larger than the maximum length, the system shall produce an error message indicating that the given argument is incorrect. 

    - Upon receiving the `-M` or `--maximum-length` option followed by an argument, as long as the program is running, the system shall not pick words with a length larger than the argument.
    If the provided value is not an integer, it is less or equal to 2, or less than the specified value for the minimum length, the system shall produce an error message indicating that the given argument is incorrect. 

    - Upon receiving the `-l` or `--lives` option followed by an argument, the system shall verify that the given argument is an integer and in the defined range(as specified in the `User Interfaces` section).
    If the argument is not an integer or outside this defined range, the system shall produce an error message indicating the given argument is incorrect and what values are correct. After this error message the system stops executing.
    If the argument is in this defined range, the system shall use the given argument as the number of lives for all games started during
    this invocation. 

    - Upon receiving the `-d` or `--difficulty`, the system shall <!-- TODO: we do not know how difficulty will work yet -->

- After processing the command-line arguments, the system shall start an instance of a game.

- On the creation of a game instance, the system shall perform the following initialisation steps:
    - The system shall initialize the number of remaining lives in the current instance to the number of lives specified by the command-line `lives` parameter.
    
    - The system shall pick a word from the Game Dictionary based on the difficulty level specified by the command-line `difficulty` parameter, the `minimum-length` parameter and the `maximum-length` parameter.

- After the initialisation step of a game instance, the system shall start a game loop with the created instance.
    - The system shall perform the following three steps in a game loop:
        - The system shall display the current State. <!-- TODO: Specify display -->
        - The system shall prompt the Player for their next guess. 
        A valid guess can be either a Game Character or a Game String. 
        If the guess is a Game Character, the system shall check if the Game Character is already guessed or missed. If the Game Character is already guessed or missed, the system shall give an informative message to the user and not deduct any lives for this move. If the Game Character is not yet guessed or missed, the system shall process the Game Character as a move. <!-- TODO: Add handling of Game String as input and invalid input -->
        - The system shall determine if the current game is finished and act accordingly.
        A game is finished if the remainig lives in the current State reach 0, or if the to be guessed word is guessed. <!-- TODO: Clearly define what guessed means. -->
        If the remainig lives reach 0, the system shall produce an informative message indicating
        that the Player lost, and exit the game loop.
        If the to be guessed word is guessed, the system shall produce an informative message indicating that the Player has won, and exit the game loop.
        If the game is not finished, the system shall repeat the game loop.
    

<!-- TODO: Define the move 'function'. -->

- The system shall only accept strings entered by the Player that consist of uppercase or lowercase characters in the English alphabet, excluding any special characters.

- The system shall inform the Player if an invalid input was entered by writing an error message to the screen, without changing the current State.

- The system shall **inform** the Player whether it guessed the word after a Game instance has ended.

- The system shall ask the Player after a Game instance has ended to start a new Game instance, or to gracefully terminate the program.

- The system shall gracefully terminate the program when the Player sends an EOF-signal, which can be done using the key combination <kbd>ctrl + D</kbd>.

- The system shall thank the Player for playing the game when it gracefully terminates.

- The system shall print error messages to the Player in <span style="color:#BF616A">red</span>.

- The system shall print informational messages to the Player in <span style="color:#5E81AC">blue</span>.

- The system shall print regular State messages to the Player in the default color of the terminal.

### *Performance requirements*
<!-- (nonfunctional requirements) -->


### *Logical database requirements*
This project does not place any data into a database.
Therefore, this section is not applicable.

### *Design constraints*

#### Standards compliance

### *Software system attributes*

#### Reliability

#### Availability

#### Security
This software does not store any persistent data in a database.


#### Maintainability

#### Portability

___
