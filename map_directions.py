##### enemy movement based on which map #####
##### number values are amount of tiles #####
map_directions = [] # create a list for directions
map_distances = [] # create a list for distances
map_start = [] # create a list for enemy spawn locations
''' working directions:
    u,d,l,r
    needs ul,ur,dl,dr
'''

m1_dir = ['d','l','d','r','u','l','d','l','u','r','d'] # list of directions map 0 directions
m1_dis = [ 2,  5,  9,  6,  5,  2,  3,  2,  5,  7,  9] # list of distances map 0 distances
m1_sta = [7,0] # starting location for enemies

m2_dir = ['r','u','l','d','r','u','l','d','r','u']
m2_dis = [11,  3,  3,  9,  3,  3,  9,  3,  3,  11]
m2_sta = [0, 5]

m3_dir = ['r','u','l','u','r','d']
m3_dis = [ 7,  3,  4,  3,  7,  10]
m3_sta = [0,9]

m4_dir = ['r','u','r','d','l','u','l']
m4_dis = [ 4,  2,  6,  7,  6,  2,  4]
m4_sta = [0,5]

m5_dir = ['d','l','u','r']
m5_dis = [11 , 3  ,3  ,11]
m5_sta = [5, 0]

m6_dir = ['r','d']
m6_dis = [ 10, 10]
m6_sta = [0, 3]

map_directions.extend([m1_dir] + [m2_dir] + [m3_dir] + [m4_dir] + [m5_dir] + [m6_dir]) # puts the directions into the directions list
map_distances.extend([m1_dis] + [m2_dis] + [m3_dis] + [m4_dis] + [m5_dis] + [m6_dis]) # puts the distances into the distances list
map_start.extend([m1_sta] + [m2_sta] + [m3_sta] + [m4_sta] + [m5_sta] + [m6_sta]) # puts the enemy spawn locations into the start list

