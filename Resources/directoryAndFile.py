from Resources.safelock import safelock

class directory:
    name = "uwu"
    father = None
    children = None
    version = 0
    safelock = None

    def __init__(self,newName,newFather,newChildren,newVersion):
        self.name = newName
        self.father=newFather
        self.children = newChildren
        self.version = newVersion
        self.safelock = safelock()

    def addChildren(self,newChild):

        self.children.append(newChild)

    def deleteChildren(self,hatedChild):

        self.children.remove(hatedChild)

    def changeSafelock(self,version,father = -1 ,children = -1, content = -1):
        self.safelock.version = version
        self.safelock.father = father
        self.safelock.children = children
        self.safelock.content = content

class file:
    name = "uwu"
    father = None
    content = ""
    version = 0
    safelock = None

    def __init__(self,newName,newFather,newVersion):
        self.name = newName
        self.father=newFather
        self.version = newVersion
        self.safelock = safelock()
        self.content = ""

    def changeContent(self,newContent):
        
        self.content = newContent

    def changeSafelock(self,version,father = -1 ,children = -1, content = -1):
        self.safelock.version = version
        self.safelock.father = father
        self.safelock.children = children
        self.safelock.content = content