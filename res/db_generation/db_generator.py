import chess
import mysql.connector
import os
import sys


UCI_FILENAME = "uci.txt"


def main(pgn_filename):
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

    # max_line = 200
    i = 0
    for line in read_file:       
        # if i > max_line:
        #     break
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
    # cnx.commit()
    cursor.close()
    cnx.close()


def convert_to_uci(pgn_filename):
    os.system(f"pgn-extract.exe -Wuci --output {UCI_FILENAME} {pgn_filename}")


def get_move_list(game_uci):
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
    board = chess.Board()
    last_fen = chess.STARTING_BOARD_FEN
    for move_uci in move_list:
        # try:
        cursor.execute(f"INSERT IGNORE INTO fen (name) VALUES ('{last_fen}');")
        cursor.execute(f"INSERT INTO moves (name, fen) VALUES ('{move_uci}', '{last_fen}');")
        # except mysql.connector.Error as err:
        #     print(f"Failed creating database: {err}")
        #     exit(1)
        board.push_uci(move_uci)
        last_fen = board.board_fen()


if __name__ == "__main__":
    main(sys.argv[1])
