from Resources.safelock import safelock

class directory:
    name = "uwu"
    father = None
    children = None
    version = 0
    safelock = None
    celv = False
    celvIndex = -1
    

    def __init__(self,newName,newFather,newChildren,newVersion):
        self.name = newName
        self.father=newFather
        self.children = newChildren
        self.version = newVersion
        self.safelock = None
        self.celv = False
        self.celvIndex = -1

    def addChildren(self,newChild):

        self.children.append(newChild)

    def deleteChildren(self,hatedChild):

        self.children.remove(hatedChild)

    def changeSafelock(self,version,father,children, content):
        self.safelock = safelock(father,children,version,content)

class file:
    name = "uwu"
    father = None
    content = ""
    version = 0
    safelock = None
    celv = False
    celvIndex = -1

    def __init__(self,newName,newFather,newVersion):
        self.name = newName
        self.father=newFather
        self.version = newVersion
        self.safelock = None
        self.content = ""
        self.celv = False
        self.celvIndex = -1

    def changeContent(self,newContent):
        
        self.content = newContent

    def changeSafelock(self,version,father = -1 ,children = -1, content = -1):
        self.safelock = safelock(father,children,version,content)