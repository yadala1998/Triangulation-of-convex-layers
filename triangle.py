import matplotlib.pyplot as plt
import numpy as np
import math
import sys    

class Vertex(object):
    
    def __init__(self,x,y):
        self.xValue = x
        self.yValue = y
        self.faces = []
        self.edges = []

    def getVertexInfo(self):
        return self.xValue, self.yValue
    
    def addFaceToVertex(self, face_object):
        self.faces.append(face_object)
    
    def addEdgeToVertex(self, edge_object):
        self.edges.append(edge_object)
     
    def getFaces(self):
	    return self.faces

    def getEdges(self):
	    return self.edges  
	

class Edge(object):
    
    def __init__(self, vertex_1, vertex_2): #vertex objects not points
        self.vertex_one = vertex_1
        self.vertex_two = vertex_2
        self.faces = []
    
    def getBothVertices(self):
        return self.vertex_one.getVertexInfo(), self.vertex_two.getVertexInfo() 
    
    def addFaceToEdge(self, face_object):
        self.faces.append(face_object)

    def getFaces(self):
	    return self.faces[0], self.faces[1]

class Face(object):
    
    def __init__(self, vertex_1, vertex_2, vertex_3):
        self.vertex_one = vertex_1  #vertex objects
        self.vertex_two = vertex_2
        self.vertex_three = vertex_3
    
    def getFaceInfo(self):
        return self.vertex_one.getVertexInfo(), self.vertex_two.getVertexInfo(), 		   			self.vertex_three.getVertexInfo()


#Global Variables
point_file = open(sys.argv[1], "r")
all_points = []
all_points_x = []
all_points_y = []
All_Vertices = []
All_edges = []
All_faces = []

#Main Method
def main():
    global all_points
    global all_points_x
    global all_points_y
    for curr_point in point_file:
        row = curr_point.split()
        all_points_x.append(float(row[0]))
        all_points_y.append(float(row[1]))
        all_points.append((float(row[0]), float(row[1])))
    plt.scatter(all_points_x, all_points_y)
    #Generation of convex layers
    convex_layers = make_convex_layers(all_points)
    #Adding all Triangle faces 
    triangles = []
    for i in range(0, len(Triangulate(convex_layers)) -1):
        triangles.append(tuple(Triangulate(convex_layers)[i]))
    triangles_2 = set(tuple(triangles)) #removing duplicate triangles
    del triangles[:]
    for i in range(0, len(triangles_2)): #Making it a list again
        triangles.append(triangles_2.pop())
    #plotting    
    for i in range(0, len(triangles) -1):
        coordinates = triangles[i][0], triangles[i][1], triangles[i][2], triangles[i][0]
        x,y = zip(*coordinates)
        plt.plot(x,y)
        
    #Adding everything to the data structure
    for i in range(0, len(triangles)):
           
            V1 = Vertex(triangles[i][0][0], triangles[i][0][1])
            V2 = Vertex(triangles[i][1][0], triangles[i][1][1])
            V3 = Vertex(triangles[i][2][0], triangles[i][2][1])
            E1 = Edge(V1,V2)
            E2 = Edge(V2,V3)
            E3 = Edge(V3,V1)
            
            #duplicate return values
            V1_dup = duplicateVertexExists(V1)
            V2_dup = duplicateVertexExists(V2)
            V3_dup = duplicateVertexExists(V3)
            E1_dup = duplicateEdgeExists(E1)
            E2_dup = duplicateEdgeExists(E2)
            E3_dup = duplicateEdgeExists(E3)
            
            #Adding Faces
            All_faces.append(Face(V1,V2,V3))
                
            #checking and adding
            if V1_dup[0] == False:
                All_Vertices.append(V1)
                V1.addFaceToVertex(All_faces[i])
                V1.addEdgeToVertex(E1)
                V1.addEdgeToVertex(E3)
            else: 
                All_Vertices[V1_dup[1]].addFaceToVertex(All_faces[i])
                All_Vertices[V1_dup[1]].addEdgeToVertex(E1)
                All_Vertices[V1_dup[1]].addEdgeToVertex(E3)
                
            if V2_dup[0] == False:
                All_Vertices.append(V2)
                V2.addFaceToVertex(All_faces[i])
                V2.addEdgeToVertex(E1)
                V2.addEdgeToVertex(E2)
            else:
                All_Vertices[V2_dup[1]].addFaceToVertex(All_faces[i])
                All_Vertices[V2_dup[1]].addEdgeToVertex(E1)
                All_Vertices[V2_dup[1]].addEdgeToVertex(E2)
                
            if V3_dup[0] == False:
                All_Vertices.append(V3)
                V3.addFaceToVertex(All_faces[i])
                V3.addEdgeToVertex(E2)
                V3.addEdgeToVertex(E3)
            else:
                All_Vertices[V3_dup[1]].addFaceToVertex(All_faces[i])
                All_Vertices[V3_dup[1]].addEdgeToVertex(E2)
                All_Vertices[V3_dup[1]].addEdgeToVertex(E3)
                
            if E1_dup[0] == False:
                All_edges.append(E1)
                E1.addFaceToEdge(All_faces[i])
            else:
                All_edges[E1_dup[1]].addFaceToEdge(All_faces[i])
            if E2_dup[0] == False:
                All_edges.append(E2)
                E2.addFaceToEdge(All_faces[i])
            else:
                All_edges[E2_dup[1]].addFaceToEdge(All_faces[i])
            if E3_dup[0] == False:
                All_edges.append(E3)
                E2.addFaceToEdge(All_faces[i])
            else:
                All_edges[E3_dup[1]].addFaceToEdge(All_faces[i])

    print("Total Number of Vertices: " + str(len(All_Vertices)))
    print("Total Number of Edges: " + str(len(All_edges)))
    print("Total Number of Faces/Triangles: " + str(len(All_faces)))
    plt.axis('equal')
    plt.show()

#Helper Method for Checking duplicate Vertices
def duplicateVertexExists(Vertex_object):
    global All_Vertices
    for i in range(0, len(All_Vertices)):
        if Vertex_object.getVertexInfo() == All_Vertices[i].getVertexInfo():
            return True, i
    return False, 0

#Helper Method for Checking duplicate Edges    
def duplicateEdgeExists(Edge_object):
    global All_edges
    for i in range(0, len(All_edges)):
        if (Edge_object.getBothVertices()[0] == All_edges[i].getBothVertices()[0] or Edge_object.getBothVertices()[0] == All_edges[i].getBothVertices()[1]) \
                and (Edge_object.getBothVertices()[1] == All_edges[i].getBothVertices()[0] or Edge_object.getBothVertices()[1] == All_edges[i].getBothVertices()[1]): 
            return True, i
    return False, 0   

#Checking the direction of area
def Area(a, b, c, d):
    return a*d - b*c

#Triangulation Algorithm/Method
def Triangulate(layers):
    i =0
    triangles = []
    for i in range(0, len(layers)-1):
        A = layers[i]
        B = layers[i+1]
        if len(B) != 1:
            k = 0
            m = 0 #Changed
            while k <= len(A) and m <= len(B): #Added a wrap around
                area = Area(B[(m+1)%len(B)][0] - B[m%len(B)][0], B[(m+1)%len(B)][1] - B[m%len(B)][1], A[(k+1)%len(A)][0] - A[k%len(A)][0], A[(k+1)%len(A)][1] - A[k%len(A)][1])
                if area > 0:
                    triangles.append([A[k%len(A)], B[m%len(B)], A[(k+1)%len(A)]])
                    k = k+1
                elif area < 0:
                    triangles.append([B[m%len(B)], B[(m+1)%len(B)], A[k%len(A)]])
                    m = m + 1
                else:
                    triangles.append([B[m%len(B)], B[(m+1)%len(B)], A[k%len(A)]])
                    triangles.append([A[k%len(A)], B[(m+1)%len(B)], A[(k+1)%len(A)]])
                    k = k + 1
                    m = m + 1
        else: #1-point at the center
            k = 0
            while k <= len(A):
                triangles.append([A[k%len(A)], B[0], A[(k+1)%len(A)]])
                k = k + 1
        i = i + 1        
    return triangles

#Convex Layers Method
def make_convex_layers(points):
    convex_hulls = []
    sets_inner_pts = []
    iteration = 0
    inside_pts = points
    while len(inside_pts) > 1:
        sets_inner_pts.append(inside_pts)
        convex_hull_formed = convex_hull(inside_pts)
        convex_hulls.append(convex_hull_formed)
        for pt in convex_hull_formed:
            inside_pts.remove(pt)
        last_point = len(convex_hulls[iteration]) - 1
        CH_x_coordinates = [convex_hulls[iteration][last_point][0]] # x values of CH points
        CH_y_coordinates = [convex_hulls[iteration][last_point][1]] # y values of CH points
        for i in range(0, last_point + 1):
            CH_x_coordinates.append(convex_hulls[iteration][i][0])
            CH_y_coordinates.append(convex_hulls[iteration][i][1])
            plt.plot(CH_x_coordinates, CH_y_coordinates)
        iteration = iteration + 1
    if len(inside_pts) == 1:
        convex_hulls.append(inside_pts)
    return convex_hulls        

#Cross Product
def cross(pt_left, pt_center, pt_right):
    return (pt_left[0] - pt_center[0]) * (pt_right[1] - pt_center[1])\
           - (pt_left[1] - pt_center[1]) * (pt_right[0] - pt_center[0])

#CH Algorithm
def convex_hull(points):
    points = sorted(set(points))
    if len(points) <= 1:
        return points
    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the beginning of the other list.
    return lower[:-1] + upper[:-1]

if __name__ == '__main__':
    main() 





