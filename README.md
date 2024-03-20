# TicTacToeKojote

This is a simple TicTacToe game written in Python. It can be played by two players in a GUI. However, it works best on Windows. Bugs may occur on other operating systems.

## Installation

- Install [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Clone the repository: `git clone https://github.com/TINF21CS1/TicTacToeKojote.git`
- Alternative to installing Git and cloning the repository: Press the green `Code`-Button on the GitHub Repository in the Browser and click `Download ZIP`. Afterwards, right click the ZIP-file and click unzip.
- Install Python 3.11 or higher from [python.org](https://www.python.org/downloads/)
- Install the required packages by running `pip install -r requirements.txt` from the root directory of the project
- Run the game by executing `python main.py` from the root directory of the project
- To play against other players in the network, you have to configure your local firewall to allow incoming traffic on port 8765
    - Alternatively, you can turn off the firewall on both clients

## Features

- Play TicTacToe with a friend online
- Play TicTacToe with a friend offline
- Play TicTacToe against an AI (weak or strong)
- Chat with your opponent during the game
- Create Profiles
- View your game statistics whenever you are connected to a server

## How to play

- **Manage your player profiles:** View Use Case 1: Manage Player Profiles
- **Play against AI:** View the corresponding [sequence diagram](docs/sequence_diagrams/play_vs_ai.png)
- **Play against another player locally:** View the corresponding [sequence diagram](docs/sequence_diagrams/play_locally.png)
- **Host an online game:** View Use Case 3.1: Host Game
- **Join an online game:** View Use Case 3.2: Join Game
- **Leave an online game:** View Use Case 3.3: Leave Game
- **Send Chat messages:** View Use Case 4: Chat
- **Display the statistics:** View Use Case 5: Display Statistics
