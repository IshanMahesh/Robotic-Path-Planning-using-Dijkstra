import heapq as hq
from matplotlib.patches import Polygon

x_max = 1200
y_max = 500 

hexagon1 = [600, 100]
hexagon2 = [729, 175]
hexagon3 = [729, 325]
hexagon4 = [600, 400]
hexagon5 = [470, 325]
hexagon6 = [470, 175]

hexagon1_clearance = [600, 95]
hexagon2_clearance = [735, 170]
hexagon3_clearance = [735, 330]
hexagon4_clearance = [600, 405]
hexagon5_clearance = [465, 330]
hexagon6_clearance = [465, 170]

rectangle_1_1 = [100, 100]
rectangle_1_2 = [175, 100]
rectangle_1_3 = [175, 500]
rectangle_1_4 = [100, 500]

rectangle_1_1_clearance = [95,95]
rectangle_1_2_clearance = [180,95]
rectangle_1_3_clearance = [180, 500]
rectangle_1_4_clearance = [95, 500]

rectangle_2_1 = [275, 0]
rectangle_2_2 = [350, 0]
rectangle_2_3 = [350, 400]
rectangle_2_4 = [275, 400]

rectangle_2_1_clearance = [270,0]
rectangle_2_2_clearance = [355,0]
rectangle_2_3_clearance = [355, 405]
rectangle_2_4_clearance = [270, 405]

ushape1 = [900,50]
ushape2 = [1100, 50]
ushape3 = [1100, 450]
ushape4 = [900, 450]
ushape5 = [900, 375]
ushape6 = [1020, 375]
ushape7 = [1020, 125]
ushape8 = [900, 125]

ushape1_clearance = [895, 45]
ushape2_clearance = [1105, 45]
ushape3_clearance = [1105, 455]
ushape4_clearance = [895, 455]
ushape5_clearance = [895, 380]
ushape6_clearance = [1015, 370]
ushape7_clearance = [1015, 130]
ushape8_clearance = [895, 130]

def get_line_equation(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    slope =(y2 - y1)/(x2 - x1)
    intercept = y1-(slope*x1)
    return [slope, intercept]

def inside_rectangle1(point):
    x, y = point
    bl = [95,95]
    ur = [180, 500]
    if((x>=bl[0] and x<=ur[0]) and (y>=bl[1] and y<=ur[1])):
        return True
    return False

def inside_rectangle(point):
    x, y = point
    bl = [270,0]
    ur = [355, 405]
    if((x>=bl[0] and x<=ur[0]) and (y>=bl[1] and y<=ur[1])):
        return True
    return False

def inside_hexagon(point):
    x, y = point
    equation1 = get_line_equation(hexagon1_clearance, hexagon2_clearance)
    l1_flag = y - equation1[0]*x - equation1[1]>=0
    l2_flag = x<=hexagon2_clearance[0]
    equation3 = get_line_equation(hexagon3_clearance, hexagon4_clearance)
    l3_flag = y - equation3[0]*x - equation3[1]<=0
    equation4 = get_line_equation(hexagon4_clearance, hexagon5_clearance)
    l4_flag = y - equation4[0]*x - equation4[1]<=0
    l5_flag = x>=hexagon5_clearance[0]
    equation6 = get_line_equation(hexagon6_clearance, hexagon1_clearance)
    l6_flag = y - equation6[0]*x - equation6[1]>=0

    flag = l1_flag and l2_flag and l3_flag and l4_flag and l5_flag and l6_flag
    return flag

def inside_ushape(point):
    x, y = point
    bl = [895, 45] 
    ur = [1105, 455]  
    cutout_bl = [895, 130]  # Bottom-left corner of the cut-out rectangle
    cutout_ur = [1015, 370]  # Upper-right corner of the cut-out rectangle
    if (x >= bl[0] and x <= ur[0]) and (y >= bl[1] and y <= ur[1]):
        if not ((x >= cutout_bl[0] and x <= cutout_ur[0]) and (y >= cutout_bl[1] and y <= cutout_ur[1])):
            return True
    return False

def check_obstacle(current_node):
    x, y = current_node
    if (x > x_max) or (y > y_max) or (x < 0) or (y < 0):
        return False
    if(inside_hexagon(current_node) or inside_rectangle1(current_node) or inside_rectangle(current_node) or inside_ushape(current_node)):
        return False
    return True

def get_shapes():
    hexagon_clearance = Polygon([hexagon1_clearance, hexagon2_clearance, hexagon3_clearance, hexagon4_clearance, hexagon5_clearance, hexagon6_clearance], facecolor = 'r')
    hexagon = Polygon([hexagon1, hexagon2, hexagon3, hexagon4, hexagon5, hexagon6], facecolor = 'b')
    rectangle_1_clearance = Polygon([rectangle_1_1_clearance, rectangle_1_2_clearance, rectangle_1_3_clearance, rectangle_1_4_clearance], facecolor = 'r')
    rectangle_1 = Polygon([rectangle_1_1, rectangle_1_2, rectangle_1_3, rectangle_1_4], facecolor = 'b')
    rectangle_2_clearance = Polygon([rectangle_2_1_clearance, rectangle_2_2_clearance, rectangle_2_3_clearance, rectangle_2_4_clearance], facecolor = 'r')
    rectangle_2 = Polygon([rectangle_2_1, rectangle_2_2, rectangle_2_3, rectangle_2_4], facecolor = 'b')
    ushape_clearance = Polygon([ushape1_clearance, ushape2_clearance, ushape3_clearance, ushape4_clearance, ushape5_clearance, ushape6_clearance, ushape7_clearance, ushape8_clearance], facecolor = 'r')
    ushape = Polygon([ushape1, ushape2, ushape3, ushape4, ushape5, ushape6, ushape7, ushape8], facecolor = 'b')
    return (hexagon_clearance, hexagon, rectangle_1_clearance, rectangle_1, rectangle_2_clearance, rectangle_2, ushape_clearance, ushape)

def look_for_neighbors(current_node):
    neighbors = []
    x, y = current_node
    actions = [[1,0], [-1,0], [0,1], [0,-1], [1,1], [-1,1], [1,-1], [-1,-1]]
    for action in actions:
        if check_obstacle((x+action[0], y+action[1])):
            if action[0]!=0 and action[1]!=0:
                neighbors.append([(x+action[0], y+action[1]), 1.4])
            else:
                neighbors.append([(x+action[0], y+action[1]), 1])
    return neighbors

def dijkstra(source, destination):
    OpenList={}
    ClosedList={}

    OpenList[source] = 0
    visited=[]

    queue = []

    hq.heappush(queue, (OpenList[source], source))
    hq.heapify(queue)

    path = []
    while queue:
        current_node = hq.heappop(queue)[1]
        print("Current node : ", current_node)
        if current_node == destination:
            print("Found!!")
            temp = destination
            while(ClosedList[temp]!=source):
                path.append(ClosedList[temp])
                temp = ClosedList[temp]
            break
        if current_node not in visited:
            if(check_obstacle(current_node)):
                visited.append(current_node)
            neighbors = look_for_neighbors(current_node)
            for neighbor, cost in neighbors:
                node_cost = OpenList[current_node] + cost
                if (not OpenList.get(neighbor)):
                    OpenList[neighbor] = node_cost
                    ClosedList[neighbor] = current_node
                else:
                    if(node_cost<OpenList[current_node]):
                        OpenList[neighbor] = node_cost
                        ClosedList[neighbor] = current_node
                hq.heappush(queue, (OpenList[neighbor], neighbor))
                hq.heapify(queue)
    return path, visited