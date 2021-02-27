import copy

class playground:
    def __init__(self,fields):
        self.fields=fields
        self.parent=None
        self.f=0
        self.parentaction=None

    def getfvalue(self):
        pathcost=0
        node=self
        while(node.parent!=None):
            node=node.parent
            pathcost+=1
        hioristic=0
        for i in self.fields:
            if(i!=[]):
                firstcolor=i[0].color
                for j in i:
                    if(j.color!=firstcolor):
                        hioristic+=5
                        break
        for i in self.fields:
            if(i!=[]):
                mylist=[]
                for j in i:
                    mylist.append(j.number)
                if(sorted(mylist)[::-1]!=mylist):
                    hioristic+=1
                    break
        return pathcost+hioristic



    
    def addparent(self,parent):
        self.parent=parent

    def actions(self):
        actions=[]
        for index1,i in enumerate(self.fields):
            for index2,j in enumerate(self.fields):
                if(j==[] and i!=[]):
                    actions.append((index1,index2))
                elif(i==[]):
                    pass
                elif(i[-1].number<j[-1].number):
                    actions.append((index1,index2))
                else:
                    pass
        return actions

    def do(self,action):
        self.fields[action[1]].append(self.fields[action[0]].pop())

    def checkcolor(self):
        for i in self.fields:
            if(i!=[]):
                firstcolor=i[0].color
                for j in i:
                    if(j.color!=firstcolor):
                        return False
        return True

    def checkdesc(self):
        for i in self.fields:
            if(i!=[]):
                mylist=[]
                for j in i:
                    mylist.append(j.number)
                if(sorted(mylist)[::-1]!=mylist):
                    return False
        return True


class card:
    def __init__(self,color,number):
        self.color=color
        self.number=int(number)
    def __str__(self):
        return str(self.color)+"-"+str(self.number)


def goaltest(state):
    if(state.checkdesc() and state.checkcolor()):
        return True
    else:
        return False

def check(state,frontier,explored):
    for i in frontier:
        if(fieldscompare(i.fields,state.fields)):
            if(i.getfvalue()>state.getfvalue()):
                frontier.remove(i)
                frontier.append(state)
            return False
    for j in explored:
        if(fieldscompare(j.fields,state.fields)):
            return False
    return True

def fieldscompare(field1,field2):
    for i in range(len(field2)):
        if(len(field2[i])!=len(field1[i])):
            return False
        else:
            for j in range(len(field1[i])):
                if(field1[i][j].number!=field2[i][j].number):
                    return False
                if(field1[i][j].color!=field2[i][j].color):
                    return False
    return True


def printstate(state):
    for i in state.fields:
        for k in i:
            print(k, end =" ")
        print("")

def printactions(state):
    node=state
    actions=[]
    actions.append(node.parentaction)
    while(node.parent!=None):
        node=node.parent
        actions.append(node.parentaction)
    depth=len(actions)
    for i in range(len(actions)):
        action=actions.pop()
        if(action!=None):
            print(action[0],end=" ")
            print("--->",end=" ")
            print(action[1])
    return depth-1
        
def getlowest(frontier):
    result=frontier[0]
    cost=result.getfvalue()
    for i in frontier:
        if(i.getfvalue()<cost):
            cost=i.getfvalue()
            result=i
    frontier.remove(result)
    return result


def astar(initstate):
    if(goaltest(initstate)):
        return [initstate,0,0]
    frontier=[]
    explored=[]
    frontier.append(initstate)
    while(True):
        if(len(frontier)==0):
            return "failure"
        currstate=getlowest(frontier)
        if(goaltest(currstate)==True):
            return [currstate,len(frontier)+len(explored),len(explored)]
        explored.append(currstate)
        for action in currstate.actions():
            child=copy.deepcopy(currstate)
            child.do(action)
            child.addparent(copy.deepcopy(currstate))
            child.parentaction=action
            if(check(child,frontier,explored)):  #check if child is in frontier or explored or not
                if(goaltest(child)==True):
                    return [child,len(frontier)+len(explored),len(explored)]
                frontier.append(child)



        
        




numbers = input("").split(' ')
n,m,k = int(numbers[0]),int(numbers[1]),int(numbers[2])
mylist=[]
templist=[]
for i in range(k):
    temp=input("").split(" ")
    if(temp[0]=="#"):
        mylist.append([])
    else:
        for j in range(len(temp)):
            templist.append(card(temp[j][len(temp[j])-1],temp[j][0:len(temp[j])-1]))
        mylist.append(templist)
    templist=[]
initstate=playground(mylist)
result=astar(initstate)
if(result=="failure"):
    print("failure")
else:
    print("final state is :")
    print("")
    printstate(result[0])
    print("")
    print("actions:")
    print("")
    depth=printactions(result[0])
    print("")
    print("soloution depth:", end="")
    print(depth)
    print("nodes created:",end="")
    print(result[1])
    print("nodes expanded:",end="")
    print(result[2])