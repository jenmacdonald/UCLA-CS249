#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 14:08:11 2017

@author: jennifer
"""  

def convertToMatrix(input_edges):
    "This takes in an array of edges and converts it into a CAM adjacency" 
    "matrix"

    # Save the input edges to the variable edges  
    edges = input_edges
        
    # Use a loop to change each list inside the list to lowercase to ignore 
    # case sensitivity, and change each integer to string
    for i in range(len(edges)):
        for j in range(len(edges[i])):
            if isinstance(edges[i][j],int):
                edges[i][j] = str(edges[i][j])
            edges[i][j] = edges[i][j].lower()
    
    # Create a list for all the verticies found in the edge list, making sure
    # to add each vertex only once
    vertices = []
    for i in range(len(edges)):
        if edges[i][0] not in vertices:
            vertices.append(edges[i][0])
        if edges[i][1] not in vertices:
            vertices.append(edges[i][1])
    
    # Sort the vertices. The first one will be used to start our CAM
    vertices = sorted(vertices)
    
    # Create the CAM, which is a list of lists. Starting off, the only list in 
    # CAM contains the single, smallest vertex
    cam = [list(vertices[0])]
    
    # Create a vertex list to keep track of the vertices that have already been
    # or are currently being examined. Add the vertex that has already been
    # added to CAM
    vertex_list = []
    vertex_list.append(vertices[0][-1])
    
    # Use a loop that will add the appropriate next line containing a node and
    # all its corresponding edges
    for i in range(len(edges) - 1):
        
        # Create a list of 3-item lists of candidates to be examined, each
        # containing a unique edge and its corresponding two nodes. If a node
        # in CAM is in the edge list were examining, we add it to the candidate
        # list
        candidate_list = []
        for i in range(len(edges)):
            for j in range(len(cam)):
                if cam[j][-1] in edges[i]:
                    candidate_list.append(edges[i])
                    if candidate_list:
                        break
        
        # Create a list of edge candidates, and add all the edges from
        # "list candidates", then sort them
        candidate_edges = []
        for i in range(len(candidate_list)):
            candidate_edges.append(candidate_list[i][-1])    
        candidate_edges = sorted(candidate_edges)
        
        # Create a list of edges that are the smallest from the list of
        # candidate edges
        lowest_edge_candidates = []
        for i in range(len(candidate_list)):
            if candidate_edges[0] == candidate_list[i][-1]:
                lowest_edge_candidates.append(candidate_list[i])
        
        # Create a list of lowest vertex candidates, and add the vertex if it
        # is not already in the list and if it's not the last node added to the 
        # vertex list. Sort so that the first item is the lowest verte
        lowest_vertex_candidates = []
        for i in range(len(lowest_edge_candidates)):
            if lowest_edge_candidates[i][0] not in lowest_vertex_candidates and \
                                     lowest_edge_candidates[i][0] != vertex_list[-1]:
                lowest_vertex_candidates.append(lowest_edge_candidates[i][0])
            if lowest_edge_candidates[i][1] not in lowest_vertex_candidates and \
                                     lowest_edge_candidates[i][1] != vertex_list[-1]:
                lowest_vertex_candidates.append(lowest_edge_candidates[i][1])
        lowest_vertex_candidates = sorted(lowest_vertex_candidates)
        
        # Find the lowest vertex in the lowest edge candidates. Simply, find 
        # the lowest vertex in a 3-item list that has the lowest edge. Save the
        # lowest edge
        for i in range(len(lowest_edge_candidates)):
            if lowest_vertex_candidates[0] in lowest_edge_candidates[i]:
                lowest_edge = lowest_edge_candidates[i]
        
        # Create a list that will contain the next row to be inserted into CAM.
        # Add the vertex of the lowest edge left in the edges list
        next_row = []
        if lowest_edge[0] not in vertex_list:
            vertex_list.append(lowest_edge[0])
        if lowest_edge[1] not in vertex_list:
            vertex_list.append(lowest_edge[1])
        
        # Create a list of 3-item edge lists to be removed. After they have
        # been added to the CAM list, they can be removed from the edges list
        # that we still need to add to CAM
        list_for_removal = []
        for i in range(len(vertex_list) - 1):
            
            # Initialize a flag to signal whether an edge has been added to CAM
            # or not. If added, add to list for removal to be executed after 
            # the loop
            flag = 0
            for j in range(len(edges)):
                if vertex_list[i] in edges[j] and vertex_list[-1] in edges[j]:
                    next_row.append(edges[j][-1])
                    list_for_removal.append(edges[j])
                    flag = 1
            
            # If flag is still 0 at the end of the loop, there is no edge 
            # between the two nodes we are examining. Insert a '0' to the row
            # to indicate that no edge exists between the nodes
            if flag == 0:
                next_row.append('0')
        
        # For each list in the list for removal, remove it from the edges list
        for i in range(len(list_for_removal)):
            edges.remove(list_for_removal[i])
        
        # Add the vertex we are comparing all the previous vertices to to the
        # next row list, then add the whole row to CAM        
        next_row.append(vertex_list[-1])
        cam.append(next_row)
    
    # Create a list for the code corresponding to the CAM. Combine all the
    # individual lists in CAM and then combine the items into a single string
    code_cam = []
    for i in range(len(cam)):
        code_cam = code_cam + cam[i]
    code_cam = ''.join(code_cam)
   
    # Return the CAM and its code
    return cam, code_cam

def generateCAM(cam_a, cam_b):
    "This creates a new matrix using CAM to handle join case 1 (Both A and B" \
    " have at least two edge entries in the last row) and join case 2 (A has" \
    " at least two edge entries in last row but B has only one)."

    # case sensitivity, and change each integer to string
    for i in range(len(cam_a)):
        for j in range(len(cam_a[i])):
            if isinstance(cam_a[i][j],int):
                cam_a[i][j] = str(cam_a[i][j])
            cam_a[i][j] = cam_a[i][j].lower()
    for i in range(len(cam_b)):
        for j in range(len(cam_b[i])):
            if isinstance(cam_b[i][j],int):
                cam_b[i][j] = str(cam_b[i][j])
            cam_b[i][j] = cam_b[i][j].lower()
    
    # Finds the maximum number of potential edges in the last rows of the two 
    # input CAM graphs
    m = len(cam_a) - 1
    n = len(cam_b) - 1
    
    # If CAM a is larger than CAM b, switch the graphs
    if(n > m):
        temp = cam_a
        cam_a = cam_b
        cam_b = temp       
        
        # Switch the max potential edge count of the CAMs as well
        m = len(cam_a) - 1
        n = len(cam_b) - 1
    
    # Makes a copy of CAM a by creating an empty list for the MP submatrix and 
    # a temp list to temporarily store each line. Each iteration of a loop 
    # creates a list of each row, then appends it to the MP submatrix a list
    mp_sub_a = []
    temp_list = []
    for i in range(len(cam_a)):
        temp_list = list(cam_a[i])
        mp_sub_a.append(temp_list)
    
    # Saves the number of lists in the copy of CAM a in a variable    
    i = len(mp_sub_a) - 1
    
    # Initialize a flag. If the flag is not changed to 1, it means that no 
    # edges exist in the last row, and that row should be removed from the MP 
    # matrix a list       
    flag = 0
    for j in reversed(range(len(mp_sub_a[i])-1)):
        if(mp_sub_a[i][j] != '0'):
            mp_sub_a[i][j] = '0'
            break
    for j in range(len(mp_sub_a[i]) - 1):
        if mp_sub_a[i][j] != '0':
            flag = 1
    if not flag:
        mp_sub_a.remove(mp_sub_a[i])        
    
    # Makes a copy of CAM b by creating an empty list for the MP submatrix and 
    # a temp list to temporarily store each line. Each iteration of a loop 
    # creates a list of each row, then appends it to the MP submatrix b list
    mp_sub_b = []
    temp_list = []
    for i in range(len(cam_b)):
        temp_list = list(cam_b[i])
        mp_sub_b.append(temp_list)
        
    # Saves the number of lists in the copy of CAM b in a variable        
    i = len(mp_sub_b) - 1
    
    # Initialize a flag. If the flag is not changed to 1, it means that no 
    # edges exist in the last row, and that row should be removed from the MP 
    # matrix b list  
    for j in reversed(range(len(mp_sub_b[i])-1)):
        if(mp_sub_b[i][j] != '0'):
            mp_sub_b[i][j] = '0'
            break
    for j in range(len(mp_sub_b[i]) - 1):
        if mp_sub_b[i][j] != '0':
            flag = 1
    if not flag:
        mp_sub_b.remove(mp_sub_b[i])
    
    # Checks if the MP submatrices are the same. If they are different, prints 
    # a statement that the CAMs cannot be joined and returns an empty string
    if mp_sub_a != mp_sub_b:
        print("CAMs cannot be joined")
        return []
    
    # Count all the edges in the last row of CAM a
    edge_counter_a = 0       
    for i in range(len(cam_a[m]) - 1):
        if cam_a[m][i] != '0':
            edge_counter_a = edge_counter_a + 1
    
    # Count all the edges in the last row of CAM b
    edge_counter_b = 0            
    for j in range(len(cam_b[n]) - 1):
        if cam_b[n][j] != '0':
            edge_counter_b = edge_counter_b + 1
    
    # Using the definitions of each join case, use the edge counts to set the 
    # join case variable to the appropriate value 
    if edge_counter_a >= 2 and edge_counter_b >= 2:
        join_case = 1
    elif (edge_counter_a >= 2 and edge_counter_b == 1) or \
        (edge_counter_a == 1 and edge_counter_b >= 2):
        join_case = 2
    elif edge_counter_a == 1 and edge_counter_b == 1:
        join_case = 3
    
    # Initially set CAM c to CAM a, so that CAM c contains the dimensions of 
    # the larger CAM. CAM a will be compared to CAM b, and CAM c will be 
    # changed whenever a specific area needs to be joined
    cam_c = []
    temp_list = []
    for i in range(len(cam_a)):
        temp_list = list(cam_a[i])
        cam_c.append(temp_list)
    
    # Switch the counter variable from n to i to keep track of place in the 
    # loop
    i = n
    
    # Join the relevant rows of CAM a and CAM b together
    for j in range(len(cam_b[i]) - 1):
        if cam_a[i][j] == cam_b[i][j]:
            continue
        elif cam_a[i][j] != '0' and cam_b[i][j] == '0':
            cam_c[i][j] = cam_a[i][j]
        elif cam_a[i][j] == '0' and cam_b[i][j] != '0':
            cam_c[i][j] = cam_b[i][j]
    
    # Check the join case and print it out
    if join_case == 1:
        print("Case 1")
    elif join_case == 2:
        print("Case 2")
    elif join_case == 3:
        if(m != n) and cam_a[m - 1][-1] == cam_b[n][-1]:
            print("Case 3a")
        print("Case 3b")
        cam_c = []    
    
    # Return the join result
    return cam_c    