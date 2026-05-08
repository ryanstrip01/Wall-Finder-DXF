from grouping_lines import grupuri
from triangulation  import b
from utils import AbsDistance

# for i in grupuri:
    
    # print (i)
    # print('\n')

# print(grupuri[0])




def UnionLogic():
    dists = []
    lindist = []
    
    
    for lines in grupuri[0]:
        # print(lines)
        x = AbsDistance.absdistance(lines)
        dists.append(x)
        lindist.append(
            {'line': lines, 'dists': x }
        )
        
    #Glued lines handling: 
    
        
        
    return lindist
    

# UnionLogic()
print(UnionLogic())