class safelock:
    father = None
    children = None
    version = None
    content =  None

    def __init__(self,father = -1 ,children = -1,version = -1, content = -1):
        self.father = father
        self.children = children
        self.version = version
        self.content =  content