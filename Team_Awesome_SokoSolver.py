#This is a sokoban solver made by Christina S. V. Silverwing & Rasmus Elving delivered 09-10-2015

'''
#  = Wall
.   = Goal
$  = Box
@ = Player4
'''

#Definition of Sokoban level
sokolevel = """\
#######
#     #
#     #
#. #  #
#. $$ #
#.$$  #
#.   @#
#######"""

#function for finding the location of the player, goals and boxes
def find_location_of(thing, level_lines):
    result = []
    for i in range(len(level_lines)):
        for j in range(len(level_lines[1])):
            if level_lines[i][j] == thing:
                print"found %s" % thing, "in (%i,%i)" % (i,j)
                s_level_lines[i]=s_level_lines[i].replace(thing,' ')
                result.append((i,j))
    return result

#function for replacing not used boxes with walls, so the player don't ignore them when moving current box around
#TODO implement into search
def replace_box_with_wall(pbox, current_box, level_lines):
    for x in pbox:                                                                              #For each box present in the map
        for i in range(len(level_lines)):                                                       #For each line in the map
            for j in range(len(level_lines[1])):                                                #For each char in current line of the map
                if (i == x[0]) and (j == x[1]) and (x != current_box):                          #Check if current position match coordinets of box
                    text = s_level_lines[i]                                                     #Strings are immutable, make s_level_lines[i] a list
                    text=text[:(x[1])] + '#' + text[(1+x[1]):]                                  #Replace character(at the position of a box) in the list, with a wall
                    s_level_lines[i] = text                                                     #Re-asign the map line to s_level_lines[i]
                    print("Box replaced with wall at (%s,%s)" % (str(x[0]), str(x[1])))
    return s_level_lines

#Function for finding where the player can move around in the level
def find_player_moves((bi,bj),(pi,pj),level):
    player_pos = (pi,pj)
    box_pos = (bi,bj)

    #These returns None if the players position is the same as a box or a wall
    if box_pos == player_pos:
        return None
    if level[box_pos[0]][box_pos[1]] == '#':
        return None
    if level[player_pos[0]][player_pos[1]] == '#':
        return None   

    #Makes a list "moves" to save player moves and return them
    moves = []

    #if statements for checking if the player have space to move and no box is on the position
    if (level[pi][pj+1] == ' ') and not((pi == bi) and (pj+1 == bj)):         #steps right
        moves.append((box_pos,(pi,pj+1)))

    if (level[pi][pj-1] == ' ') and not((pi == bi) and (pj-1 == bj)):          #steps left
        moves.append((box_pos,(pi,pj-1)))

    if (level[pi-1][pj] == ' ') and not((pi-1 == bi) and (pj == bj)):          #steps up
        moves.append((box_pos,(pi-1,pj))) 

    if (level[pi+1][pj] == ' ') and not((pi+1 == bi) and (pj == bj)):          #steps down
        moves.append((box_pos,(pi+1,pj)))

    #returns only list if it is not empty, else return nothing
    if moves != []:
        return moves

#Function for finding valid box moves
def find_box_pushes((bi,bj),level):
    box_pos = (bi,bj)
    legal_moves = {}

    #Checks if box position is the same as a wall, and returns none if true
    if level[box_pos[0]][box_pos[1]] == '#':
        return None

    #Checks if position to the right of the box is empty if true checks the left position as well
    #if both is true then it is a valid move (player on one site, box move to the other)
    if level[bi][bj+1] == ' ':          #Check if there is space to the right
        if level[bi][bj-1] == ' ':      #Check if there is also space to the left
            legal_moves[box_pos,(bi,bj-1)] = ((bi,bj+1),box_pos)
            legal_moves[box_pos,(bi,bj+1)] = ((bi,bj-1),box_pos)

    #Does the same as above for up and down positions
    if level[bi-1][bj] == ' ':          #Check if there is space above
        if level[bi+1][bj] == ' ':      #Check if there is also space below
            legal_moves[box_pos,(bi-1,bj)] = ((bi+1,bj),box_pos)
            legal_moves[box_pos,(bi+1,bj)] = ((bi-1,bj),box_pos)

    #Checks if list is not empty and returns it, else returns nothing
    if legal_moves != []:
        return legal_moves

#Function for Breath first search
def bfs_paths(graph, start, goal):
    stack = [(start, [start])]
    next = ''
    while stack:
        (vertex, path) = stack.pop(0)
        for next in graph[vertex] - set(path):
            if next == goal:
                return path + [next]
            else:
                stack.append((next, path + [next]))

#Assign the map to level_lines, split in to lines
level_lines = sokolevel.splitlines()

#create copy to work on
s_level_lines = []

for line in level_lines:
    s_level_lines.append(line)


#Locating and removing Goals, Boxes and the player
pgoal = find_location_of('.', level_lines)
pbox = find_location_of('$', level_lines)
pplayer = find_location_of('@', level_lines)

level = s_level_lines

#walled_maps =[]

#TODO implement (Currently broken)
'''for coords in range(len(pbox)):
    walled_maps.append(replace_box_with_wall(pbox,pbox[coords],level_lines))'''


#graph is a dictionary mapping states to a set of states. State format is
#((bi,bj),(pi,pj)) = ((boxpos),(playerpos))
graph = {}

#all player moves for all box positions
for bi in range(len(level)):
    for bj in range(len(level[1])):
        for pi in range(len(level)):
            for pj in range(len(level[1])):
                moves = find_player_moves((bi,bj),(pi,pj),level)
                if moves != None:
                    graph[((bi,bj),(pi,pj))] = set(moves)

###update graph with all legal box pushes
for bi in range(len(level)):
    for bj in range(len(level[1])):
        pushes = find_box_pushes((bi,bj),level)
        if pushes != None:
            for state in pushes.keys():
                graph[state].update([pushes[state]])


#Executes breath-first search
complete_path =[]

for i in range(len(pgoal)):
    path = bfs_paths(graph, (pbox[i],pplayer[0]), (pgoal[i],pplayer[0]))
    complete_path.append(path)

for x in range(len(complete_path)):
    print ("Path for one box to one goal and back to player start pos: " + str(complete_path[x]))