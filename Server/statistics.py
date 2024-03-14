import emoji
import sqlite3
import os

from Server.player import Player


class Statistics:
    """
    Handle Statistics and Writing to permanent storage.

    Methods:
    get_statistics() -> list: returns all statistics
    increment_emojis(player: Player, message: str) -> None: counts the emojis in the given message and updates the emoji statistics of a profile by its player object
    increment_moves(player: Player) -> None: increments the moves of a profile by its player object
    increment_games(player_list: list[Player], winner: int) -> None: increments the wins and losses of both players by their player objects

    Private Methods:
    _increment_win(player: Player) -> None: increments the wins of a profile by its player object
    _increment_loss(player: Player) -> None: increments the losses of a profile by its player object
    _increment_draws(player: Player) -> None: increments the draws of a profile by its player object
    _check_add_profile(player: Player) -> None: checks if a profile with the given uuid exists and adds it if it doesn't
    _check_profile(uuid: str) -> bool: checks if a profile with the given uuid exists
    _add_profile(player: Player) -> None: adds a new profile to the database
    """


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
                wins INT,
                losses INT,
                draws INT,
                moves INT, 
                emojis INT
                )
                """)


    def get_statistics(self) -> list:
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

        self._check_add_profile(player)

        with self.conn:
            self.cursor.execute(f"""
            UPDATE statistics
            SET emojis = emojis + ?
            WHERE uuid = ?
            """,
            (emoji.emoji_count(message), str(player.uuid)))

    def increment_moves(self, player: Player) -> None:
        """
        Increments the moves of a profile by its uuid
        :param player:
        """

        self._check_add_profile(player)

        with self.conn:
            self.cursor.execute(f"""
            UPDATE statistics
            SET moves = moves + 1
            WHERE uuid = ?
            """, (str(player.uuid),))

    def increment_games(self, player_list: list[Player], winner: int) -> None:
        """
        Increments the wins and losses of both players by their player objects
        :param player_list: list of None, player1, player2
        :param winner: 0 if draw, 1 if player1 wins, 2 if player2 wins
        """

        self._check_add_profile(player_list[1].uuid)
        self._check_add_profile(player_list[2].uuid)

        if winner == 0:
            self._increment_draws(player_list[1])
            self._increment_draws(player_list[2])
        elif winner == 1:
            self._increment_win(player_list[1])
            self._increment_loss(player_list[2])
        elif winner == 2:
            self._increment_win(player_list[2])
            self._increment_loss(player_list[1])
        else:
            raise ValueError("Winner must be 0, 1 or 2")

    def _increment_win(self, player: Player) -> None:
        """
        Increments the wins of a profile by its uuid
        :param player: player object of the profile that is updated
        """

        self._check_add_profile(player)

        with self.conn:
            self.cursor.execute(f"""
                UPDATE statistics
                SET wins = wins + 1
                WHERE uuid = ?
                """,
                (str(player.uuid),)
            )
    
    def _increment_loss(self, player: Player) -> None:
        """
        Increments the losses of a profile by its uuid
        :param player: player object of the profile that is updated
        """

        self._check_add_profile(player)

        with self.conn:
            self.cursor.execute(f"""
                UPDATE statistics
                SET losses = losses + 1
                WHERE uuid = ?
                """,
                (str(player.uuid),)
            )
    
    def _increment_draws(self, player: Player) -> None:
        """
        Increments the draws of a profile by its uuid
        :param player: player object of the profile that is updated
        """

        self._check_add_profile(player)

        with self.conn:
            self.cursor.execute(f"""
                UPDATE statistics
                SET draws = draws + 1
                WHERE uuid = ?
                """,
                (str(player.uuid),)
            )


    def _check_add_profile(self, player: Player) -> None:
        """
        Checks if a profile with the given uuid exists and adds it if it doesn't
        :param uuid: uuid of the profile that is checked
        :return: True if the profile exists, False if it doesn't
        """
        if not self._check_profile(player.uuid):
            self._add_profile(player)

    def _check_profile(self, uuid: str) -> bool:
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

    def _add_profile(self, player: Player) -> None:
        """
        Adds a new profile to the database
        :param player: player object of the profile that is added
        """
        with self.conn:
            self.cursor.execute(f"""
                INSERT INTO statistics
                VALUES (
                :uuid,
                :display_name,
                :color,
                :wins,
                :losses,
                :draws,
                :moves,
                :emojis
                )
                """,
                {'uuid': str(player.uuid), 'display_name': player.display_name, 'color': player.color,
                    'wins': 0, 'losses': 0, 'draws': 0,
                    'moves': 0, 'emojis': 0}
            )
