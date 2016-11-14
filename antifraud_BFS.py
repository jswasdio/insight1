
# coding: utf-8

# Implement using Breadth First Search Algorithms
# Reference from MIT online courseware 6.006 
# BFS (V,Adj,s): See CLRS for queue-based implementation 
#     level = { s: 0 } 
#     parent = {s : None } 
#     i = 1 
#     frontier = [s] # previous level, i−1 
#     while frontier: 
#         next = [ ] # next level, i 
#         for u in frontier: 
#             for v in Adj[u]: 
#                 if v not in level: # not yet seen 
#                     level[v] = i # level[u] + 1 
#                     parent[v] = u 
#                     next.append(v) 
#         frontier = next 
#         i + =1
# 

# In[57]:

import csv

#input file
batch_filename = 'batch_payment_test_f3.txt'
stream_filename = 'stream_payment_test_f3.txt'
#batch_filename = 'batch_payment.txt'
#stream_filename = 'stream_payment.txt'
feature1_output = 'output1.txt'
feature2_output = 'output2.txt'
feature3_output = 'output3.txt'

#batch_filename = 'batch_payment.txt'
#stream_filename = 'stream_payment.txt'
connections_dict ={}


def check_newuser(user):
    if user in connections_dict:
        newflag ='N'
    else:
        newflag ='Y'
    return newflag

#build user connections
def build_connections(batch_filename):
    cnt = 0
    with open(batch_filename, 'r', encoding='utf-8') as batchfile:
        next(batchfile)
        with open('debug.txt', 'w',) as debugfile:
            reader = csv.reader(batchfile)
            #assume data came in order (of time)
            for row in reader:
                cnt += 1
                debugfile.write(str(cnt)+'\n')
                if row:
                    user1 = int(row[1])
                    user2 = int(row[2])
                    if user1 in connections_dict:
                        connections_dict[user1].add(user2)
                    else:
                        connections_dict[user1] = {user2}

                    if user2 in connections_dict:
                        connections_dict[user2].add(user1)
                    else:
                        connections_dict[user2] = {user1}  




build_connections(batch_filename)
print('build connection completed')


def find_connections_BFS (payer,payee,degree): 
    '''
    payee= user who receives a payment
    payer =user who makes a payment
    degree = degree of connections, first degree = 1
    
    '''

    Adj = connections_dict
    foundFlag = True
    validation_f3 = 'unverified'
    level = { payer: 0 } 
    parent = {payer : None } 
    i = 1 
    frontier = [payer] # previous level, i−1 
    
    while frontier and i <= degree: 
        next = [] # next level, i 
        for u in frontier: 
            for v in Adj[u]: 
                if int(v) == int(payee):
                    validation_f3 = 'trusted'
                    foundFlag = 'Y'
                else:
                    if v not in level: # not yet seen 
                        level[v] = i # level[u] + 1 
                        parent[v] = u 
                        next.append(v)
        if foundFlag == 'Y':
            frontier =[]
        else:            
            frontier = next     
        i +=1
    return validation_f3
print('find_connection_BFS completed')


# In[60]:

#validate users connection for feature1
with open(stream_filename, 'r', encoding='utf-8') as streamfile:
    with open(feature1_output, 'w',) as f1file:
        next(streamfile)
        reader = csv.reader(streamfile)
        #assume data came in order of time
        for row in reader:
            payer = int(row[1])
            payee = int(row[2])
            #Find immediate connections (first degree of connections)
            max_degree = 1
            
            #New user comes in, no historical to verify connections
            if check_newuser(payer) =='Y':
                validation_f1 ='unverified'
            #Existing users, historical datas are available to verify connection
            else:          
                validation_f1 = find_connections_BFS(payer,payee,max_degree)
            print(validation_f1)
            f1file.write(validation_f1+'\n')
            
print('feature1_completed')


# In[65]:

#validate users connection for feature2
with open(stream_filename, 'r', encoding='utf-8') as streamfile:
    with open(feature2_output, 'w',) as f2file:
        next(streamfile)
        reader = csv.reader(streamfile)
        #assume data came in order of time
        for row in reader:
            payer = int(row[1])
            payee = int(row[2])
            max_degree =1

            
            #New user comes in, no historical data to verify connections
            if check_newuser(payer) =='Y':
                validation_f2 ='unverified'
                
            #existing user comes in, can use historical data to verify connections
            else:
                validation_f1 = find_connections_BFS(payer,payee,max_degree)
                if validation_f1 == 'trusted':
                    validation_f2 = validation_f1
                else:
                    for nested_user in connections_dict[payer]:
                        validation_f2 = find_connections_BFS(nested_user,payee,max_degree)
            print(validation_f2)
            f2file.write(validation_f2+'\n')

print('feature2_completed')           

            
            


# In[ ]:

#test = [49466,8552,52349,6989]
#test = [1,2,3,4,5]  
#for key in test:
#   print(key, connections_dict[key])


# In[59]:

#validate users connection for feature3
with open(stream_filename, 'r', encoding='utf-8') as streamfile:
    with open(feature3_output, 'w',) as f3file:
        next(streamfile)
        reader = csv.reader(streamfile)
        #assume data came in order of time
        for row in reader:
            payer = int(row[1])
            payee = int(row[2])
            #Find within fourth degree of connections)
            max_degree = 4

            
            #New user comes in, no historical data to verify connections
            if check_newuser(payer) =='Y':
                validation_f3 ='unverified'
            existing user comes in, can use historical data to verify connections
            else:          
                validation_f3 = find_connections_BFS(payer,payee,max_degree)
            print(validation_f3)
            f3file.write(validation_f3+'\n')
            
print('feature3_completed')


# In[43]:

#validate users connection for feature3
with open(stream_filename, 'r', encoding='utf-8') as streamfile:
    with open(feature3_output, 'w',) as f3file:
        next(streamfile)
        reader = csv.reader(streamfile)
        #assume data came in order of time
        for row in reader:
            #cnt += 1
            #print(cnt)
            user1 = int(row[1])
            user2 = int(row[2])
            #print(user1)
            #print(user2)
            
            #New user comes in, no historical to verify connections
            if check_newuser(user1) =='Y':
                validation_f3 ='unverified'
                
            #existing user comes in, can use historical data to verify connections from level to level 4
            else:
                validation_f3_l1 = check_connections(user1,user2)
                if validation_f3_l1 == 'trusted':
                    validation_f3 = 'trusted'
                else:
                    for nested_l1_user in connections_dict[user1]:
                        validation_f3_l2 = check_connections(nested_l1_user,user2)
                        if validation_f3_l2 == 'trusted':
                            validation_f3 = 'trusted'
                            break
                        else:
                            for nested_l2_user in connections_dict[nested_l1_user]:
                                validation_f3_l3 = check_connections(nested_l2_user,user2)
                                if validation_f3_l3 == 'trusted':
                                    validation_f3 = 'trusted'
                                    break
                                else:
                                    for nested_l3_user in connections_dict[nested_l2_user]:
                                        validation_f3_l4 = check_connections(nested_l3_user,user2)
                                        if validation_f3_l4 == 'trusted':
                                            validation_f3 = 'trusted'
                                            break
                                        else:
                                            validation_f3 = 'unverified'
                                    
            print(validation_f3)
            f3file.write(validation_f3+'\n')
            
print('feature3_completed')


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



