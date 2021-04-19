<img src="assets/logo.png" height="150px" />

---

[![Build Status](https://www.travis-ci.com/marinoandrea/hangman-software-testing.svg?token=oQZSVvHp9LbB8M8icK4Z&branch=main)](https://www.travis-ci.com/marinoandrea/hangman-software-testing)
[![codecov](https://codecov.io/gh/marinoandrea/hangman-software-testing/branch/main/graph/badge.svg?token=0PZNNSXFL5)](https://codecov.io/gh/marinoandrea/hangman-software-testing)

Project repository for the Software Testing course at VU.

# Choose a topic

In this project, we chose to create the Hangman Game.
For this, we will adopt the Test Driven Development approach in an Agile setting.

# Software Requirements Specification

<!-- This documentation follows the guidelines as specified in the IEEE SRS template, described at: https://canvas.vu.nl/courses/52331/files/3487737?module_item_id=527231 -->

## **Introduction**

Hangman is a game that is played with two players.
One player (thinker) chooses a word and the other player (guesser) aims to guess what word the player chose, by guessing one character at a time.
The guesser knows the length of the word that the thinker chose, and there is a limit on the number of wrong characters that the guesser can guess.
If the character is in the word, the thinker fills in all the occurrences of the word.
If it is not in the word, it is wrong and the thinker writes down the character.

In this project, the thinker of the game will be implemented, such that the guesser can guess the words that only the thinker knows.

### Purpose

The purpose of this SRS document is to define the requirements of a hangman game and the software to interface with the game. The requirements must contain all information required to write an implementation, derive tests for the implementation, and test an implementation.

This document is intended for implementers(testing and developing) of this specification and for anyone evaluation an implementation implementing this specification.

### Scope

There is one software product: the hangman game.
This product performs the interaction with the Player and the management of a game.
The hangman game does not make use of a leaderboard or any other statistics not required for a game instance.
In addition, the game can only be played on one machine and the game product does not make use of any kind of network communication.

The goal of the hangman game product is to provide an application to play the similar named game.

### Intended Audience and Reading Suggestions

The target audience of this document consists mainly of the software testing team, that will use this specification to test the software product.
A secondary target audience is developers.
Future developers may use this documentation to get familiar with the design decisions that were made during the development of this project.
A ternary target audience is the users that will use this software product.

This document is structured in the following way.
First, it provides an overview of the software product.
This overview specifies how and in what environment the software product should be used.
Secondly, the external interfaces are described.
This specifies how the user will be able to interact with the software product on a high level.
Thirdly, the system features are described.
Lastly, the nonfunctional requirements are described.
This specifies how well the software product performs.

All readers are advised to start reading the definitions following this section.
These definitions are used throughout the document and are important for understanding the rest of the document.
In addition to this, the overview section is important to understand the intended use of the software product.

A software testing team is advised to continue reading the functional requirements, followed by the nonfunctional requirements.
The software testing team can use the external references-section as a reference during the testing of the product.

A developer is advised to continue reading the external interfaces, followed by the functional requirements.

A user is advised to continue reading the section on external interfaces.

### Definitions

- **Player**: The user that will use the system to guess words.

- **Difficulty**: Every word gets as its difficulty value, the sum of the weights of every character in the word. The weight of a character is defined as the inverse of its proportion[1].
  Proportion describes how common a character is in a word compared to the least occuring character.
  A higher proportion denotes a higher probability of the character occuring in word, therefore, the inverse gives a lower weight to characters occuring often.

- **Lives**: The limit of the number of wrong guesses that the Player can make.

- **State**: The state of the system describes the to be guessed word, all the wrongly guessed characters, the current progress of the word, the number of Lives and the configuration options.

- **Game instance**: A Game instance starts when a word has been chosen by the system and it ends when the Player has either guessed the word, or lost all its Lives while guessing the words.

- **Game Character**: A Game Character is defined as an ASCII character in the range 97 - 122.

- **Game Word**: A Game Word is any string containing only Game Characters.

- **Game Dictionary**: A collection of files embedded in the program containing lists of Game Words classified by their _Difficulty_ into three groups(easy, medium, hard).
  The groups are determined based of the median difficulty of words in one file.

### References

1. The [proportion source](https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html) used for determining the character proportion values.

## **Overall description**

### Product perspective

The hangman game product is completely self-contained. It is based on an already existing game, but the whole program is built from scratch.

### Product Functions

The user must be able to perform certain actions in the game. The list of actions is as follows:

- Write a letter of the alphabet as a guess, either with or without capital.
- Change the difficulty, with options easy, medium and hard.
- Change the minimum and maximum word length.
- Change the number of lives that a player has ranging from 1 to 10.
- Restart the game when it is over.

### Userclasses and Characteristics

- People who can speak English. The game is supposed to be played by people who know English.
- TAs. In this particular instance, the game is made for the teaching assistents and this course.
- Students that are also inrolled in this course will test our game.

We aim to mostly satisfy the TAs and students, so that they will have a proper game to test and grade. We try to achieve this by testing our game thoroughly, as to minimize errors in the game.
The native language of the students and TAs mostly is not English. However, we know that the people who follow this course are well educated adults that can speak English well. The wordlists we use are of an appropriate difficulty level.

### Operating Environment

The system provides a **Command Line Interface** which will be accessible via a terminal in both the Linux and Windows releases.
No particular assumptions are made about the hardware configuration of the user's machine.
The system expects both the user's OS kernel and the terminal emulator to be fully functional when running the program, there are no other expectations on external software.

### Design and Implementation Constraints

The system msut be designed to potentially allow the use of multiple languages, but for its first release it will only use English. The interface documentation, the in-game feedbacks and messages, and the list of words to guess for this release will only be available in English.

### User Documentation

The user will have access to instructions on the program's configuration settings through the CLI by running the program with the `--help` option.

### Assumptions and Dependencies

The system does not require any external dependency and does not assume anything about the user's platform.
Although, for an optimal experience (i.e. display emojis in the terminal), users are expected to have at least an emoji-capable font (like [Google Noto Color Emoji](https://www.google.com/get/noto/)) installed on their machine.

## **External Interface Requirements**

Since the hangman game product is completely self-contained, there are no system interfaces.

#### User interfaces

The Players will interface with the program using the command line.
The Player can start a new game simply by running the binary that will be provided.

The Player can customize the game using the following command line options:

- `-m --min-length` a number specifying the minimum word length that can be randomly selected. It defaults to 2
- `-M --max-length` a number specifying the maximum word length that can be randomly selected. It defaults to undefined
- `-l --lives` a number between 1 and 10 that specifies the number of lives for the next game, defaults to 10
- `-d --difficulty` a string being either: 'easy', 'medium', or 'hard', defaults to 'medium'

#### Hardware interfaces

The system is purely made out of software components.

#### Software interfaces

The system relies on the underlying OS implementation of basic I/O in order to receive `stdinput` via a terminal and to output to the `stdoutput`.
The Windows release of the system will work on any machine running Windows 8 or newer.
The GNU/Linux release of the system will work on any machine running a Linux distribution.

#### Communications interfaces

The system relies solely on the CLI in order to provide interactive functionality. It does not require any external protocol in order to execute.

#### Memory constraints

The user's machine should have a minimum of 50Mb of free RAM in order to run this application.
This constraint accounts for both the Python runtime size and the program size.

## System Features

### Minimum length

The minimum length feature allows a user to specify a minimum length for the word to be guessed. This feature has
a low priority, because the game can be played without the minimum length feature included.

#### Stimulus/Response

The Player shall set the minimum length via the `-m` or `--minimum-length` option followed by an integer argument.
There is no response from the system, but for the remainder of the program the length of every guess word shall be of atleast the
specified length.

#### Functional

- FREQ-1.1: The system must support the parsing of the feature argument.
- FREQ-1.2: If the provided argument is larger than the _Maximum length_ argument,
  the system shall produce an error message and gracefully quit.
- FREQ-1.3: If the provided argument is not an integer bigger than 2,
  the system shall produce an error message and gracefully quit.
- FREQ-1.4: If there is no word in the dictionary larger or of equal length as the specified argument,
  the system shall produce an error message and gracefully quit.

### Maximum length

The maximum length feature allows a user to specify the maximum length for the word to be guessed in a game instance.

#### Stimulus/Response

The Player shall set the maximum length via the `-M` or `--maximum-length` option followed by an integer argument.
There is no response from the system, but for the remainder of the program the length of every guess word shall be no more
than the specified length.

#### Functional

- FREQ-2.1: The system must support the parsing of the feature argument.
- FREQ-2.2: If the provided argument is not an integer bigger than 2,
  the system shall produce an error message and gracefully quit.

### Lives

The lives feature allows a user to specify the number of lives in a game instance. This corresponds to the amount of guesses
a Player has.

#### Stimulus/Response

The Player shall set the lives via the `-l` or `--lives` option followed by an integer argument in the range of 1 to 10.
There is no response from the system, but for the remainder of the program the number of lives at the start of a game instance shall be equal to the given argument.

#### Functional

- FREQ-3.1: The system must support the parsing of the feature argument.
- FREQ-3.2: If the provided argument is not an integer in the range of 1 to 10,
  the system shall produce an error and gracefully quit.
- FREQ-3.3: If the provided argument is valid, the system shall for this invocation start
  any game with the number of lives provided by the argument.

### Difficulty

The difficulty feature allows a user to specify the difficulty of to be guessed words.

#### Stimulus/Response

The Player shall set the difficulty via the `-d` or `--difficulty` option with the argument being one of 'easy', 'medium', or 'hard'.
There is no response from the system, but for the remainder of the program the word difficulty shall correspond to the given argument.

#### Functional

- FREQ-4.1: The system must support the parsing of the feature argument.
- FREQ-4.2: If the provided argument is not one of 'easy', 'medium', or 'hard',
  the system shall produce an error and gracefully quit.
- FREQ-4.3: If the provided argument is valid, but there is no words in the difficulty level
  that adhere to the length requirement, the system shall produce an error and gracefully quit.
- FREQ-4.4: If the provided argument is valid, the system shall for this invocation
  only pick words the correspond to the specified difficulty.

### Multiple games

The multiple games feature allows a user to play multiple games during one invocation of the program.
This feature does not allow to play multiple games simultaneously.

#### Stimulus/Response

The system shall ask the Player for an input of either 'y' or 'n'. Based on the provided answer,
the system shall stop the program, play a new game, or reask te question.

#### Functional

- FREQ-5.1: After ending a game instance, the system shall
  ask the player to play another game by asking for command-line input of the form of 'y' or 'n'.
- FREQ-5.2: If the provided input is not 'y' nor 'n', the system shall
  repeat the question.
- FREQ-5.3: A Keyboard Interrupt or an EOF character shall be interpreted identical
  to a 'n' input.
- FREQ-5.4: If the Player inputs 'y', the system shall start a new game instance.
- FREQ-5.5: If the Player inputs 'n', the system shall gracefully exit.

### Game Information

The game information feature provides information about the current state of the game to the Player during a game instance.

#### Stimulus/Response

The system shall display the current state on the terminal device. There is no response required from the user.

#### Functional

- FREQ-6.1: The system shall display the current guess, if any; the current word, where correctly guessed character
  are displayed, and character not yet guessed are displayed as an underscore; and a hangman animation.
- FREQ-6.2: The hangman animation shall be unique for the amount of lives a Player has.
- FREQ-6.3: The hangman animation shall become more complete the less lives a Player has.
- FREQ-6.4: When a Player reaches zero lives the hangman must be complete.

### Player guessing

The player guessing feature allows a Player to perform a guess for a Game character or a Game word.

#### Stimulus/Response

The system shall ask the user for input. The user must respond with a valid Game Character or
valid Game String.

#### Functional

- FREQ-7.1: To perform a guess, the system must ask the Player via command-line input.
- FREQ-7.2: If the guess by the Player is not a valid Game String or Game Character,
  the system shall inform the Player that it is not and redo the input request.
- FREQ-7.3: If the guess is a valid Game String, but the length of the guess is not equal
  to the length of the Game String, the system shall inform the Player and redo the input request.
- FREQ-7.4: If the guess is valid and not a duplicate, but the guessed Game Character is not part of the Game String,
  the system shall substract one 'life' from the amount of 'lives'.
- FREQ-7.5: If the guess is valid, a Game String, and not a duplicate, but not equal to the to be guessed Game String,
  the system shall substract one 'life' from the amount of 'lives'.
- FREQ-7.6: If the guess is valid, but a duplicate, the system shall inform the player that it is a duplicate and
  not substract any lives.
- FREQ-7.7: If the Player inputs a EOF character or performs a Keyboard Interrupt during input, the system
  shall end the corresponding Game Instance.

### Winner/Loser

The Winner/Loser feature assign a win-condition to the game.

#### Functional

- FREQ-8.1: The win-condition is if the word is completely guessed, either via Game Character guessing
  or via Game String guessing, before the amount of lives reach zero.
- FREQ-8.2: If the amount of lives reach zero before the word is guessed, the
  system shall inform the Player they lost and display the actual word.
- FREQ-8.3: If the player reaches the win-condition, the system shall inform the
  Player they won.
- FREQ-8.4: Reaching win or lose, results in the end of the corresponding Game Instace.

### Graceful exits

The graceful exits feature provides an indication to the user when the exit was done gracefully.

#### Stimulus/Response

The player shall get a message on the command-line when the system gracefully exits.

#### Functional

- FREQ-9.1: When the system gracefully exits, it shall thank the Player for playing via
  a command-line message.

### Coloured output

The coloured output feature provides a clear distinction
between the different type of messages.

#### Functional

- FREQ-10.1: The system shall print error messages to the Player with red as the foreground color via escape code '31' in the terminal.

- FREQ-10.2: The system shall print informational messages to the Player with light cyan as the foreground color via escape code '96' in the terminal.

- FREQ-10.3: The system shall print regular messages to the Player without any color modifications from our side.

## _Other Nonfunctional Requirements_

### Performance requirements

The system shall execute the game's logic for each turn in under 2 seconds on any system with the following minimum configuration:

- 2.6Ghz 2 core CPU
- 4GB of DDR3/DDR4 RAM
- SSD/HDD with 100MB/s write speed

### Safety Requirements

The system shall not, in any way, render the user's system unoperable while it is running.

### Security Requirements

The system shall not use, excluding user input, an amount of memory greater than what specified in the 'Memory Constraints' section and it shall not access unauthorized memory in the user's system.

### Software Quality Attributes

The system shall be built according to industry standards and its development process shall feature:

- Continuous Integration system
  - build shall be `passing` before release
- Code coverage monitoring
  - test code coverage shall be over 90% before release
- reasonable versioning and coding policies including:
  - meaningful and documented commits
  - source level documentation for the core functionalities
  - idiomatic use of the Python language and standard libraries
  - adherence to PEP8 specification for code formatting
  - adherence to `flake8` linting specification (no error flags are allowed)

### Business Rules

The system shall only have one type of user: the Player.

---
