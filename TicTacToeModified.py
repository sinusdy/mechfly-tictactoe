#print field layout
def show_field(field):
    print(field[0] + ' ' + field[1] + ' ' + field[2] + '\n')
    print(field[3] + ' ' + field[4] + ' ' + field[5] + '\n')
    print(field[6] + ' ' + field[7] + ' ' + field[8] + '\n')

#block opponent at specific positions
def check_streak(field, pos1, pos2, pos3, side):
    slot_isfilled = [False,False,False,False,False,False,False,False,False]
    counter = 0

    for i in [pos1, pos2, pos3]:
        if field[i] != ' ':
            slot_isfilled[i] = True
        if field[i] == side:
            counter += 1

    if counter == 2:
        for i in [pos1, pos2, pos3]:
            if slot_isfilled[i] == False:
                return i

#check all field and block
def check_streak_all(field, side):
    move = None

    move = check_streak(field,0,1,2,side) #block row1
    if move != None:
        return move
    move = check_streak(field,3,4,5,side) #block row2
    if move != None:
        return move
    move = check_streak(field,6,7,8,side) #block row3
    if move != None:
        return move
    move = check_streak(field,0,3,6,side) #block col1
    if move != None:
        return move
    move = check_streak(field,1,4,7,side) #block col2
    if move != None:
        return move
    move = check_streak(field,2,5,8,side) #block col3
    if move != None:
        return move
    move = check_streak(field,0,4,8,side) #block dia1
    if move != None:
        return move
    move = check_streak(field,2,4,6,side) #block dia2
    if move != None:
        return move

#suggest next move for player X
def suggest_move(field):
    # check for player winning move
    move = check_streak_all(playfield, 'X')
    if move != None: return move

    # check for opp winning move
    move = check_streak_all(playfield, 'O')
    if move != None: return move

    #check how many boxes are filled
    no_filled = 0
    for i in field:
        if i != ' ':
            no_filled += 1

    #no_filled even -> player starts first
    #no_filled odd -> opponent starts first

    if no_filled == 0: #no one has moved
        return 4

    if no_filled == 1: #opp moved 1x
        if field[4] == 'O': #check centre
            return 0
        else:
            return 4

    if no_filled == 2: #player moved 1x, opp moved 1x
        #check corners
        if field[0] == 'O':
            return 2
        if field[2] == 'O':
            return 0
        if field[6] == 'O':
            return 8
        if field[8] == 'O':
            return 6
        #check edge
        if field[1] == 'O':
            return 2
        if field[3] == 'O':
            return 0
        if field[5] == 'O':
            return 2
        if field[7] == 'O':
            return 6

    if no_filled == 3: #opp moved 2x, player moved 1x
        #check diagonal
        if (field[0] == 'O' and field[8] == 'O') or (field[2] == 'O' and field[6] == 'O'):
            return 1

        #if center is X
        if field[4] == 'X':
            #check corners for O
            if field[0] == 'O':
                return 8
            if field[2] == 'O':
                return 6
            if field[6] == 'O':
                return 2
            if field[8] == 'O':
                return 0

            #check 'L' shape
            if field[1] == 'O' and field[5] == 'O':
                return 2
            if field[1] == 'O' and field[3] == 'O':
                return 0
            if field[3] == 'O' and field[7] == 'O':
                return 6
            if field[5] == 'O' and field[7] == 'O':
                return 8

    if no_filled == 4: #player moved 2x, opp moved 2x
        #if opponent 1st move is on the edge
        if field[0] == 'O':
            if field[1] == ' ': return 1
            else: return 3
        if field[2] == 'O':
            if field[1] == ' ': return 1
            else: return 5
        if field[6] == 'O':
            if field[7] == ' ': return 7
            else: return 3
        if field[8] == 'O':
            if field[7] == ' ': return 7
            else: return 5

    else:
        #occupy corner
        for i in [0,2,6,8]:
            if field[i] == ' ':
                return i

        #occupy edge
        for i in [1,3,5,7]:
            if field[i] == ' ':
                return i

####################################################
#X = AI
#O = player

#map          0   1   2   3   4   5   6   7   8
playfield = [' ',' ',' ',' ',' ',' ',' ',' ',' ']

#first_move = input("player first (O) or AI first (X)?\n")
#if first_move == 'O':
    #player_move = input("your move?\n")
    #playfield[int(player_move)] = 'O'
    #show_field(playfield)

#while True:
    #check for empty slot
    #empty_slot = 0
    #for i in range(9):
        #if playfield[i] == ' ':
            #empty_slot +=1
    #if empty_slot == 0:
        #break

    #AI move
    #print('AI move:\n')
    #playfield[suggest_move(playfield)] = 'X'
    #show_field(playfield)

    #player move
    #player_move = input("your move?\n")
    #playfield[int(player_move)] = 'O'
    #show_field(playfield)