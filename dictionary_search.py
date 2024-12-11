from itertools import permutations
from collections import deque
import re


def check_dictionary_exists(filename, input_string):

    my_file = open(filename, "r")

    # reading the file
    data = my_file.read()

    # replacing end of line('/n') with ' ' and
    # splitting the text it further when '.' is seen.
    data_into_list = set(data.split("\n"))

    # printing the data

    exists = input_string in data_into_list
    return exists


dict_filename = "dictionary.txt"
input = "SBAD"


def permutation_check(filename, input):
    # of length n*n/2
    n = len(input)
    candidate_list = deque([input])
    subst_list = set([])
    while candidate_list:
        curr_candidate = candidate_list.popleft()
        if len(curr_candidate) == 0:
            break
        subst_list.add(curr_candidate)
        for i in range(len(curr_candidate)):
            next_candidate = curr_candidate[:i] + curr_candidate[i + 1 :]
            candidate_list.append(next_candidate)

    ss_perm_list = []
    for subst in subst_list:
        ss_perm_list.extend(["".join(p) for p in permutations(subst)])
    ss_perm_list = set(ss_perm_list)

    output_list = []
    for ss_perm in ss_perm_list:
        if check_dictionary_exists(filename, ss_perm):
            output_list.append(ss_perm)
    return output_list


# check = permutation_check(filename, input)
# print(f"len: {len(check)}, check: {check}")


def is_board_valid(board, dictionary_file):
    # a board is invalid if no center tile
    if board[7][7] == ".":
        print(f"center unoccupied")
        return False

    # check for vertical words
    vertical_words = []
    for i in range(15):
        current_word = ""
        for j in range(15):
            if board[i][j] != ".":
                current_word += board[i][j]
            else:
                if len(current_word) > 1:
                    vertical_words.append(current_word)
                current_word = ""

    # check for horizontal words
    horizontal_words = []
    for j in range(15):
        current_word = ""
        for i in range(15):
            if board[i][j] != ".":
                current_word += board[i][j]
            else:
                if len(current_word) > 1:
                    horizontal_words.append(current_word)
                current_word = ""
    for word in vertical_words + horizontal_words:
        if not check_dictionary_exists(dictionary_file, word):
            print(f"invalid word: {word}")
            return False

    # make sure everything is connected
    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    nodes_to_check = deque([(7, 7)])
    while nodes_to_check:
        i, j = nodes_to_check.popleft()
        board[i][j] = "."
        for dx, dy in dirs:
            new_i, new_j = i + dx, j + dy
            if board[new_i][new_j] != ".":
                nodes_to_check.append((new_i, new_j))
    # check if there are still any non-"." nodes
    for line in board:
        if re.search(r"[^.]", "".join(line)):
            print(f"dangling connection")
            return False

    return True


# replacing end of line('/n') with ' ' and
# splitting the text it further when '.' is seen.
# load in boards
filename = "boards.txt"
my_file = open(filename, "r")

# reading the file
data = my_file.read()
boards = data.split("\n\n\n")
index = 2
print(boards[index])
read_boards = []
valid_list = []
for board in boards:
    read_board = board.split("\n")
    out_board = []
    for line in read_board:
        out_board.append(list(line))
    read_boards.append(out_board)

board_validity = []
for board in read_boards:
    board_validity.append(is_board_valid(board, dict_filename))
print(board_validity)
