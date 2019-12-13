from postgre_conn import executeQuery
from prefixspan import PrefixSpan
#get relevant data

#This will create a LIST OF motion sensors ordered by Datetime
sql_str = "SELECT sname FROM Motion WHERE smessage = 'ON' ORDER BY sdatetime"

motion_list = executeQuery(sql_str)

#this changes the result to remove empty elements
#motion_list = [item[0] for item in motion_list]

print(motion_list)

i = 0
j = 0
mod = 4
motion_matrix = []
temp_list = []
last_event = None

# I removed repeat sensor events because that gives us less information
# this loop could be improved alot, I think the output of the mining will be determined too much by the read in order of
#the dataset
for event in motion_list:
    try:
        #converts sensor to int i think this conversion might work better
        now_event = int(event[0][-3:])
        #print(now_event)
        if last_event != now_event:
            temp_list.append(now_event)
            if i % mod == 0:
                motion_matrix.append(temp_list)
                temp_list = []
                j = j + 1
            i = i + 1
        last_event = now_event
    except:
        print("event read in error")

print(motion_matrix)

ps = PrefixSpan(motion_matrix)

frequent_items = ps.frequent(10) #10 is just here to make the serach faster
f_itemset = []

#find the events over 3
for item in frequent_items:
    if len(item[1]) > 3:
        f_itemset.append(item)

#sorts the frequent items by
f_itemset = sorted(f_itemset, key=lambda f_itemset: f_itemset[0], reverse=True)
print(f_itemset)
