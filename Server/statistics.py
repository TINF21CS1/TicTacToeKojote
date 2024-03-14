import emoji
import sqlite3
import os
from Server.player import Player
from Server.gamestate import GameState


class Statistics:
    def __init__(self, path: str = os.path.abspath('Server/Data/statistics.db')) -> None:
        """
        Initializes the statistics object by creating a connection to the database
        and creating the table if it doesn't exist
        :param path: path to db file, default is './Data/statistics.db'
        """
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        with self.conn:
            self.cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS statistics(
                    uuid TEXT,
                    display_name TEXT,
                    color INT,
                    wins_first INT,
                    wins_second INT,
                    losses_first INT,
                    losses_second INT,
                    draws_first INT,
                    draws_second INT,
                    moves INT, 
                    emojis INT
                    )
                    """)

    def get_statistics(self):
        """
        Returns the statistics of all players
        :return: all statistics
        """
        with self.conn:
            self.cursor.execute(f"""
            SELECT * FROM statistics
            """)
            return self.cursor.fetchall()

    def increment_emojis(self, player: Player, message: str) -> None:
        """
        Counts the emojis in the given message and updates the emoji
        statistics of a profile by its uuid
        :param player:
        :param message: message that is checked for emojis
        """
        uuid = str(player.uuid)
        self.__update_emojis(uuid, emoji.emoji_count(message))

    def increment_moves(self, player: Player) -> None:
        """
        Increments the moves of a profile by its uuid
        :param player:
        """
        uuid = str(player.uuid)
        if self.__check_profile(uuid):
            with self.conn:
                self.cursor.execute(f"""
                UPDATE statistics
                SET moves = moves + 1
                WHERE uuid = ?
                """, (uuid,))
        else:
            self.__add_profile(player, moves=1)

    def increment_wins_fromstate(self, player_list: list[Player], winner: int, starting_player: int) -> None:
        """
        Increments the wins of a both players by their player objects
        :param gamestate:
        :param player_list:
        """
        if not self.__check_profile(str(player_list[1].uuid)):
            self.__add_profile(player_list[1])
        if not self.__check_profile(str(player_list[2].uuid)):
            self.__add_profile(player_list[2])

        player1 = ""
        player2 = ""
        if starting_player == 1:
            player1 = "first"
            player2 = "second"
        elif starting_player == 2:
            player1 = "second"
            player2 = "first"
        else:
            raise ValueError('Invalid starting player')
        if winner == 1:
            self.__increment_games(player_list[1], "wins_" + player1)
            self.__increment_games(player_list[2], "losses_" + player2)
        elif winner == 2:
            self.__increment_games(player_list[2], "wins_" + player2)
            self.__increment_games(player_list[1], "losses_" + player1)
        elif winner == 0:
            self.__increment_games(player_list[1], "draws_" + player1)
            self.__increment_games(player_list[2], "draws_" + player2)
        else:
            raise ValueError('Invalid winner')

    def __increment_games(self, player: Player, type: str) -> None:
        """
        Updates the wins of a profile by its uuid
        :param uuid: uuid of the profile that is updated
        :param type: type of the win, can be:
        'wins_first' (if player started the round), 'wins_second' (if other player started the round),
        'draws_first', 'draws_second', 'losses_first', 'losses_second'
        """
        uuid = str(player.uuid)
        if type not in ['wins_first', 'wins_second', 'draws_first', 'draws_second', 'losses_first', 'losses_second']:
            raise ValueError('Invalid type')
        if self._check_profile(uuid):
            with self.conn:
                self.cursor.execute(f"""
                   UPDATE statistics
                   SET {type} = {type} + 1
                   WHERE uuid = ?
                   """,
                                    (uuid,))
        else:
            self.__add_profile(player, wins_first=1 if type == 'wins_first' else 0,
                               wins_second=1 if type == 'wins_second' else 0,
                               draws_first=1 if type == 'draws_first' else 0,
                               draws_second=1 if type == 'draws_second' else 0,
                               losses_first=1 if type == 'losses_first' else 0,
                               losses_second=1 if type == 'losses_second' else 0)

    def __update_emojis(self, uuid: str, count: int) -> None:
        """
        Updates the emojis of a profile by its uuid
        :param uuid: uuid of the profile that is updated
        :param count: count of emojis that are added to the statistics
        """
        if self.__check_profile(uuid):
            with self.conn:
                self.cursor.execute(f"""
                UPDATE statistics
                SET emojis = emojis + ?
                WHERE uuid = ?
                """, (count, uuid,))
        else:
            self.__add_profile(uuid, emojis=count)

    def __check_profile(self, uuid: str) -> bool:
        """
        Checks if a profile with the given uuid exists
        :param uuid: uuid of the profile that is checked
        :return: True if the profile exists, False if it doesn't
        """
        with self.conn:
            self.cursor.execute(f"""
            SELECT * FROM statistics
            WHERE uuid = ?
            """, (uuid,))
            return True if self.cursor.fetchone() is not None else False

    def __add_profile(self, player: Player, wins_first: int = 0, wins_second: int = 0,
                      draws_first: int = 0, draws_second=0, losses_first: int = 0,
                      losses_second: int = 0, moves: int = 0,
                      emojis: int = 0) -> None:
        """
        Adds a new profile to the database
        :param uuid: uuid of the profile that is added
        :param wins_first: wins if player started the round
        :param wins_second: wins if other player started the round
        :param draws_first: draws if player started the round
        :param draws_second: draws if other player started the round
        :param losses_first: losses if player started the round
        :param losses_second: losses if other player started the round
        :param moves: moves made by the profile
        :param emojis: emojis used by the profile
        """

        uuid = str(player.uuid)
        display_name = player.display_name
        color = player.color
        ready = player.ready
        with self.conn:
            self.cursor.execute(f"""
            INSERT INTO statistics
            VALUES (
            :uuid,
            :display_name,
            :color,
            :wins_first, 
            :wins_second, 
            :losses_first,
            :losses_second,
            :draws_first,
            :draws_second,
            :moves, 
            :emojis
            )
            """, {'uuid': uuid, 'display_name': display_name, 'color': color, 'wins_first': wins_first,
                  'wins_second': wins_second,
                  'losses_first': losses_first, 'losses_second': losses_second, 'draws_first': draws_first,
                  'draws_second': draws_second, 'moves': moves, 'emojis': emojis})
