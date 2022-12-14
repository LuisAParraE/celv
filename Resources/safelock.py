class safelock:
    father = -1
    children = -1
    version = -1
    content =  -1

    def __init__(self,father = -1 ,children = -1,version = -1, content = -1):
        self.father = father
        self.children = children
        self.version = version
        self.content =  content