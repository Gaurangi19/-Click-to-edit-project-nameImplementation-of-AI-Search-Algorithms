import sys
import getopt

cmd_input = False
try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:h', ['input=', 'help'])
except getopt.GetoptError:
    print "Please enter -i <input file name>"
    sys.exit(2)

for opt, arg in opts:
    if opt in ('-h', '--help'):
        print "Please enter -i <input file name>"
        sys.exit(2)
    elif opt in ('-i', '--input'):
        in_file = arg.strip()
        if len(in_file) > 0:
            cmd_input = True
        else:
            cmd_input = False
    else:
        print "Please enter -i <input file name>"
        sys.exit(2)

if cmd_input == False:
    print "Please enter -i <input file name>"
    sys.exit(2)
    
#read input file and store the values
input_file = open(in_file, "r")

algo_type = int(input_file.readline())
if algo_type == 4:
    player1 = input_file.readline().strip()
    player1_algo = int(input_file.readline())
    player1_cutoff_depth = int(input_file.readline())
    player2 = input_file.readline().strip()
    player2_algo = int(input_file.readline())
    player2_cutoff_depth = int(input_file.readline())
else:
    player = input_file.readline().strip()
    if player == "X":
        opponent = "O"
    else:
        opponent = "X"
    player_cutoff_depth = int(input_file.readline())

values = []
value_row = []
for i in range(0,5):
    values = input_file.readline().split()
    value_row.append(values)

positions = []
position_row = []
for i in range(0,5):
    positions = input_file.readline().split()
    position_row.append(positions)

input_file.close()

#store board values in grid list
grid = []  
for i in range(0,5):
    grid_row = []
    for j in range(0,5):
        grid_row.append({"value": int(value_row[i][j]), "occupied": position_row[i][0][j]})
    grid.append(grid_row)

#check if operation is raid or sneak
def check_raid(r,c,raid_player):
    raid_flag = False
    if (r - 1) >= 0:
        if (grid[r-1][c]["occupied"] == raid_player):
            raid_flag = True
    if (c - 1) >= 0:
        if (grid[r][c-1]["occupied"] == raid_player):
            raid_flag = True
    if (r + 1) <= 4:
        if (grid[r+1][c]["occupied"] == raid_player):
            raid_flag = True
    if (c + 1) <= 4:
        if (grid[r][c+1]["occupied"] == raid_player):
            raid_flag = True
    return raid_flag

#calulate evaluation function for greedy raid operation
def eval_raid(r,c,raid_opponent):
    eval_value = grid[r][c]["value"]
    if (r - 1) >= 0:
        if (grid[r-1][c]["occupied"] == raid_opponent):
            eval_value += grid[r-1][c]["value"] * 2
    if (c - 1) >= 0:
        if (grid[r][c-1]["occupied"] == raid_opponent):
            eval_value += grid[r][c-1]["value"] * 2
    if (r + 1) <= 4:
        if (grid[r+1][c]["occupied"] == raid_opponent):
            eval_value += grid[r+1][c]["value"] * 2
    if (c + 1) <= 4:
        if (grid[r][c+1]["occupied"] == raid_opponent):
            eval_value += grid[r][c+1]["value"] * 2
    return eval_value

#perform greedy raid operation
def raid(r,c,raid_player):
    if raid_player == "X":
        raid_opponent = "O"
    else:
        raid_opponent = "X"
    grid[r][c]["occupied"] = raid_player
    if (r - 1) >= 0:
        if (grid[r-1][c]["occupied"] == raid_opponent):
            grid[r-1][c]["occupied"] = raid_player
    if (c - 1) >= 0:
        if (grid[r][c-1]["occupied"] == raid_opponent):
            grid[r][c-1]["occupied"] = raid_player
    if (r + 1) <= 4:
        if (grid[r+1][c]["occupied"] == raid_opponent):
            grid[r+1][c]["occupied"] = raid_player
    if (c + 1) <= 4:
        if (grid[r][c+1]["occupied"] == raid_opponent):
            grid[r][c+1]["occupied"] = raid_player
            
#find next move using greedy algorithm
def greedy_algo(greedy_player):
    if greedy_player == "X":
        greedy_opponent = "O"
    else:
        greedy_opponent = "X"
    eval_player = 0
    eval_opponent = 0
    for r in range(0,5):
        for c in range(0,5):
            if (grid[r][c]["occupied"] == greedy_player):
                eval_player += grid[r][c]["value"]
            elif (grid[r][c]["occupied"] == greedy_opponent):
                eval_opponent += grid[r][c]["value"]
    eval_diff = eval_player - eval_opponent

    max_eval = eval_diff
    for r in range(4,-1,-1):
        for c in range(4,-1,-1):
            if (grid[r][c]["occupied"] == "*"):
                raid_flag = check_raid(r,c,greedy_player)
                if raid_flag == True:
                    new_eval = eval_diff + eval_raid(r,c,greedy_opponent)
                else:
                    new_eval = eval_diff + grid[r][c]["value"]
                if (new_eval >= max_eval):
                    max_eval = new_eval
                    row = r
                    col = c
                    final_raid_flag = raid_flag

    if final_raid_flag == True:
        raid(row,col,greedy_player)
    else:
        grid[row][col]["occupied"] = greedy_player

#write greedy next state to file
def write_greedy():
    for i in range(0,5):
        str2 = ""
        for j in range(0,5):
            str1 = grid[i][j]["occupied"]
            str2 += str1
        output_file.write("".join(str2) + "\n") 

#write greedy next state to trace file
def write_greedy_trace():
    for i in range(0,5):
        str2 = ""
        for j in range(0,5):
            str1 = grid[i][j]["occupied"]
            str2 += str1
        trace_file.write("".join(str2) + "\n") 

#calulate evaluation function for minimax raid operation
def minimax_eval_raid(raid_player):
    eval_player = 0
    eval_opponent = 0
    for r in range(0,5):
        for c in range(0,5):
            if (grid[r][c]["occupied"] == "X"):
                eval_player += grid[r][c]["value"]
            elif (grid[r][c]["occupied"] == "O"):
                eval_opponent += grid[r][c]["value"]
    eval_value = eval_player - eval_opponent
    return eval_value

#perform minimax raid operation
def minimax_raid(r,c,raiding_player):
    if raiding_player == "X":
        raided_player = "O"
    else:
        raided_player = "X"
    grid[r][c]["occupied"] = raiding_player
    raids = []
    if (r - 1) >= 0:
        if (grid[r-1][c]["occupied"] == raided_player):
            grid[r-1][c]["occupied"] = raiding_player
            raided = [r-1,c]
            raids.append(raided)
    if (c - 1) >= 0:
        if (grid[r][c-1]["occupied"] == raided_player):
            grid[r][c-1]["occupied"] = raiding_player
            raided = [r,c-1]
            raids.append(raided)
    if (r + 1) <= 4:
        if (grid[r+1][c]["occupied"] == raided_player):
            grid[r+1][c]["occupied"] = raiding_player
            raided = [r+1,c]
            raids.append(raided)
    if (c + 1) <= 4:
        if (grid[r][c+1]["occupied"] == raided_player):
            grid[r][c+1]["occupied"] = raiding_player
            raided = [r,c+1]
            raids.append(raided)
    return raids

#perform reverse of raid operation            
def minimax_unraid(r,c,move,raiding_player):
    if raiding_player == "X":
        raided_player = "O"
    else:
        raided_player = "X"
    grid[r][c]["occupied"] = "*"
    for i in range(0, len(move["raided"])):
        r_index = move["raided"][i][0]
        c_index = move["raided"][i][1]
        grid[r_index][c_index]["occupied"] = raided_player

#find next move using minimax algorithm
def minimax(row,col,depth,next_player,cutoff_depth):
    if depth == cutoff_depth:
        return minimax_eval_raid(next_player), [row,col]

    if next_player == "X":
        best_score = -100000
        moves = []
        for r in range(0,5):
            for c in range(0,5):
                if (grid[r][c]["occupied"] == "*"):
                    move = {}
                    move["row"] = r
                    move["col"] = c
                    if check_raid(r,c,next_player):
                        move["raided"] = minimax_raid(r,c,next_player)
                        move["raid"] = True
                    else:
                        grid[r][c]["occupied"] = next_player
                        move["raided"] = []
                        move["raid"] = False

                    if best_score == -100000:
                        write_traverse_log(row,col,depth,best_score)
                    move["score"],next_move = minimax(r,c,depth+1,"O",cutoff_depth)
                    write_traverse_log(r,c,depth+1,move["score"])
                    if move["score"] > best_score:
                        best_score = move["score"]
                        best_move = [move["row"], move["col"]]
                    write_traverse_log(row,col,depth,best_score)
                    moves.append(move)
                    if move["raid"] == False:
                        grid[r][c]["occupied"] = "*"
                    else:
                        minimax_unraid(r,c,move,next_player)
                    
    else:
        best_score = 100000
        moves = []
        for r in range(0,5):
            for c in range(0,5):
                if (grid[r][c]["occupied"] == "*"):
                    move = {}
                    move["row"] = r
                    move["col"] = c
                    if check_raid(r,c,next_player):
                        move["raided"] = minimax_raid(r,c,next_player)
                        move["raid"] = True
                    else:
                        grid[r][c]["occupied"] = next_player
                        move["raided"] = []
                        move["raid"] = False

                    if best_score == 100000:
                        write_traverse_log(row,col,depth,best_score)
                    move["score"],next_move = minimax(r,c,depth+1,"X",cutoff_depth)
                    write_traverse_log(r,c,depth+1,move["score"])
                    if move["score"] < best_score:
                        best_score = move["score"]
                        best_move = [move["row"], move["col"]]
                    write_traverse_log(row,col,depth,best_score)
                    moves.append(move)
                    if move["raid"] == False:
                        grid[r][c]["occupied"] = "*"
                    else:
                        minimax_unraid(r,c,move,next_player)
                       
    return best_score,best_move

#find next move using alpha-beta algorithm
def alphabeta(row,col,depth,next_player,alpha,beta,cutoff_depth):
    if depth == cutoff_depth:
        return minimax_eval_raid(next_player), [row,col]

    if next_player == "X":
        moves = []
        for r in range(0,5):
            for c in range(0,5):
                if (grid[r][c]["occupied"] == "*"):
                    move = {}
                    move["row"] = r
                    move["col"] = c
                    if check_raid(r,c,next_player):
                        move["raided"] = minimax_raid(r,c,next_player)
                        move["raid"] = True
                    else:
                        grid[r][c]["occupied"] = next_player
                        move["raided"] = []
                        move["raid"] = False

                    if alpha == -100000:
                        write_ab_traverse_log(row,col,depth,alpha,alpha,beta)

                    move["score"],next_move = alphabeta(r,c,depth+1,"O",alpha,beta,cutoff_depth)
                    write_ab_traverse_log(r,c,depth+1,move["score"],alpha,beta)
                    moves.append(move)
                    if move["raid"] == False:
                        grid[r][c]["occupied"] = "*"
                    else:
                        minimax_unraid(r,c,move,next_player)
                    if move["score"] > alpha:
                        alpha = move["score"]
                        best_move = [move["row"], move["col"]]
                    write_ab_traverse_log(row,col,depth,alpha,alpha,beta)
                    if alpha >= beta:
                        break
        return alpha, best_move
                    
    else:
        moves = []
        for r in range(0,5):
            for c in range(0,5):
                if (grid[r][c]["occupied"] == "*"):
                    move = {}
                    move["row"] = r
                    move["col"] = c
                    if check_raid(r,c,next_player):
                        move["raided"] = minimax_raid(r,c,next_player)
                        move["raid"] = True
                    else:
                        grid[r][c]["occupied"] = next_player
                        move["raided"] = []
                        move["raid"] = False

                    if beta == 100000:
                        write_ab_traverse_log(row,col,depth,beta,alpha,beta)
                        
                    move["score"],next_move = alphabeta(r,c,depth+1,"X",alpha,beta,cutoff_depth)
                    write_ab_traverse_log(r,c,depth+1,move["score"],alpha,beta)
                    moves.append(move)
                    if move["raid"] == False:
                        grid[r][c]["occupied"] = "*"
                    else:
                        minimax_unraid(r,c,move,next_player)
                    if move["score"] < beta:
                        beta = move["score"]
                        best_move = [move["row"], move["col"]]
                    write_ab_traverse_log(row,col,depth,beta,alpha,beta)
                    if alpha >= beta:
                        break
        return beta, best_move

#find next move using minimax algorithm without traverse log
def bs_minimax(row,col,depth,next_player,cutoff_depth):
    if depth == cutoff_depth:
        return minimax_eval_raid(next_player), [row,col]

    if next_player == "X":
        best_score = -100000
        moves = []
        for r in range(0,5):
            for c in range(0,5):
                if (grid[r][c]["occupied"] == "*"):
                    move = {}
                    move["row"] = r
                    move["col"] = c
                    if check_raid(r,c,next_player):
                        move["raided"] = minimax_raid(r,c,next_player)
                        move["raid"] = True
                    else:
                        grid[r][c]["occupied"] = next_player
                        move["raided"] = []
                        move["raid"] = False

                    move["score"],next_move = bs_minimax(r,c,depth+1,"O",cutoff_depth)
                    if move["score"] > best_score:
                        best_score = move["score"]
                        best_move = [move["row"], move["col"]]
                    moves.append(move)
                    if move["raid"] == False:
                        grid[r][c]["occupied"] = "*"
                    else:
                        minimax_unraid(r,c,move,next_player)
                    
    else:
        best_score = 100000
        moves = []
        for r in range(0,5):
            for c in range(0,5):
                if (grid[r][c]["occupied"] == "*"):
                    move = {}
                    move["row"] = r
                    move["col"] = c
                    if check_raid(r,c,next_player):
                        move["raided"] = minimax_raid(r,c,next_player)
                        move["raid"] = True
                    else:
                        grid[r][c]["occupied"] = next_player
                        move["raided"] = []
                        move["raid"] = False

                    move["score"],next_move = bs_minimax(r,c,depth+1,"X",cutoff_depth)
                    if move["score"] < best_score:
                        best_score = move["score"]
                        best_move = [move["row"], move["col"]]
                    moves.append(move)
                    if move["raid"] == False:
                        grid[r][c]["occupied"] = "*"
                    else:
                        minimax_unraid(r,c,move,next_player)
                       
    return best_score,best_move

#find next move using alpha-beta algorithm without traverse log
def bs_alphabeta(row,col,depth,next_player,alpha,beta,cutoff_depth):
    if depth == cutoff_depth:
        return minimax_eval_raid(next_player), [row,col]

    if next_player == "X":
        moves = []
        for r in range(0,5):
            for c in range(0,5):
                if (grid[r][c]["occupied"] == "*"):
                    move = {}
                    move["row"] = r
                    move["col"] = c
                    if check_raid(r,c,next_player):
                        move["raided"] = minimax_raid(r,c,next_player)
                        move["raid"] = True
                    else:
                        grid[r][c]["occupied"] = next_player
                        move["raided"] = []
                        move["raid"] = False

                    move["score"],next_move = bs_alphabeta(r,c,depth+1,"O",alpha,beta,cutoff_depth)
                    moves.append(move)
                    if move["raid"] == False:
                        grid[r][c]["occupied"] = "*"
                    else:
                        minimax_unraid(r,c,move,next_player)
                    if move["score"] > alpha:
                        alpha = move["score"]
                        best_move = [move["row"], move["col"]]
                    if alpha >= beta:
                        break
        return alpha, best_move
                    
    else:
        moves = []
        for r in range(0,5):
            for c in range(0,5):
                if (grid[r][c]["occupied"] == "*"):
                    move = {}
                    move["row"] = r
                    move["col"] = c
                    if check_raid(r,c,next_player):
                        move["raided"] = minimax_raid(r,c,next_player)
                        move["raid"] = True
                    else:
                        grid[r][c]["occupied"] = next_player
                        move["raided"] = []
                        move["raid"] = False
                        
                    move["score"],next_move = bs_alphabeta(r,c,depth+1,"X",alpha,beta,cutoff_depth)
                    moves.append(move)
                    if move["raid"] == False:
                        grid[r][c]["occupied"] = "*"
                    else:
                        minimax_unraid(r,c,move,next_player)
                    if move["score"] < beta:
                        beta = move["score"]
                        best_move = [move["row"], move["col"]]
                    if alpha >= beta:
                        break
        return beta, best_move

#write traverse log 
def write_traverse_log(row,col,depth,score):
    if score == -100000:
        score = "-Infinity"
    elif score == 100000:
        score = "Infinity"
    if depth == 0:
        traverse_file.write(",".join(("root",str(depth),str(score))) + "\n")
    else:
        node = chr(col+65) + str(row+1)
        traverse_file.write(",".join((node,str(depth),str(score))) + "\n")

#write alpha beta traverse log 
def write_ab_traverse_log(row,col,depth,score,alpha,beta):
    if score == -100000:
        score = "-Infinity"
    elif score == 100000:
        score = "Infinity"
    if alpha == -100000:
        alpha = "-Infinity"
    elif alpha == 100000:
        alpha = "Infinity"
    if beta == -100000:
        beta = "-Infinity"
    elif beta == 100000:
        beta = "Infinity"
        
    if depth == 0:
        traverse_file.write(",".join(("root",str(depth),str(score),str(alpha),str(beta))) + "\n")
    else:
        node = chr(col+65) + str(row+1)
        traverse_file.write(",".join((node,str(depth),str(score),str(alpha),str(beta))) + "\n")

#write minimax output to next state file
def write_minimax(r,c,write_player):
    if check_raid(r,c,write_player):
        raids = minimax_raid(r,c,write_player)
    else:
        grid[r][c]["occupied"] = write_player
    for i in range(0,5):
        str2 = ""
        for j in range(0,5):
            str1 = grid[i][j]["occupied"]
            str2 += str1
        output_file.write("".join(str2) + "\n") 

#write minimax output to trace state file
def write_minimax_trace(r,c,write_player):
    if check_raid(r,c,write_player):
        raids = minimax_raid(r,c,write_player)
    else:
        grid[r][c]["occupied"] = write_player
    for i in range(0,5):
        str2 = ""
        for j in range(0,5):
            str1 = grid[i][j]["occupied"]
            str2 += str1
        trace_file.write("".join(str2) + "\n") 

#check if board is full
def check_gameover():
    gameover_flag = True
    for i in range(0,5):
        for j in range(0,5):
            if (grid[i][j]["occupied"] == "*"):
                gameover_flag = False
    if gameover_flag == True:
        return True
    else:
        return False

#perform battle simulation for given input
def battle_simulation():
    while (check_gameover() == False):
        if player1_algo == 1:
            greedy_algo(player1)
            write_greedy_trace()
        elif player1_algo == 2:
            final_score,final_move = bs_minimax("root","root",0,player1,player1_cutoff_depth)
            write_minimax_trace(final_move[0],final_move[1],player1)
        elif player1_algo == 3:
            final_score,final_move = bs_alphabeta("root","root",0,player1,-100000,100000,player2_cutoff_depth)
            write_minimax_trace(final_move[0],final_move[1],player1)
        if (check_gameover() == False):
            if player2_algo == 1:
                greedy_algo(player2)
                write_greedy_trace(player2)
            elif player2_algo == 2:
                final_score,final_move = bs_minimax("root","root",0,player2,player2_cutoff_depth)
                write_minimax_trace(final_move[0],final_move[1],player2)
            elif player2_algo == 3:
                final_score,final_move = bs_alphabeta("root","root",0,player2,-100000,100000,player2_cutoff_depth)
                write_minimax_trace(final_move[0],final_move[1],player2)
    
#create output file to print next move result
output_file = open("next_state.txt", "w")

#execute algorithms for next move based on input
if algo_type == 1:
    if check_gameover():
        print "Sorry board is full -- Gameover!"
    else:
        greedy_algo(player)
        write_greedy()
elif algo_type == 2:
    if check_gameover():
        print "Sorry board is full -- Gameover!"
    else:
        traverse_file = open("traverse_log.txt", "w")
        traverse_file.write("Node,Depth,Value \n")
        final_score,final_move = minimax("root","root",0,player,player_cutoff_depth)
        write_minimax(final_move[0],final_move[1],player)
        traverse_file.close()
elif algo_type == 3:
    if check_gameover():
        print "Sorry board is full -- Gameover!"
    else:
        traverse_file = open("traverse_log.txt", "w")
        traverse_file.write("Node,Depth,Value,Alpha,Beta \n")
        final_score,final_move = alphabeta("root","root",0,player,-100000,100000,player_cutoff_depth)
        write_minimax(final_move[0],final_move[1],player)
        traverse_file.close()
else:
    trace_file = open("trace_state.txt", "w")
    battle_simulation()
    trace_file.close()

#close output file
output_file.close()
