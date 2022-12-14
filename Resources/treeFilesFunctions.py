from Resources.directoryAndFile import directory, file, safelock
from pathlib import Path

celvRoots = []


def encontrar_nombre(arbolito,name):
    if isinstance(arbolito, directory):
        for element in arbolito.children:
            if isinstance(element, directory):

                if element.name == name:
                    raise NameError
                encontrar_nombre(element,name)

            elif isinstance(element, file):
                if element.name == name:
                    raise NameError

    elif isinstance(arbolito, file):
        if arbolito.name == name:
            raise NameError

def crear_dir(arbolito,name):
    encontrar_nombre(arbolito,name)
    
    if isinstance(arbolito,directory):
        newChild = directory(name,arbolito,[],0)
        arbolito.addChildren(newChild)
    else:
        raise Exception

def crear_archivo(arbolito,name):
    encontrar_nombre(arbolito,name)
    if isinstance(arbolito,directory):
        newChild = file(name,arbolito,0)
        arbolito.addChildren(newChild)
    else:
        raise Exception

def escribir(arbolito, name, content):
    if isinstance(arbolito, directory):
        for element in arbolito.children:
            if isinstance(element, directory):
                try:
                    writed = escribir(element,name,content)
                    if writed == 0:
                        return 0
                except:
                    pass
            elif isinstance(element, file):
                if element.name == name:
                    element.content = content
                    return 0
    elif isinstance(arbolito, file):
        if arbolito.name == name:
            arbolito.content = content
            return 0
    raise FileNotFoundError


def eliminar(arbolito, name):
    if isinstance(arbolito, directory):
        for element in arbolito.children:
            if isinstance(element, directory):
                if element.name == name:
                    arbolito.deleteChildren(element)
                    return 0
                else:
                    try:
                        deleted = eliminar(element,name)
                        if deleted == 0:
                            return 0
                    except:
                        pass
            elif isinstance(element, file):
                if element.name == name:
                    arbolito.deleteChildren(element)
                    return 0

    raise FileExistsError

def leer(arbolito,name):
    if isinstance(arbolito, directory):
        for element in arbolito.children:
            if isinstance(element, directory):
                try:
                    printed = leer(element,name)
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

def ir(arbolito,name):
    if name == "":
        if arbolito.father == None:
            print("Error: Ya se encuentra en la Raiz del arbol")
            raise ReferenceError

        return arbolito.father
    else:
        if isinstance(arbolito, directory):
            for element in arbolito.children:
                if element.name == name:
                    return element
            print("Error: Nombre no encontrado!!")
            raise NameError

def celv_importar(path):

    base = Path(path)

    if (not base.exists()) or (not base.is_dir()):
        raise FileNotFoundError


    baseDir = directory(base.name,None,[],None)


    files_in_Path = base.iterdir()
    for element in files_in_Path:
        if element.is_file():
            newFile = file(element.name,baseDir,None)
            baseDir.addChildren(newFile)
        elif element.is_dir():
            newDir = celv_importar(path+"/"+element.name)
            newDir.father = baseDir
            baseDir.addChildren(newDir)

    return baseDir

def imprimir_arbol(arbolito,tab):
    
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