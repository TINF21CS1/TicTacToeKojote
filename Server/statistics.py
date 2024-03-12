import emoji
import sqlite3
import os


class Statistics:
    def __init__(self, path: str = os.path.abspath('Server/Data/statistics.db')) -> None:
        """
        Initializes the statistics object by creating a connection to the database
        and creating the table if it doesn't exist
        :param path: path to db file, default is './Data/statistics.db'
        """
        self.path = path
        print(path)
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        with self.conn:
            self.cursor.execute(f"""
                    CREATE TABLE IF NOT EXISTS statistics(
                    uuid TEXT,
                    wins_first INT,
                    wins_second INT,
                    loses_first INT,
                    loses_second INT,
                    draws_first INT,
                    draws_second INT,
                    moves INT, 
                    emojis INT
                    )
                    """)

    """
    ________Public Methods_________
    ________Main Methods___________
    """

    def get_statistics(self, uuid: str) -> tuple:
        """
        Returns the statistics of a profile by its uuid
        :param uuid: uuid of the profile that is searched
        :return: tuple containing:
        (uuid : str, wins_first : int, wins_second : int, loses_first : int,
        loses_second : int, draws_first : int, draws_second, moves : int, emojis : int)
        """
        return self._get_profile(uuid)

    def get_all_statistics(self) -> list:
        """
        Returns all statistics from the database
        :return: an array of tuples containing:
        (uuid : str, wins_first : int, wins_second : int, loses_first : int,
        loses_second : int, draws : int, moves : int, emojis : int)
        """
        with self.conn:
            self.cursor.execute(f"""
            SELECT * FROM statistics
            """)
            return self.cursor.fetchall()

    def add_profile(self, uuid: str, wins_first: int = 0, wins_second: int = 0, loses_first: int = 0,
                    loses_second: int = 0, draws_first: int = 0, draws_second = 0, moves: int = 0, emojis: int = 0
                    ) -> None:
        """
        Adds a new profile to the database
        :param uuid: uuid of the profile that is added
        :param wins_first: wins if player started the round
        :param wins_second: wins if other player started the round
        :param loses_first: loses if player started the round
        :param loses_second: loses if other player started the round
        :param draws_first: draws if player started the round
        :param draws_second: draws if other player started the round
        :param moves: moves made by the profile
        :param emojis: emojis used by the profile
        :return:
        """
        self._add_profile(uuid, wins_first = wins_first, wins_second = wins_second,
                          loses_first = loses_first, loses_second = loses_second,
                          draws_first = draws_first, draws_second = draws_second,
                          moves = moves, emojis = emojis)

    def update_statistics(self, uuid: str, type: str, moves: int) -> None:
        """
        Updates the statistics of a profile by its uuid
        :param uuid: uuid of the profile that is updated
        :param type: type of the update, can be:
        'wins_first' (if player started the round), 'wins_second' (if other player started the round),
        'draws_first', 'draws_second', 'loses_first', 'loses_second'
        :param moves: number of moves that were made in the game
        """
        if type not in ['wins_first', 'wins_second', 'draws_first', 'draws_second', 'loses_first', 'loses_second']:
            raise ValueError('Invalid type')
        self._update_wins(uuid, type)
        self._update_moves(uuid, moves)

    def count_emojis(self, uuid: str, message: str) -> None:
        """
        Counts the emojis in the given message and updates the emoji
        statistics of a profile by its uuid
        :param uuid: uuid of the profile that is updated
        :param message: message that is checked for emojis
        """
        self._update_emojis(uuid, emoji.emoji_count(message))

    """
    ________Delete Methods_________
    """
    def delete_statistics(self, uuid: str) -> None:
        """
        Deletes statistics of a profile by its uuid
        :param uuid: uuid of the profile that is deleted
        """
        if self._check_profile(uuid):
            with self.conn:
                self.cursor.execute(f"""
                DELETE FROM statistics
                WHERE uuid = '{uuid}'
                """)
        else:
            raise ValueError(f'Statistics for uuid: {uuid} does not exist')

    def delete_all_statistics(self):
        """
        Deletes all statistics from the database
        """
        with self.conn:
            self.cursor.execute(f"""
              DELETE FROM statistics
              """)
    """
    ________Reset Methods_________
    """
    def reset_statistics(self, uuid: str, arg: str):
        """
        Resets an argument value of a profile by its uuid to 0
        :param uuid: uuid of the profile that is reset
        :param arg: statistics that is get reseted, hast to be one of those:
        'wins_first', 'wins_second', 'loses_first', 'loses_second', 'draws_first', 'draws_second', 'emojis', 'moves'
        :return:
        """
        if arg not in ['wins_first', 'wins_second' 'loses_first', 'loses_second',
                       'draws_first', 'draws_secons', 'emojis', 'moves']:
            raise ValueError('Invalid type')
        if self._check_profile(uuid):
            with self.conn:
                self.cursor.execute(f"""
                UPDATE statistics
                SET {arg} = 0
                WHERE uuid = '{uuid}'
                """)
        else:
            raise ValueError(f'Statistics for uuid: {uuid} does not exist')
    """
    ________Get Methods___________
    """

    def get_winrates(self, uuid: str, type: str = "all") -> float:
        """
        Returns the winrate of a profile by its uuid
        :param uuid: uuid of the profile that is searched
        :param type: type of the winrate, can be:
        'first' (if player started the round), 'second' (if other player started the round), 'all' (overall)
        standard is 'all'
        :return: winrate as a float
        """
        if type not in ['first', 'second', 'all']:
            raise ValueError('Invalid type')
        if self._check_profile(uuid):
            profile = self._get_profile(uuid)
            if type == 'all':
                return (profile[1] + profile[2]) / (profile[1] + profile[2] + profile[3] + profile[4])
            elif type == 'first':
                return profile[1] / (profile[1] + profile[3])
            elif type == 'second':
                return profile[2] / (profile[2] + profile[4])
        else:
            raise ValueError(f'Statistics for uuid: {uuid} does not exist')

    def get_emojis(self, uuid: str) -> int:
        """
        Returns the number of emojis used by a profile by its uuid
        :param uuid: uuid of the profile that is searched
        :return: number of emojis as an int
        """
        if self._check_profile(uuid):
            profile = self._get_profile(uuid)
            return profile[8]
        else:
            raise ValueError(f'Statistics for uuid: {uuid} does not exist')

    def get_moves(self, uuid: str) -> int:
        """
        Returns the number of moves made by a profile by its uuid
        :param uuid: uuid of the profile that is searched
        :return: number of moves as an int
        """
        if self._check_profile(uuid):
            profile = self._get_profile(uuid)
            return profile[7]
        else:
            raise ValueError(f'Statistics for uuid: {uuid} does not exist')

    def get_wins(self, uuid: str, type='all') -> int:
        """
        Returns the number of wins of a profile by its uuid
        :param uuid: uuid of the profile that is searched
        :param type: type of wins, can be:
        'first' (if player started the round), 'second' (if other player started the round), 'all' (overall)
        standard is 'all'
        :return: number of wins as an int
        """
        if type not in ['first', 'second', 'all']:
            raise ValueError('Invalid type')
        if self._check_profile(uuid):
            profile = self._get_profile(uuid)
            if type == 'all':
                return profile[1] + profile[2]
            elif type == 'first':
                return profile[1]
            elif type == 'second':
                return profile[2]
        else:
            raise ValueError(f'Statistics for uuid: {uuid} does not exist')

    def get_loses(self, uuid: str, type='all') -> int:
        """
        Returns the number of loses of a profile by its uuid
        :param uuid: uuid of the profile that is searched
        :param type: type of loses, can be:
        'first' (if player started the round), 'second' (if other player started the round), 'all' (overall)
        standard is 'all'
        :return: number of loses as an int
        """
        if type not in ['first', 'second', 'all']:
            raise ValueError('Invalid type')
        if self._check_profile(uuid):
            profile = self._get_profile(uuid)
            if type == 'all':
                return profile[3] + profile[4]
            elif type == 'first':
                return profile[3]
            elif type == 'second':
                return profile[4]
        else:
            raise ValueError(f'Statistics for uuid: {uuid} does not exist')

    def get_draws(self, uuid: str, type: str = 'all') -> int:
        """
        Returns the number of draws of a profile by its uuid
        :param uuid: uuid of the profile that is searched
        :param type: type of draws, can be:
        'first' (if player started the round), 'second' (if other player started the round), 'all' (overall)
        standard is 'all'
        :return: number of draws as an int
        """
        if type not in ['first', 'second', 'all']:
            raise ValueError('Invalid type')
        if self._check_profile(uuid):
            profile = self._get_profile(uuid)
            if type == 'all':
                return profile[5] + profile[6]
            elif type == 'first':
                return profile[5]
            elif type == 'second':
                return profile[6]
        else:
            raise ValueError(f'Statistics for uuid: {uuid} does not exist')

    """
    ________Private Methods_________
    
    ________Update Methods__________
    
    All update functions add new profiles if they don't exist
    """

    def _update_wins(self, uuid: str, type: str) -> None:
        """
        Updates the wins of a profile by its uuid
        :param uuid: uuid of the profile that is updated
        :param type: type of the win, can be:
        'wins_first' (if player started the round), 'wins_second' (if other player started the round),
        'draws_first', 'draws_second', 'loses_first', 'loses_second'
        """
        if type not in ['wins_first', 'wins_second', 'draws_first', 'draws_second', 'loses_first', 'loses_second']:
            raise ValueError('Invalid type')
        if self._check_profile(uuid):
            with self.conn:
                self.cursor.execute(f"""
                UPDATE statistics
                SET {type} = {type} + 1
                WHERE uuid = '{uuid}'
                """)
        else:
            self._add_profile(uuid, wins_first=1 if type == 'wins_first' else 0,
                              wins_second=1 if type == 'wins_second' else 0,
                              draws_first=1 if type == 'draws_first' else 0,
                              draws_second= 1 if type == 'draws_second' else 0,
                              loses_first=1 if type == 'loses_first' else 0,
                              loses_second=1 if type == 'loses_second' else 0)

    def _update_moves(self, uuid: str, moves: int) -> None:
        """
        Updates the moves of a profile by its uuid
        :param uuid: uuid of the profile that is updated
        :param moves: moves that are added to the statistics
        """
        if self._check_profile(uuid):
            with self.conn:
                self.cursor.execute(f"""
                UPDATE statistics
                SET moves = moves + {moves}
                WHERE uuid = '{uuid}'
                """)
        else:
            self._add_profile(uuid, moves=moves)

    def _update_emojis(self, uuid: str, count: int) -> None:
        """
        Updates the emojis of a profile by its uuid
        :param uuid: uuid of the profile that is updated
        :param count: count of emojis that are added to the statistics
        """
        if self._check_profile(uuid):
            with self.conn:
                self.cursor.execute(f"""
                UPDATE statistics
                SET emojis = emojis + :emoji
                WHERE uuid = '{uuid}'
                """, {'emoji': count})
        else:
            self._add_profile(uuid, emojis=count)

    """
    _________Check Methods_________    
    """

    def _check_profile(self, uuid: str) -> bool:
        """
        Checks if a profile with the given uuid exists
        :param uuid: uuid of the profile that is checked
        :return: True if the profile exists, False if it doesn't
        """
        with self.conn:
            self.cursor.execute(f"""
            SELECT * FROM statistics
            WHERE uuid = '{uuid}'
            """)
            return True if self.cursor.fetchone() is not None else False

    """
    _________Get Methods_________
    """

    def _get_profile(self, uuid: str) -> tuple:
        """
        Returns the profile by its uuid
        :param uuid: uuid of the profile that is searched
        :return: profile statistics as a tuple
        """
        if not self._check_profile(uuid):
            raise ValueError(f'Statistics for uuid: {uuid} does not exist')
        with self.conn:
            self.cursor.execute(f"""
            SELECT * FROM statistics
            WHERE uuid = '{uuid}'
            """)
            return self.cursor.fetchone()

    """
    _________Add Methods_________
    """

    def _add_profile(self, uuid: str, wins_first: int = 0, wins_second: int = 0,
                     draws_first: int = 0, draws_second = 0, loses_first: int = 0,
                     loses_second: int = 0, moves: int = 0,
                     emojis: int = 0) -> None:
        """
        Adds a new profile to the database
        :param uuid: uuid of the profile that is added
        :param wins_first: wins if player started the round
        :param wins_second: wins if other player started the round
        :param draws_first: draws if player started the round
        :param draws_second: draws if other player started the round
        :param loses_first: loses if player started the round
        :param loses_second: loses if other player started the round
        :param moves: moves made by the profile
        :param emojis: emojis used by the profile
        """
        with self.conn:
            self.cursor.execute(f"""
            INSERT INTO statistics
            VALUES (
            :uuid, 
            :wins_first, 
            :wins_second, 
            :loses_first,
            :loses_second,
            :draws_first,
            :draws_second,
            :moves, 
            :emojis
            )
            """, {'uuid': uuid, 'wins_first': wins_first, 'wins_second': wins_second,
                  'loses_first': loses_first, 'loses_second': loses_second, 'draws_first': draws_first, 'draws_second': draws_second, 'moves': moves, 'emojis': emojis})

