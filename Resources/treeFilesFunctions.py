from Resources.directoryAndFile import directory, file, safelock
from pathlib import Path


class celvId:
    id = -1
    celvRoots = []
    versionCount = 0

    def __init__(self,id) -> None:
        self.id = id
        self.versionCount = 0

    def addRoot(self, root):
        self.celvRoots.append(root)


celvVersions = []
changeOnCicle = False

def checkParents(arbolito):
    if arbolito.father != None:
        if arbolito.father.celv:
            raise Exception
        else:
            checkParents(arbolito.father)


def checkChildren(arbolito):
    for element in arbolito.children:
        if isinstance(element,directory):
            if element.celv:
                raise Exception
            checkChildren(element)
        elif isinstance(element,file):
            if element.celv:
                raise Exception

def celv_vamos(arbolito,version):
    global celvVersions

    if arbolito.celv:
        newRoot = None
        versionIndex = 0
        for i in range(0,len(celvVersions)):
            if celvVersions[i].id == arbolito.celvIndex:
                versionIndex = i
                break
        print(version)
        for element in celvVersions[i].celvRoots:
            if element.safelock != None and element.safelock.version <= version:
                print("Nodo 1")
                newRoot = element
                
            elif element.version <= version:
                print("Nodo 2")
                newRoot = element
        return (newRoot,version)
    else:
        raise Exception

def celv_inicilizator(arbolito,index):
    arbolito.celv = True
    arbolito.celvIndex = index
    if isinstance(arbolito,directory):
        for element in arbolito.children:
            celv_inicilizator(element,index)

def celv_iniciar(arbolito):
    global celvVersions

    checkParents(arbolito)
    if isinstance(arbolito,directory):
        checkChildren(arbolito)
    
    if len(celvVersions) == 0:
        index = 0
        nuevoIndex = celvId(0)
    else:
        index = celvVersions[len(celvVersions)-1].id +1
        nuevoIndex = celvId(index)
    
    celv_inicilizator(arbolito,index)

    nuevoIndex.addRoot(arbolito)

    celvVersions.append(nuevoIndex)

def encontrar_nombre(arbolito,name,version):
    global celvVersions

    if arbolito.celv:
        if isinstance(arbolito, directory):
            if arbolito.name == name:
                print("error 1")
                raise Exception
            if arbolito.safelock != None and arbolito.safelock.children != -1 and arbolito.safelock.version <= version:
                for element in arbolito.safelock.children:
                    if isinstance(element, directory):
                        if element.name == name:
                            print("error 2")
                            raise Exception
                        
                        if arbolito.celv == False and element.celv:
                            versionIndex = 0
                            for i in range(0,len(celvVersions)):
                                if celvVersions[i].id == element.celvIndex:
                                    versionIndex = i
                                    break
                            encontrar_nombre(element,name,celvVersions[versionIndex].versionCount)
                        else:
                            encontrar_nombre(element,name,version)

                    elif isinstance(element, file):
                        if element.name == name:
                            print("error 3")
                            raise Exception
            else:
                for element in arbolito.children:
                    if isinstance(element, directory):

                        if element.name == name:
                            print("error 2")
                            raise Exception
                        encontrar_nombre(element,name,version)

                    elif isinstance(element, file):
                        if element.name == name:
                            print("error 3")
                            raise Exception

        elif isinstance(arbolito, file):
            if arbolito.name == name:
                print("error 4")
                raise Exception
    else:
        if isinstance(arbolito, directory):
            if arbolito.name == name:
                print("error 1")
                raise Exception

            for element in arbolito.children:
                if isinstance(element, directory):

                    if element.name == name:
                        print("error 2")
                        raise Exception
                    encontrar_nombre(element,name,version)

                elif isinstance(element, file):
                    if element.name == name:
                        print("error 3")
                        raise Exception

        elif isinstance(arbolito, file):
            if arbolito.name == name:
                print("error 4")
                raise Exception

def crear_dir(arbolito,name,version):
    global celvVersions
    encontrar_nombre(arbolito,name,version)

    if arbolito.celv:
        versionIndex = 0
        for i in range(0,len(celvVersions)):
            if celvVersions[i].id == arbolito.celvIndex:
                versionIndex = i
                break

        celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1
        if isinstance(arbolito,directory):
            newChild = directory(name,arbolito,[],celvVersions[versionIndex].versionCount)
            newChild.celv = True
            newChild.celvIndex = celvVersions[versionIndex].id

            if arbolito.safelock ==None:
                print("crear 1")
                arbolito.changeSafelock(celvVersions[versionIndex].versionCount,-1,arbolito.children,-1)
                arbolito.safelock.children.append(newChild)
                return (arbolito,celvVersions[versionIndex].versionCount)
            else:
                print("crear 2")
                return (updateTreeAdd(arbolito,newChild,versionIndex,version),celvVersions[versionIndex].versionCount)
        else:
            print("error 5")
            raise Exception
    else:
        if isinstance(arbolito,directory):
            newChild = directory(name,arbolito,[],0)
            arbolito.addChildren(newChild)
            return (arbolito,0)
        else:
            print("error 6")
            raise Exception

def crear_archivo(arbolito,name,version):
    global celvVersions

    encontrar_nombre(arbolito,name,version)
    if arbolito.celv:
        versionIndex = 0
        for i in range(0,len(celvVersions)):
            if celvVersions[i].id == arbolito.celvIndex:
                versionIndex = i
                break

        celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1
        if isinstance(arbolito,directory):
            newChild = file(name,arbolito,celvVersions[versionIndex].versionCount)
            newChild.celv =  True
            newChild.celvIndex = celvVersions[versionIndex].id

            if arbolito.safelock ==None:
                print("crear 1")
                arbolito.changeSafelock(celvVersions[versionIndex].versionCount,-1,arbolito.children,-1)
                arbolito.safelock.children.append(newChild)
                return (arbolito,celvVersions[versionIndex].versionCount)
            else:
                print("crear 2")
                return (updateTreeAdd(arbolito,newChild,versionIndex,version),celvVersions[versionIndex].versionCount)
        else:
            print("error 5")
            raise Exception
    else:
        print("uwu")
        if isinstance(arbolito,directory):
            newChild = file(name,arbolito,0)
            arbolito.addChildren(newChild)
            return (arbolito,0)
        else:
            print("error 6")
            raise Exception

def escribir(arbolito, name, content,version):
    global celvVersions
    writed = None
    if arbolito.celv:
        writed = escribirTree(arbolito,name,content,version)
        if writed == None:
            raise FileNotFoundError
        return writed
    else:
        if isinstance(arbolito, directory):
            for element in arbolito.children:
                if isinstance(element, directory):
                    try:
                        writed = escribir(element,name,content,version)
                        if writed != None:
                            return (arbolito.father,version)
                    except:
                        pass
                elif isinstance(element, file):
                    if element.name == name:
                        element.content = content
                        return (arbolito,version)
        elif isinstance(arbolito, file):
            if arbolito.name == name:
                arbolito.content = content
                return (arbolito,version)
        if writed == None:
            raise FileNotFoundError

def escribirTree(arbolito,name,content,version):
    global celvVersions
    writed = None
    if isinstance(arbolito, directory):
            if arbolito.safelock != None and arbolito.safelock.children != -1 and arbolito.safelock.version <= version:
                for element in arbolito.safelock.children:
                    if isinstance(element, directory):
                        try:
                            writed = escribirTree(element,name,content,version)
                            if writed != None:
                                return (writed[0].father,writed[1])
                        except:
                            pass
                    elif isinstance(element, file):
                        if element.name == name:
                            versionIndex = 0
                            for i in range(0,len(celvVersions)):
                                if celvVersions[i].id == arbolito.celvIndex:
                                    versionIndex = i
                                    break
                            celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1

                            if element.safelock == None:
                                element.changeSafelock(celvVersions[versionIndex].versionCount,-1,-1,content)
                                return (element.father,celvVersions[versionIndex].versionCount)
                            elif element.safelock != None:
                                newFile = file(element.name,element.father,celvVersions[versionIndex].versionCount)
                                newFile.celv = True
                                newFile.celvIndex = element.celvIndex
                                newFile.content =  content

                                if element.safelock.father != -1 and element.safelock.version <= version:
                                    newFile.father = element.safelock.father

                                updateParents(element,newFile,versionIndex,version)
                                
                                return (newFile.father,celvVersions[versionIndex].versionCount)
            else:
                for element in arbolito.children:
                    if isinstance(element, directory):
                        try:
                            writed = escribirTree(element,name,content,version)
                            if writed != None:
                                return (writed[0].father,writed[1])
                        except:
                            pass
                    elif isinstance(element, file):
                        if element.name == name:
                            versionIndex = 0
                            for i in range(0,len(celvVersions)):
                                if celvVersions[i].id == arbolito.celvIndex:
                                    versionIndex = i
                                    break
                            celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1
                            
                            if element.safelock == None:
                                element.changeSafelock(celvVersions[versionIndex].versionCount,-1,-1,content)
                                return (element.father,celvVersions[versionIndex].versionCount)
                            elif element.safelock != None:
                                newFile = file(element.name,element.father,celvVersions[versionIndex].versionCount)
                                newFile.celv = True
                                newFile.celvIndex = element.celvIndex
                                newFile.content =  content

                                if element.safelock.father != -1 and element.safelock.version <= version:
                                    newFile.father = element.safelock.father

                                updateParents(element,newFile,versionIndex,version)
                                
                                return (newFile.father,celvVersions[versionIndex].versionCount)
    if writed == None:
        raise FileNotFoundError

def eliminar(arbolito,name,version):
    global celvVersions
    deleted = None
    if arbolito.celv:
        deleted = eliminarTree(arbolito,name,version)
        if deleted == None:
            raise FileNotFoundError
        return deleted
    else:
        if isinstance(arbolito, directory):
            if arbolito.name == name:
                if arbolito.father == None:
                    return(None,0)
                else:
                    arbolito.father.children.remove(arbolito)
                    return(arbolito.father,0)
            for element in arbolito.children:
                if isinstance(element, directory):
                    if element.name == name:   
                        element.father.deleteChildren(element)
                        return (element.father,version)
                    else:
                        try:
                            deleted = eliminar(element,name,version)
                            if deleted != None:
                                return (deleted[0].father,0)
                        except:
                            pass
                elif isinstance(element, file):
                    if element.name == name:
                        element.father.deleteChildren(element)
                        return (element.father,version)
        if deleted == None:
            raise FileExistsError

def eliminarTree(arbolito,name,version):
    global celvVersions
    deleted = None
    if isinstance(arbolito, directory):
            if arbolito.name == name:
                print("eliminar 1")
                versionIndex = 0
                for i in range(0,len(celvVersions)):
                    if celvVersions[i].id == arbolito.celvIndex:
                        versionIndex = i
                        break

                if arbolito.safelock != None and arbolito.safelock.father != -1:
                    celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1

                    if arbolito.safelock.father.safelock == None:
                        arbolito.safelock.father.changeSafelock(version,-1,arbolito.safelock.father.children,-1)
                        arbolito.safelock.father.children.remove(arbolito)
                        return(arbolito.safelock.father,version)

                    elif arbolito.safelock.father.safelock != None:
                        newFather = directory(arbolito.safelock.father.name,arbolito.safelock.father.father,arbolito.safelock.father.children,version)
                        newFather.celv = True
                        newFather.celvIndex = arbolito.safelock.father.celvIndex

                        if arbolito.safelock.father.safelock.children != -1:
                            newFather.children = arbolito.safelock.father.safelock.children

                        if arbolito.safelock.father.safelock.father != -1:
                            newFather.father = arbolito.safelock.father.safelock.father

                        newFather.children.remove(arbolito)

                        updateChildrenCicle(newFather,version)
                        updateParents(arbolito.safelock.father,newFather,versionIndex)

                        return(newFather,version)
                else:
                    if arbolito.father == None or (arbolito.father!=None and arbolito.father.celv == False):
                        celvVersions.pop(versionIndex)
                        if arbolito.father == None:
                            return(None,0)
                        else:
                            arbolito.father.children.remove(arbolito)
                            return(arbolito.father,0)
                    else:
                        
                        celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1

                        if arbolito.father.safelock == None:
                            arbolito.father.changeSafelock(version,-1,arbolito.father.children,-1)
                            arbolito.father.children.remove(arbolito)
                            return(arbolito.father,version)

                        elif arbolito.father.safelock != None:
                            newFather = directory(arbolito.father.name,arbolito.father.father,arbolito.father.children,version)
                            newFather.celv = True
                            newFather.celvIndex = arbolito.father.celvIndex

                            if arbolito.father.safelock.children != -1:
                                newFather.children = arbolito.father.safelock.children

                            if arbolito.father.safelock.father != -1:
                                newFather.father = arbolito.father.safelock.father

                            newFather.children.remove(arbolito)

                            updateChildrenCicle(newFather,versionIndex,version)
                            updateParents(arbolito.father,newFather,versionIndex,version)

                            return(newFather,version)
            else:
                if arbolito.safelock != None and arbolito.safelock.children != -1 and arbolito.safelock.version <= version:
                    for element in arbolito.safelock.children:
                        if isinstance(element, directory):
                            if element.name == name:
                                print("eliminar 2")
                                versionIndex = 0
                                for i in range(0,len(celvVersions)):
                                    if celvVersions[i].id == arbolito.celvIndex:
                                        versionIndex = i
                                        break
                                celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1
                                
                                if element.safelock != None and element.safelock.father != -1 and element.safelock.version <= version:
                                    if element.safelock.father.safelock == None:
                                        element.safelock.father.changeSafelock(celvVersions[versionIndex].versionCount,-1,element.safelock.father.children,-1)
                                        element.safelock.father.children.remove(element)

                                        return(element.safelock.father,celvVersions[versionIndex].versionCount)
                                    elif element.safelock.father.safelock != None:
                                        newFather = directory(element.safelock.father.name,element.safelock.father.father,element.safelock.father.children,celvVersions[versionIndex].versionCount)
                                        newFather.celv = True
                                        newFather.celvIndex = element.safelock.father.celvIndex

                                        if element.safelock.father.safelock.children != -1 and element.safelock.father.safelock.version <= version:
                                            newFather.children = element.safelock.father.safelock.children

                                        if element.safelock.father.safelock.father != -1 and element.safelock.father.safelock.version <= version:
                                            newFather.father = element.safelock.father.safelock.father

                                        newFather.children.remove(element)

                                        updateChildrenCicle(newFather,versionIndex,version)
                                        updateParents(element.safelock.father,newFather,versionIndex,version)

                                        return(newFather,celvVersions[versionIndex].versionCount)
                                else:
                                    if element.father.safelock == None:
                                        element.father.changeSafelock(celvVersions[versionIndex].versionCount,-1,element.father.children,-1)
                                        element.father.children.remove(element)

                                        return(element.father,celvVersions[versionIndex].versionCount)
                                    elif element.father.safelock != None:
                                        newFather = directory(element.father.name,element.father.father,element.father.children,celvVersions[versionIndex].versionCount)
                                        newFather.celv = True
                                        newFather.celvIndex = element.father.celvIndex

                                        if element.father.safelock.children != -1 and element.father.safelock.version <= version:
                                            newFather.children = element.father.safelock.children

                                        if element.father.safelock.father != -1 and element.father.safelock.version <= version:
                                            newFather.father = element.father.safelock.father

                                        newFather.children.remove(element)

                                        updateChildrenCicle(newFather,versionIndex,version)
                                        updateParents(element.father,newFather,versionIndex,version)

                                        return(newFather,celvVersions[versionIndex].versionCount)  
                            else:
                                try:
                                    deleted = eliminarTree(element,name,version)
                                    if deleted != None:
                                        return (deleted[0].father,deleted[1])
                                except:
                                    pass
                        elif isinstance(element, file):
                            if element.name == name:
                                print("eliminar 3")
                                versionIndex = 0
                                for i in range(0,len(celvVersions)):
                                    if celvVersions[i].id == arbolito.celvIndex:
                                        versionIndex = i
                                        break
                                celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1

                                if element.safelock != None and element.safelock.father != -1 and element.safelock.version <= version:
                                    print("eliminar 3.1")
                                    if element.safelock.father.safelock == None:
                                        element.safelock.father.changeSafelock(version,-1,element.safelock.father.children,-1)
                                        element.safelock.father.children.remove(element)

                                        return(element.safelock.father,celvVersions[versionIndex].versionCount)

                                    elif element.safelock.father.safelock != None:
                                        newFather = directory(element.safelock.father.name,element.safelock.father.father,element.safelock.father.children,version)
                                        newFather.celv = True
                                        newFather.celvIndex = element.safelock.father.celvIndex

                                        if element.safelock.father.safelock.children != -1 and element.safelock.father.safelock.version <= version:
                                            newFather.children = element.safelock.father.safelock.children

                                        if element.safelock.father.safelock.father != -1 and element.safelock.father.safelock.version <= version:
                                            newFather.father = element.safelock.father.safelock.father

                                        newFather.children.remove(element)

                                        updateChildrenCicle(newFather,versionIndex,version)
                                        updateParents(element.safelock.father,newFather,versionIndex,version)

                                        return(newFather,celvVersions[versionIndex].versionCount)
                                else:
                                    print("eliminar 3.2")
                                    if element.father.safelock == None:
                                        print("eliminar 3.2.1")
                                        element.father.changeSafelock(version,-1,element.father.children,-1)
                                        element.father.children.remove(element)

                                        return(element.father,celvVersions[versionIndex].versionCount)
                                    elif element.father.safelock != None:
                                        print("eliminar 3.2.2")
                                        newFather = directory(element.father.name,element.father.father,element.father.children,version)
                                        newFather.celv = True
                                        newFather.celvIndex = element.father.celvIndex

                                        if element.father.safelock.children != -1 and element.father.safelock.version <= version:
                                            newFather.children = element.father.safelock.children

                                        if element.father.safelock.father != -1 and element.father.safelock.version <= version:
                                            newFather.father = element.father.safelock.father

                                        newFather.children.remove(element)

                                        updateChildrenCicle(newFather,versionIndex,version)
                                        updateParents(element.father,newFather,versionIndex,version)

                                        return(newFather,celvVersions[versionIndex].versionCount)
                else:
                    for element in arbolito.children:
                        if isinstance(element, directory):
                            if element.name == name:
                                print("eliminar 4")
                                versionIndex = 0
                                for i in range(0,len(celvVersions)):
                                    if celvVersions[i].id == arbolito.celvIndex:
                                        versionIndex = i
                                        break
                                celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1
                                
                                if element.safelock != None and element.safelock.father != -1 and element.safelock.version <= version:
                                    if element.safelock.father.safelock == None:
                                        element.safelock.father.changeSafelock(celvVersions[versionIndex].versionCount,-1,element.safelock.father.children,-1)
                                        element.safelock.father.children.remove(element)

                                        return(element.safelock.father,celvVersions[versionIndex].versionCount)
                                    elif element.safelock.father.safelock != None:
                                        newFather = directory(element.safelock.father.name,element.safelock.father.father,element.safelock.father.children,celvVersions[versionIndex].versionCount)
                                        newFather.celv = True
                                        newFather.celvIndex = element.safelock.father.celvIndex

                                        if element.safelock.father.safelock.children != -1 and element.safelock.father.safelock.version <= version:
                                            newFather.children = element.safelock.father.safelock.children

                                        if element.safelock.father.safelock.father != -1 and element.safelock.father.safelock.version <= version:
                                            newFather.father = element.safelock.father.safelock.father

                                        newFather.children.remove(element)

                                        updateChildrenCicle(newFather,versionIndex,version)
                                        updateParents(element.safelock.father,newFather,versionIndex,version)

                                        return(newFather,celvVersions[versionIndex].versionCount)
                                else:
                                    if element.father.safelock == None:
                                        element.father.changeSafelock(celvVersions[versionIndex].versionCount,-1,element.father.children,-1)
                                        element.father.children.remove(element)

                                        return(element.father,celvVersions[versionIndex].versionCount)
                                    elif element.father.safelock != None:
                                        newFather = directory(element.father.name,element.father.father,element.father.children,celvVersions[versionIndex].versionCount)
                                        newFather.celv = True
                                        newFather.celvIndex = element.father.celvIndex

                                        if element.father.safelock.children != -1 and element.father.safelock.version <= version:
                                            newFather.children = element.father.safelock.children

                                        if element.father.safelock.father != -1 and element.father.safelock.version <= version:
                                            newFather.father = element.father.safelock.father

                                        newFather.children.remove(element)

                                        updateChildrenCicle(newFather,versionIndex,version)
                                        updateParents(element.father,newFather,versionIndex,version)

                                        return(newFather,celvVersions[versionIndex].versionCount)  
                            else:
                                try:
                                    deleted = eliminarTree(element,name,version)
                                    if deleted != None:
                                        return (deleted[0].father,deleted[1])
                                except:
                                    pass
                        elif isinstance(element, file):
                            if element.name == name:
                                print("eliminar 5")
                                versionIndex = 0
                                for i in range(0,len(celvVersions)):
                                    if celvVersions[i].id == arbolito.celvIndex:
                                        versionIndex = i
                                        break
                                celvVersions[versionIndex].versionCount = celvVersions[versionIndex].versionCount +1

                                if element.safelock != None and element.safelock.father != -1 and element.safelock.version <= version:
                                    if element.safelock.father.safelock == None:
                                        element.safelock.father.changeSafelock(version,-1,element.safelock.father.children,-1)
                                        element.safelock.father.children.remove(element)

                                        return(element.safelock.father,celvVersions[versionIndex].versionCount)

                                    elif element.safelock.father.safelock != None:
                                        newFather = directory(element.safelock.father.name,element.safelock.father.father,element.safelock.father.children,version)
                                        newFather.celv = True
                                        newFather.celvIndex = element.safelock.father.celvIndex

                                        if element.safelock.father.safelock.children != -1:
                                            newFather.children = element.safelock.father.safelock.children

                                        if element.safelock.father.safelock.father != -1:
                                            newFather.father = element.safelock.father.safelock.father

                                        newFather.children.remove(element)

                                        updateChildrenCicle(newFather,versionIndex,version)
                                        updateParents(element.safelock.father,newFather,versionIndex,version)

                                        return(newFather,celvVersions[versionIndex].versionCount)
                                else:
                                    if element.father.safelock == None:
                                        element.father.changeSafelock(version,-1,element.father.children,-1)
                                        element.father.children.remove(element)

                                        return(element.father,celvVersions[versionIndex].versionCount)
                                    elif element.father.safelock != None:
                                        newFather = directory(element.father.name,element.father.father,element.father.children,version)
                                        newFather.celv = True
                                        newFather.celvIndex = element.father.celvIndex

                                        if element.father.safelock.children != -1:
                                            newFather.children = element.father.safelock.children

                                        if element.father.safelock.father != -1:
                                            newFather.father = element.father.safelock.father

                                        newFather.children.remove(element)

                                        updateChildrenCicle(newFather,versionIndex,version)
                                        updateParents(element.father,newFather,versionIndex,version)

                                        return(newFather,celvVersions[versionIndex].versionCount)
    if deleted == None:
        raise FileNotFoundError

def leer(arbolito,name,version):
    if arbolito.celv:
        if isinstance(arbolito, directory):
            for element in arbolito.children:
                if isinstance(element, directory):
                    try:
                        printed = leer(element,name,version)
                        if printed == 0:
                            return 0
                    except:
                        pass
                elif isinstance(element, file):
                    if element.name == name:
                        if element.safelock != None and safelock.content !=-1 and element.safelock.version<=version:
                            print(element.safelock.content)
                        elif element.safelock == None:
                            print(element.content)
                        return 0
        raise FileNotFoundError
    else:
        if isinstance(arbolito, directory):
            for element in arbolito.children:
                if isinstance(element, directory):
                    try:
                        printed = leer(element,name,version)
                        if printed == 0:
                            return 0
                    except:
                        pass
                elif isinstance(element, file):
                    if element.name == name:
                        print(element.content)
                        return 0
        elif isinstance(arbolito, file):
            if arbolito.name == name:
                print(arbolito.content)
                return 0
        raise FileNotFoundError

def ir(arbolito,name,version):
    global celvVersions

    if arbolito.celv:
        if name == "":
            if arbolito.safelock != None and arbolito.safelock.father != -1 and arbolito.safelock.version <= version:
                if arbolito.safelock.father == None:
                    print("Error: Ya se encuentra en la Raiz del arbol")
                    raise Exception
                else:
                    return (arbolito.safelock.father,version)
            elif (arbolito.safelock != None and arbolito.safelock.father != -1  and arbolito.safelock.version > version):
                if arbolito.father == None:
                    print("Error: Ya se encuentra en la Raiz del arbol")
                    raise Exception
                else:
                    print("Padre1?")
                    if arbolito.father.celv:
                        return (arbolito.father, version)
                    else:
                        return (arbolito.father, 0)
            elif arbolito.safelock != None and arbolito.safelock.father == -1 :
                if arbolito.father == None:
                    print("Error: Ya se encuentra en la Raiz del arbol")
                    raise Exception
                else:
                    print("Padre1?")
                    if arbolito.father.celv:
                        return (arbolito.father, version)
                    else:
                        return (arbolito.father, 0)
            elif arbolito.safelock == None and arbolito.father != None:
                print("Padre2?")
                if arbolito.father.celv:
                    return (arbolito.father, version)
                else:
                    return (arbolito.father, 0)

            elif arbolito.safelock == None and arbolito.father == None:
                print("Error: Ya se encuentra en la Raiz del arbol")
                raise Exception
        else:
            if isinstance(arbolito, directory):
                if arbolito.safelock != None and arbolito.safelock.children != -1  and arbolito.safelock.version <= version:
                    for element in arbolito.safelock.children:
                        if element.name == name:
                            return (element,version)
                    print("Error: Nombre no encontrado!!")
                    raise NameError
                elif arbolito.safelock != None and arbolito.safelock.children != -1  and arbolito.safelock.version > version:
                    for element in arbolito.children:
                        if element.name == name:
                            return (element,version)
                    print("Error: Nombre no encontrado!!")
                    raise NameError
                elif arbolito.safelock == None:
                    for element in arbolito.children:
                        if element.name == name:
                            return (element,version)
                    print("Error: Nombre no encontrado!!")
                    raise NameError
    else:
        if name == "":
            if arbolito.father == None:
                print("Error: Ya se encuentra en la Raiz del arbol")
                raise Exception
            else:
                return (arbolito.father,0)
        else:
            if isinstance(arbolito, directory):
                for element in arbolito.children:
                    if element.name == name:
                        if element.celv:
                            versionNumbr = 0
                            for i in range(0,len(celvVersions)):
                                if celvVersions[i].id == element.celvIndex:
                                    versionNumbr = celvVersions[i].versionCount
                                    break
                            return (element,versionNumbr)
                        else:
                            return (element, 0)
                print("Error: Nombre no encontrado!!")
                raise NameError

def celv_importar(path):

    base = Path(path)

    if (not base.exists()) or (not base.is_dir()):
        raise FileNotFoundError


    baseDir = directory(base.name,None,[],0)


    files_in_Path = base.iterdir()
    for element in files_in_Path:
        if element.is_file():
            newFile = file(element.name,baseDir,0)
            baseDir.addChildren(newFile)
        elif element.is_dir():
            newDir = celv_importar(path+"/"+element.name)
            newDir.father = baseDir
            baseDir.addChildren(newDir)

    return baseDir

def imprimir_arbol(arbolito,tab,version = 0):
    if arbolito.safelock != None:
        print("safelock: " + str(arbolito.safelock.version))
    else: 
        print(arbolito.version)
    if arbolito.celv:
        if isinstance(arbolito, file):
            for i in range(0,tab):
                print(" ",end="")
            print(arbolito.name)
        elif isinstance(arbolito, directory):
            for i in range(0,tab):
                print(" ",end="")
            print("<DIR>",end="")
            print(arbolito.name)
            if arbolito.safelock != None and arbolito.safelock.children != -1 and arbolito.safelock.version <= version:
                print("aca?")      
                for element in arbolito.safelock.children:
                    imprimir_arbol(element,tab +5,version)
            else :
                print("aqui?") 
                for element in arbolito.children:
                    imprimir_arbol(element,tab +5,version)
                
    else:
        if isinstance(arbolito, file):
            for i in range(0,tab):
                print(" ",end="")
            print(arbolito.name)
        elif isinstance(arbolito, directory):
            for i in range(0,tab):
                print(" ",end="")
            print("<DIR>",end="")
            print(arbolito.name)
            for element in arbolito.children:
                imprimir_arbol(element,tab +5)

def updateTreeAdd(arbolito, newNode, versionIndex,version):
    global celvVersions
    global changeOnCicle

    if arbolito.safelock != None and arbolito.safelock.father!= -1 and arbolito.safelock.version <= version:
        if arbolito.safelock.father.safelock == None and isinstance(arbolito.safelock.father, directory):
            print("update 1.1")
            newDirectory = directory(arbolito.name,arbolito.safelock.father,arbolito.children,celvVersions[versionIndex].versionCount)
            newDirectory.celv = True
            newDirectory.celvIndex = celvVersions[versionIndex].id

            if arbolito.safelock.children != -1:
                newDirectory.children = arbolito.safelock.children

            newDirectory.addChildren(newNode)
            arbolito.safelock.father.changeSafelock(celvVersions[versionIndex].versionCount,-1,arbolito.safelock.father.children,-1)
            arbolito.safelock.father.safelock.children.remove(arbolito)
            arbolito.safelock.father.safelock.children.append(newDirectory)    

            updateChildrenCicle(newDirectory,versionIndex,version)

            return newDirectory

        elif arbolito.safelock.father.safelock != None and isinstance(arbolito.safelock.father, directory):
            print("update 1.2")
            newFather = directory(arbolito.safelock.father.name,arbolito.safelock.father.father,arbolito.safelock.father.children,celvVersions[versionIndex].versionCount)
            newFather.celv = True
            newFather.celvIndex = celvVersions[versionIndex].id

            if arbolito.safelock.father.safelock.children != -1 and arbolito.safelock.father.safelock.version <= version:
                newFather.children = arbolito.safelock.father.safelock.children
            
            if arbolito.safelock.father.safelock.father != -1 and arbolito.safelock.father.safelock.version <= version:
                newFather.father = arbolito.safelock.father.safelock.father

            newDirectory = directory(arbolito.name,newFather,arbolito.children,celvVersions[versionIndex].versionCount)
            newDirectory.celv = True
            newDirectory.celvIndex = celvVersions[versionIndex].id

            if arbolito.safelock.children != -1:
                newDirectory.children = arbolito.safelock.children

            newFather.children.remove(arbolito.name)
            newFather.children.append(newDirectory)
            newDirectory.addChildren(newNode)
            """
            print("CONSERVA SUS HIJOS DESPUES DE LA NUEVA CREACIÓN?")
            
            for element in newDirectory.children:
                print(element.name)
            """
            updateParents(arbolito.safelock.father,newFather,versionIndex,version)
            updateChildrenCicle(newDirectory,versionIndex,version)
            updateChildrenCicle(newFather,versionIndex,version)
        
            return newDirectory

    elif arbolito.father != None and arbolito.father.celv:
        if arbolito.father.safelock != None and isinstance(arbolito.father, directory):
            print("update 2.2")

            newFather = directory(arbolito.father.name,arbolito.father.father,arbolito.father.children,celvVersions[versionIndex].versionCount)
            newFather.celv = True
            newFather.celvIndex = celvVersions[versionIndex].id

            if arbolito.father.safelock.children != -1 and arbolito.father.safelock.version <= version:
                newFather.children = arbolito.father.safelock.children
            
            if arbolito.father.safelock.father != -1 and arbolito.father.safelock.version <= version:
                newFather.father = arbolito.father.safelock.father

            newDirectory = directory(arbolito.name,newFather,arbolito.children,celvVersions[versionIndex].versionCount)
            newDirectory.celv = True
            newDirectory.celvIndex = celvVersions[versionIndex].id

            if arbolito.safelock.children != -1 and arbolito.safelock.version <= version:
                newDirectory.children = arbolito.safelock.children
            
            if arbolito.safelock.father != -1 and arbolito.safelock.version <= version:
                newDirectory.father = arbolito.safelock.father

            newFather.children.remove(arbolito)
            newFather.children.append(newDirectory)
            newDirectory.addChildren(newNode)
            """
            print("CONSERVA SUS HIJOS DESPUES DE LA NUEVA CREACIÓN?")
            
            for element in newDirectory.children:
                print(element.name)
            """
            print(arbolito.father.name)
            print(type(arbolito.father.safelock))
            print("entro aca?")
            updateParents(arbolito.father,newFather,versionIndex,version)
            updateChildrenCicle(newDirectory,versionIndex,version)
            updateChildrenCicle(newFather,versionIndex,version)
        
            return newDirectory
            
        elif arbolito.father.safelock == None and isinstance(arbolito.father, directory):
            print("update 2.1")
            newDirectory = directory(arbolito.name,arbolito.father,arbolito.children,celvVersions[versionIndex].versionCount)
            newDirectory.celv = True
            newDirectory.celvIndex = celvVersions[versionIndex].id

            if arbolito.safelock.children != -1 and arbolito.safelock.version <= version:
                newDirectory.children = arbolito.safelock.children
            
            if arbolito.safelock.father != -1 and arbolito.safelock.version <= version:
                newDirectory.father = arbolito.safelock.father

            newDirectory.addChildren(newNode)
            arbolito.father.changeSafelock(celvVersions[versionIndex].versionCount,-1,arbolito.father.children,-1)
            arbolito.father.safelock.children.remove(arbolito)
            arbolito.father.safelock.children.append(newDirectory)    

            updateChildrenCicle(newDirectory,versionIndex,version)

            return newDirectory

    elif arbolito.father != None and (not arbolito.father.celv):
        print("update 3")
        newRoot = directory(arbolito.name,arbolito.father,arbolito.children,celvVersions[versionIndex].versionCount)
        newRoot.celv = True
        newRoot.celvIndex = celvVersions[versionIndex].id

        if arbolito.safelock.children != -1 and arbolito.safelock.version <= version:
            newRoot.children = arbolito.safelock.children
            
        if arbolito.safelock.father != -1 and arbolito.safelock.version <= version:
            newRoot.father = arbolito.safelock.father

        arbolito.father.children.remove(arbolito)
        arbolito.father.children.append(newRoot)
        newRoot.addChildren(newNode)
        celvVersions[versionIndex].addRoot(newRoot)

        updateChildrenCicle(newRoot,versionIndex,version)

        return newRoot

    elif arbolito.father == None:
        print("update 4")
        newRoot = directory(arbolito.name,arbolito.father,arbolito.children,celvVersions[versionIndex].versionCount)
        newRoot.celv = True
        newRoot.celvIndex = celvVersions[versionIndex].id

        if arbolito.safelock.children != -1 and arbolito.safelock.version <= version:
            newRoot.children = arbolito.safelock.children
            
        if arbolito.safelock.father != -1 and arbolito.safelock.version <= version:
            newRoot.father = arbolito.safelock.father

        newRoot.addChildren(newNode)
        celvVersions[versionIndex].addRoot(newRoot)

        updateChildrenCicle(newRoot,versionIndex,version)

        return newRoot
    
def updateChildren(hijo, padre,versionIndex,version):
    global celvVersions
    global changeOnCicle

    if hijo.safelock == None and hijo.version == celvVersions[versionIndex].versionCount:
        print("Entre")
        hijo.father = padre
    elif hijo.safelock == None and hijo.version <= version:
        print("Entre 1")
        hijo.changeSafelock(celvVersions[versionIndex].versionCount,padre,-1,-1)
    elif hijo.safelock != None and hijo.safelock.version == celvVersions[versionIndex].versionCount:
        print("Entre 2")
        hijo.safelock.father = padre
    elif hijo.safelock != None and hijo.safelock.version <= version:
        print("Entre 3")
        if isinstance(hijo,directory):
            newDirectory = directory(hijo.name,hijo.father,hijo.children,celvVersions[versionIndex].versionCount)
            newDirectory.celv = True
            newDirectory.celvIndex = celvVersions[versionIndex].id

            if hijo.safelock.children != -1:
                newDirectory.children = hijo.safelock.children
        
            if hijo.safelock.father != -1:
                newDirectory.father = hijo.safelock.father
            
            padre.children.remove(hijo)
            padre.children.append(newDirectory)

            updateChildrenCicle(newDirectory,versionIndex,version)
            changeOnCicle = True

        elif isinstance(hijo,file):
            newFile = file(hijo.name,hijo.father,celvVersions[versionIndex].versionCount)
            newFile.content = hijo.content
            newFile.celv = True
            newFile.celvIndex = celvVersions[versionIndex].id
            padre.children.remove(hijo)
            padre.children.append(newFile)
            changeOnCicle = True

def updateParents(padre, newPadre,versionIndex, version):
    global celvVersions
    print(newPadre.name)
    if padre.father!= None and (not padre.celv):
        print("Nueva Raiz 1")
        padre.father.children.remove(padre)
        padre.father.children.append(newPadre)

        celvVersions[versionIndex].addRoot(newPadre)

        updateChildrenCicle(newPadre,versionIndex,version)

    elif padre.father == None:
        print("Nueva Raiz 2")
        celvVersions[versionIndex].addRoot(newPadre)

        updateChildrenCicle(newPadre,versionIndex,version)

    elif padre.safelock !=None and padre.safelock.father != -1 and (padre.safelock.father.version == celvVersions[versionIndex].versionCount or padre.safelock.father.version <= version):
        print("Actualizar papa del Safe")
        if padre.safelock.father.safelock == None and padre.safelock.father.version == celvVersions[versionIndex].versionCount:
            padre.safelock.father.children.remove(padre)
            padre.safelock.father.children.append(newPadre)
        elif padre.safelock.father.safelock == None and padre.safelock.father.version <= version:
            padre.safelock.father.changeSafelock(celvVersions[versionIndex].versionCount,-1,padre.safelock.father.children,-1)
            padre.safelock.father.safelock.children.remove(padre)
            padre.safelock.father.safelock.children.append(newPadre)
        elif padre.safelock.father.safelock != None and padre.safelock.father.safelock.version == celvVersions[versionIndex].versionCount:
            padre.safelock.father.safelock.children.remove(padre)
            padre.safelock.father.safelock.children.append(newPadre)
        elif padre.safelock.father.safelock != None and padre.safelock.father.version <= version:
            newAbuelo = directory(padre.father.name,padre.father.father,padre.father.children,celvVersions[versionIndex].versionCount)
            newAbuelo.celv = True
            newAbuelo.celvIndex = celvVersions[versionIndex].id

            if padre.safelock.father.safelock.children != -1:
                newAbuelo.children = padre.safelock.father.safelock.children
            
            if padre.safelock.father.safelock.father != -1:
                newAbuelo.father = padre.safelock.father.safelock.father

            newAbuelo.children.remove(padre)
            newAbuelo.children.append(newPadre)

            updateChildrenCicle(newAbuelo,versionIndex,version)
            updateParents(padre.safelock.father, newAbuelo,versionIndex,version)

    elif padre.father!= None and padre.celv:
        print("Actualizar padre ori")
        if padre.father.safelock == None and padre.father.version == celvVersions[versionIndex].versionCount:
            print("opcion 1")
            padre.father.children.remove(padre)
            padre.father.children.append(newPadre)
        elif padre.father.safelock == None and padre.father.version <= version:
            print("opcion 2")
            padre.father.changeSafelock(celvVersions[versionIndex].versionCount,-1,padre.father.children,-1)
            padre.father.safelock.children.remove(padre)
            padre.father.safelock.children.append(newPadre)
        elif padre.father.safelock != None and padre.father.safelock.version == celvVersions[versionIndex].versionCount:
            print("opcion 3")
            padre.father.safelock.children.remove(padre)
            padre.father.safelock.children.append(newPadre)
        elif padre.father.safelock != None and padre.father.safelock.version <= version:
            print("opcion 4")
            newAbuelo = directory(padre.father.name,padre.father.father,padre.father.children,celvVersions[versionIndex].versionCount)
            newAbuelo.celv = True
            newAbuelo.celvIndex = celvVersions[versionIndex].id

            if padre.father.safelock.children != -1 and padre.father.safelock.version <= version:
                newAbuelo.children = padre.father.safelock.children
            
            if padre.father.safelock.father != -1 and padre.father.safelock.version <= version:
                newAbuelo.father = padre.father.safelock.father

            newAbuelo.children.remove(padre)
            newAbuelo.children.append(newPadre)

            updateChildrenCicle(newAbuelo,versionIndex,version)

            updateParents(padre.father, newAbuelo,versionIndex,version)

    

def print_hijos(arbolito):
    if isinstance(arbolito,directory):
        if arbolito.safelock != None and arbolito.safelock.children != -1:
            for element in arbolito.safelock.children:
                print("name:" + element.name + ", version:" + str(element.version))
        else:
            for element in arbolito.children:
                print("name:" + element.name + ", version:" + str(element.version))

def printSafelock(arbolito):

    print(arbolito.father.name)

    if arbolito.safelock != None:
        
        if arbolito.safelock.children != -1:
            print("Hijos")
            for element in arbolito.safelock.children:
                print(element.name)
        if arbolito.safelock.father != -1:
            print(arbolito.safelock.father.name)
        print(arbolito.safelock.version)

def updateChildrenCicle(padre,versionIndex,version):
    global changeOnCicle

    if padre.safelock != None and padre.safelock.children != -1:
        print("ciclo 1")
        while True:
            changeOnCicle = False
            for element in padre.safelock.children:
                updateChildren(element,padre,versionIndex,version)
                if changeOnCicle:
                    break
            if changeOnCicle == False:
                break
    elif padre.safelock == None:
        print("ciclo 2")
        while True:
            changeOnCicle = False
            for element in padre.children:
                updateChildren(element,padre,versionIndex,version)
                if changeOnCicle:
                    break
            if changeOnCicle == False:
                break