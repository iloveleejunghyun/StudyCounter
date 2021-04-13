# Name List
name_list = ['Peter', 'Mary', 'John', 'Lily']

# Age tuple
age_tuple = (20, 21, 25, 30)

#
# Using name_list and age_tuple
# instead of any hardcoded values
#
# Write some python code to generate a dictionary where d
# d = {'Peter':20, 'Mary':21, 'John':25, 'Lily':30}
#
# Your code must be robust enough to handle any error situation
#

def combine(name_list, age_tuple):
    dic = dict()
    if len(name_list) != len(age_tuple):
        print("err, every name should have an age!")
        return None
    if name_list == None or age_tuple == None or len(name_list) == 0 or len(age_tuple) == 0:
        return dict()
        
    n = len(name_list)
    for i in range(n):
        if name_list[i] in dic:
            print("err, duplicate name:", name_list[i])
            return None
        dic[name_list[i]] = age_tuple[i]

    return dic

print(combine(name_list, age_tuple))

def g_sum(start, end):
    return (int)((start+end) * (end-start+1))/2
res = g_sum(520895777, 773160767)
print(res, res %(10**9+7))

arr = [i for i in range(1,5000)]
print(arr)