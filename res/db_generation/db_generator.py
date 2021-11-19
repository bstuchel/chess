""" File: db_generator.py

This file contains the opening database generator given a .pgn file.  
Games using portable game notation (PGN) can be downloaded 
at https://www.ficsgames.org/download.html
"""
import chess
import mysql.connector
import os
import sys


UCI_FILENAME = "uci.txt"


def main(pgn_filename):
    """ Create an openings database using the given pgn file 
    :param str pgn_filename: The name of the pgn file
    """
    clear_db()

    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="briansql",
        database="chess_openings"
        )
    cursor = cnx.cursor(buffered=True)
    convert_to_uci(pgn_filename)

    read_file = open(UCI_FILENAME, 'r')
    write_file = open("output.txt", 'w')

    i = 0
    for line in read_file:       
        if i % 1000 == 0:
            print(i)
        i += 1
        
        if line[0] != '[' and line[0] != ' ':
            move_list = get_move_list(line)
            add_to_database(move_list, cursor)
            write_file.write(line)

    cnx.commit()
    cursor.close()
    cnx.close()

    write_file.close()
    read_file.close()


def clear_db():
    """ Clear the opening database """
    cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="briansql",
    database="chess_openings"
    )

    cursor = cnx.cursor(buffered=True)

    clear_call = "\
    USE chess_openings;\
    DROP TABLE IF EXISTS moves;\
    DROP TABLE IF EXISTS fen;\
    CREATE TABLE fen (\
    name VARCHAR(72) NOT NULL,\
    PRIMARY KEY (name)\
    );\
    CREATE TABLE moves (\
    id INT NOT NULL AUTO_INCREMENT,\
    name VARCHAR(10) NOT NULL,\
    fen VARCHAR(72) NOT NULL,\
    PRIMARY KEY (id),\
    FOREIGN KEY (fen) REFERENCES fen(name)\
    );\
    "
    cursor.execute(clear_call)
    cursor.close()
    cnx.close()


def convert_to_uci(pgn_filename):
    """ Convert portable game notation (PGN) to universal chess 
    interface (UCI) notation and output to UCI_FILENAME
    :param str pgn_filename: The name of the pgn file
    """
    os.system(f"pgn-extract.exe -Wuci --output {UCI_FILENAME} {pgn_filename}")


def get_move_list(game_uci):
    """ Create and return the move list for the given game 
    :param str game_uci: The game moves in uci notation
    :return: The list of the first 20 moves (10 for each side)
    :rtype: list[str]
    """
    move_list = game_uci.split(' ')[:-1]
    if len(move_list) > 20:
        move_list = move_list[:20]
    result_list = []
    for move in move_list:
        if move[-1].isalpha():
            move = move[:-1] + move[-1].lower()
        result_list.append(move)
    return result_list


def add_to_database(move_list, cursor):
    """ Store the move made for each board FEN (Forsyth-Edwards Notation) 
    :param list[str] move_list: The list of moves in uci notation 
    :param mysql.connector.connect.cursor cursor: The cursor for the openings 
        database
    """
    board = chess.Board()
    last_fen = chess.STARTING_BOARD_FEN
    for move_uci in move_list:
        cursor.execute(f"INSERT IGNORE INTO fen (name) VALUES ('{last_fen}');")
        cursor.execute(f"INSERT INTO moves (name, fen) VALUES ('{move_uci}', '{last_fen}');")
        board.push_uci(move_uci)
        last_fen = board.board_fen()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python db_generator.py [pgn file name]")
    else:
        main(sys.argv[1])
