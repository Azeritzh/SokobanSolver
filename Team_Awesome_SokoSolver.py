'''
#  = Wall
.   = Goal
$  = Box
@ = Player4
'''

sokolevel = """"\
#######
#     #
#  .$ #
#.$  @#
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

def find_player_moves((pi,pj),(bi,bj),level):
    player_pos = (pi,pj)
    box_pos = (bi,bj)

    if box_pos == player_pos:
        return None
    if level[box_pos[0]][box_pos[1]] == '#':
        return None
    if level[player_pos[0]][player_pos[1]] == '#':
        return None   
    
    moves = []

    if level[pi][pj+1] == ' ':         #steps right
        moves.append((pi,pj+1))

    if level[pi][pj-1] == ' ':          #steps left
        moves.append((pi,pj-1))

    if level[pi-1][pj] == ' ':          #steps up
        moves.append((pi-1,pj))

    if level[pi+1][pj] == ' ':          #steps down
        moves.append((pi+1,pj))

    return moves

def find_box_pushes((bi,bj),level):
    box_pos = (bi,bj)
    legal_moves = {}

    if level[box_pos[0]][box_pos[1]] == '#':
        return None
    
    if level[bi][bj+1] == ' ':          #steps right
        if level[bi][bj-1] == ' ':      #can it go left as well?
            legal_moves[(bi,bj+1),box_pos] = (bi,bj+1)

    if level[bi][pj-1] == ' ':          #steps left
        if level[bi][bj+1] == ' ':      #can it go right as well?
            legal_moves[(bi,bj-1),box_pos] = (bi,bj-1)

    if level[bi-1][bj] == ' ':          #steps up
        if level[bi+1][bj] == ' ':      #can it go down as well?
            legal_moves[(bi+1,bj),box_pos] = (bi+1,bj)

    if level[bi+1][bj] == ' ':          #steps down
        if level[bi-1][bj] == ' ':      #can it go up as well?
            legal_moves[(bi-1,bj),box_pos] = (bi-1,bj)

    print legal_moves
    return legal_moves

level_lines = sokolevel.splitlines()


#create copy to work on
s_level_lines = []
for line in level_lines:
    s_level_lines.append(line)


pgoal = find_location_of('.', level_lines)
pbox = find_location_of('$', level_lines)

pplayer = find_location_of('@', level_lines)

level = s_level_lines
print level


#graph is a dictionary mapping states to a set of states. State format is
#((bi,bj),(pi,pj)) = ((boxpos),(playerpos))
graph = {}

#all player moves for all box positions
for bi in range(len(level)):
    for bj in range(len(level[1])):
        for pi in range(len(level)):
            for pj in range(len(level[1])):
                moves = find_player_moves((pi,pj),(bi,bj),level)
                if moves != None:
                    graph[((bi,bj),(pi,pj))] = set(moves)
                    
print graph

#update graph with all legal box pushes
for bi in range(len(level)):
    for bj in range(len(level[1])):
        pushes = find_box_pushes((bi,bj),level)
        if pushes != None:
            for state in pushes.keys():
                graph[state].update(pushes[state])
