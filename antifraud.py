import csv

#input file
batch_filename = 'batch_payment_test_f3.txt'
stream_filename = 'stream_payment_test_f3.txt'
#batch_filename = 'batch_payment.txt'
#stream_filename = 'stream_payment.txt'
feature1_output = 'output1.txt'
feature2_output = 'output2.txt'
feature3_output = 'output3.txt'
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



def check_connections(user1,user2):
    if user1 in connections_dict:
        if user2 in connections_dict[user1]:
            validation = 'trusted'

        else:
            validation ='unverified'
 
    else:
        validation = 'unverified'
 
    return (validation)      
        

#build user connections
build_connections(batch_filename)


#validate users connection for feature1
with open(stream_filename, 'r', encoding='utf-8') as streamfile:
    with open(feature1_output, 'w',) as f1file:
        next(streamfile)
        reader = csv.reader(streamfile)
        #assume data came in order of time
        for row in reader:
            user1 = int(row[1])
            user2 = int(row[2])
            #New user come in, no historical to verify connections
            if check_newuser(user1) =='Y':
                validation_f1 = 'unverified'
                
            #existing users comes in, can use historical data to verify connections
            else:
                validation_f1 = check_connections(user1,user2)
            f1file.write(validation_f1+'\n')
print('feature1_completed')

#validate users connection for feature2
with open(stream_filename, 'r', encoding='utf-8') as streamfile:
    with open(feature2_output, 'w',) as f2file:
        next(streamfile)
        reader = csv.reader(streamfile)
        #assume data came in order of time
        for row in reader:

            user1 = int(row[1])
            user2 = int(row[2])
            
            #New user comes in, no historical to verify connections
            if check_newuser(user1) =='Y':
                validation_f2 ='unverified'
                
            #existing user comes in, can use historical data to verify connections
            else:
                validation_f1 = check_connections(user1,user2)
                if validation_f1 == 'trusted':
                    validation_f2 = validation_f1
                else:
                    for nested_user in connections_dict[user1]:
                        validation_f2 = check_connections(nested_user,user2)
            #print(validation_f2)
            f2file.write(validation_f2+'\n')

print('feature2_completed')           

#validate users connection for feature3
with open(stream_filename, 'r', encoding='utf-8') as streamfile:
    with open(feature3_output, 'w',) as f3file:
        next(streamfile)
        reader = csv.reader(streamfile)
        #assume data came in order of time
        for row in reader:

            user1 = int(row[1])
            user2 = int(row[2])

            
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
                                    

            f3file.write(validation_f3+'\n')
            
print('feature3_completed')

