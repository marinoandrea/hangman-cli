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

### _Purpose_

The purpose of this SRS document is to define the requirements of a hangman game and the software to interface with the game. The requirements must contain all information required to write an implementation, derive tests for the implementation, and test an implementation.

This document is intended for implementers(testing and developing) of this specification and for anyone evaluation an implementation implementing this specification.

### _Scope_

There is one software product: the hangman game. This product performs
the interaction with the Player and the management of a game.
The hangman game does not keep a leaderboard or any other statistics not required for a game instance. In addition, the game can only be played on one machine and the game product is not responsible for any kind of network communication.

The goal of the hangman game product is to provide an application to play the similar named game.

### _Definitions_

- **Player**: The user that will use the system to guess words.

- **Difficulty**: Every word gets as its difficulty value, the sum of the weights of every character in the word. The weight of a character is defined as the inverse of its proportion(1).
  Proportion describes how common a character is in a word compared to the least occuring character.
  A higher proportion denotes a higher probability of the character occuring in word, therefore, the inverse gives a lower weight to characters occuring often.

- **Lives**: The limit of the number of wrong guesses that the Player can make.

- **State**: The state of the system describes the to be guessed word, all the wrongly guessed characters, the current progress of the word, the number of Lives and the configuration options.

- **Game instance**: A Game instance starts when a word has been chosen by the system and it ends when the Player has either guessed the word, or lost all its Lives while guessing the words.

- **Game Character**: A Game Character is defined as an ASCII character in the range 65 - 90 and 97 - 122.

- **Game Word**: A Game Word is any string containing only Game Characters.

- **Game Dictionary**: A collection of files embedded in the program containing lists of Game Words classified by their _Difficulty_ into three groups(easy, medium, hard).
  The groups are determined based of the median difficulty of words in one file.

### _References_

1. The [proportion source](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html) used for determining the character proportion values.

### _Overview_

---

## **Overall description**

### _Product perspective_

The hangman game product is completely self-contained.

#### _System interfaces_

Since the hangman game product is completely self-contained, there are no system interfaces.

#### User interfaces

The Players will interface with the program using the command line.
The Player can start a new game simply by running the binary that will be provided.

The Player can customize the game using the following command line options:

- `-m --min-length` a number specifying the minimum word length that can be randomly selected. It defaults to 2
- `-M --max-length` a number specifying the maximum word length that can be randomly selected. It defaults to undefined
- `-l --lives` a number between 1 and 10 that specifies the number of lives for the next game, defaults to 10
- `-d --difficulty` a string being either: 'easy', 'medium', or 'hard', defaults to 'medium'
<!-- - `-j --jargon` one of: 'computer science', 'mathematics', 'english', defaults to 'english'. -->

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

### _Product functions_

### _User characteristics_

### _Constraints_

- The system should only make use of Python standard libraries.

### _Assumptions and dependencies_

### _Apportioning of requirements_

<!-- won't haves (but may have in the future) -->

The system could potentially have a more involved difficulty configuration setting, choosing from a list of words that belong to that difficulty level.

---

## **Specific requirements**

### _External interfaces_

### _Functions_

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

  - Upon receiving the `-d` or `--difficulty`, the system shall verify that the given argument is a string matching one of the possible difficulty levels.
    If the argument does not match any of the possible difficulty levels, the system shall produce an error message indicating the given argument is incorrect and what are correct.
    After this error, the system shall stop executing.

- After processing the command-line arguments, the system shall start an instance of a game.

- On the creation of a game instance, the system shall perform the following initialisation steps:

  - The system shall initialize the number of remaining lives in the current instance to the number of lives specified by the command-line `lives` parameter.

  - The system shall pick a word from the Game Dictionary based on the difficulty level specified by the command-line `difficulty` parameter, the `minimum-length` parameter and the `maximum-length` parameter.
    If no word for configuration can be found, the system shall inform the Player and exit.

- After the initialisation step of a game instance, the system shall start a game loop with the created instance.

  - The system shall perform the following three steps in a game loop:
    - The system shall display the current State. On display, the system shall display the correctly guessed character; the current guess, if any; the misses; and a diagram of the current hangman.
      Every life must have a unique diagram.
    - The system shall determine if the current game is finished and act accordingly.
      A game is finished if the remainig lives in the current State reach 0, or if the to be guessed word is guessed.
      The word is guessed if the all Game Characters are guessed of if the user guesses the Game String correctly.
      If the remainig lives reached 0, the system shall stop the game loop.
      If the Player guessed the Game String correctly, the system shall stop the game loop.
      If the game is not finished, the system shall continue to the prompt action.
    - The system shall prompt the Player for their next guess.
      A valid guess can be either a Game Character or a Game String.
      If the guess is not a valid Game Character or Game String, the system shall inform the Player, not deduct any lives for this move, and move on to the display operation.
      If the guess is a duplicate, the system shall inform the Player, not deduct any lives for this move, and move on to the display operation.
      If the guess is not a duplicate, the system shall process the guess as a move.

- On a move, the system shall check if the move is a Game Character or a Game String

  - If the move is a Game String, the system shall determine if the guess matches the to be guessed Game String.
    If the Game String was already input by the Player on a previous turn, the system shall notify the player and wait for another input.
    If the guess is correct, the system shall make the to be guessed Game String fully public and continue with the display operation.
    If the guess is incorrect, the system shall deduct a live, add the guess to the misses list, and continue to the display operation.
  - If the move is a Game Character, the system shall determine if the to be guessed Game String contains the Game Character.
    If the Game Character was already input by the Player on a previous turn, the system shall notify the player and wait for another input.
    If the Game String contains the Game Character, the system shall make all the occurances of the Game Character public, and continue to the display operation.
    If the Game String does not contain the Game Character, the system shall add the Game Character to the misses list, and continue to the display operation.

- After stopping the game loop, the system shall inform the user accordingly.

  - If the game finished and the Player won, the system shall **inform** the Player that it guessed the Game String.
  - If the game finised and the Player lost, the systam shall **inform** the Player that it did not guess the Game String and inform the Player what the Game String is.

- The system shall ask the Player after a Game instance has ended to start a new Game instance, or to gracefully terminate the program.

- The system shall gracefully terminate the program when the Player sends an EOF-signal, which can be done using the key combination <kbd>ctrl + D</kbd>.

- The system shall thank the Player for playing the game when it gracefully terminates.

- The system shall print error messages to the Player in <span style="color:#BF616A">red</span>.

- The system shall print informational messages to the Player in <span style="color:#5E81AC">blue</span>.

- The system shall print regular State messages to the Player in the default color of the terminal.

### _Performance requirements_

<!-- (nonfunctional requirements) -->

### _Logical database requirements_

This project does not place any data into a database.
Therefore, this section is not applicable.

### _Design constraints_

#### Standards compliance

### _Software system attributes_

#### Reliability

#### Availability

#### Security

This software does not store any persistent data in a database.

#### Maintainability

#### Portability

---
