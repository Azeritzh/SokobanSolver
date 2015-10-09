'''
#  = Wall
.   = Goal
$  = Box
@ = Player4
'''

sokolevel = """\
#######
#     #
#     #
#. #  #
#. $$ #
#.$$  #
#.   @#
#######"""

def find_location_of(thing, level_lines):
    result = []
    for i in range(len(level_lines)):
        for j in range(len(level_lines[1])):
            if level_lines[i][j] == thing:
                print"found %s" % thing, "in (%i,%i)" % (i,j)
                s_level_lines[i]=s_level_lines[i].replace(thing,' ')
                result.append((i,j))
    return result

def replace_box_with_wall(pbox, current_box, level_lines):

    for x in pbox:
        for i in range(len(level_lines)):
            for j in range(len(level_lines[1])):
                if (i == x[0]) and (j == x[1]) and (x != current_box):
                    text = s_level_lines[i]
                    text=text[:(x[1])] + '#' + text[(1+x[1]):]
                    s_level_lines[i] = text
                    print("Box replaced with wall at (%s,%s)" % (str(x[0]), str(x[1])))

def find_player_moves((bi,bj),(pi,pj),level):
    player_pos = (pi,pj)
    box_pos = (bi,bj)

    if box_pos == player_pos:
        return None
    if level[box_pos[0]][box_pos[1]] == '#':
        return None
    if level[player_pos[0]][player_pos[1]] == '#':
        return None   
    
    moves = []

    if (level[pi][pj+1] == ' ') and not((pi == bi) and (pj+1 == bj)):         #steps right
        moves.append((box_pos,(pi,pj+1)))

    if (level[pi][pj-1] == ' ') and not((pi == bi) and (pj-1 == bj)):           #steps left
        moves.append((box_pos,(pi,pj-1)))

    if (level[pi-1][pj] == ' ') and not((pi-1 == bi) and (pj == bj)):          #steps up
        moves.append((box_pos,(pi-1,pj))) 

    if (level[pi+1][pj] == ' ') and not((pi+1 == bi) and (pj == bj)):           #steps down
        moves.append((box_pos,(pi+1,pj)))

    if moves != []:
        #print moves
        return moves

def find_box_pushes((bi,bj),level):
    box_pos = (bi,bj)
    legal_moves = {}

    if level[box_pos[0]][box_pos[1]] == '#':
        return None
    
    if level[bi][bj+1] == ' ':          #is there space to the right?
        if level[bi][bj-1] == ' ':      #is there also space to the left?
            legal_moves[box_pos,(bi,bj-1)] = ((bi,bj+1),box_pos)
            legal_moves[box_pos,(bi,bj+1)] = ((bi,bj-1),box_pos)

    if level[bi-1][bj] == ' ':          #is there space above?
        if level[bi+1][bj] == ' ':      #is there also space below?
            legal_moves[box_pos,(bi-1,bj)] = ((bi+1,bj),box_pos)
            legal_moves[box_pos,(bi+1,bj)] = ((bi-1,bj),box_pos)

    if legal_moves != []:
        #print legal_moves
        return legal_moves

def bfs_paths(graph, start, goal):
    stack = [(start, [start])]
    next = ''
    while stack:
        #print('NewStack: ',stack)
        (vertex, path) = stack.pop(0)
        #print('Stack: ',stack, '## Vertex: ',vertex, '## Path: ',path, '## Next: ',next);print('\n')
        for next in graph[vertex] - set(path):
            if next == goal:
                return path + [next]
                print next
            else:
                stack.append((next, path + [next]))
                print next

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
one_path_at_a_time = []

for coords in range(len(pbox)):
    print()


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
                    
#print graph

###update graph with all legal box pushes
for bi in range(len(level)):
    for bj in range(len(level[1])):
        pushes = find_box_pushes((bi,bj),level)
        if pushes != None:
            for state in pushes.keys():
                #print pushes[state]
                graph[state].update([pushes[state]])
                #print graph[state]

#print pplayer
#print pgoal
#print pbox

#print level
#replace_box_with_wall(pbox,(4,4),level_lines)
#print level

#print graph

#Executes depth-first search

complete_path =[]

for i in range(len(pgoal)):

    path = bfs_paths(graph, (pbox[i],pplayer[0]), (pgoal[i],pplayer[0]))
    complete_path.append(path)
    #print path

for x in range(len(complete_path)):
    print ("Path: " + str(complete_path[x]))

    #path = bfs_paths(graph, (pbox[1],pplayer[0]), (pgoal[i],pplayer[0]))
    #print ("Path: " + str(path))