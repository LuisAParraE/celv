import re
from Resources import treeFilesFunctions as tree

def main():
    print("")
    print("Bienvenidos a..... Como era la cosa?\n")
    print("Ah cierto, un manejador de versiones de archivos")
    print("Puedes Crear Directorios, archivos asi como eliminarlos")
    print("Si desea saber los comandos a usar escriba 'help' en el repl")
    arbolito = None

    p = re.compile('^crear_dir\((\S)+\)$')
    p1 = re.compile('^crear_archivo\((\S)+\)$')
    p2 = re.compile('^eliminar\((\S)+\)$')
    p3 = re.compile('^leer\((\S)+\)$')
    p4 = re.compile('^escribir\((\S)+,[(\s)(\S)]+\)$')
    p5 = re.compile('^ir\((\S)*\)$')
    p6 = re.compile('^help$')
    p7 = re.compile('^imprimir$')
    p8 = re.compile('^salir$')
    p9 = re.compile('^celv_importar\((\S)+\)$')

    path = "/"
    while True:
        
        option = input(path+"> ")
        if p.match(option):
            try:
                tree.crear_dir(arbolito,option[10:-1])
            except:
                print('Error: Nombre ya en uso!!')
        elif p1.match(option):
            try:
                tree.crear_archivo(arbolito,option[14:-1])
            except:
                print('Error: Nombre ya en uso!!')
        elif p2.match(option):
            try:
                tree.eliminar(arbolito,option[9:-1])
            except:
                print('Error: Archivo No existe!!')
        elif p3.match(option):

            try:
                tree.leer(arbolito,option[5:-1])
            except:
                print('Error: Archivo No existe!!')

        elif p4.match(option):

            token = option[9:-1].split(",")
            try:
                tree.escribir(arbolito,token[0],token[1])
            except:
                print('Error: Archivo No existe!!')

        elif p5.match(option):

            try:
                arbolito = tree.ir(arbolito,option[3:-1])
            except:
                pass
            
        elif p6.match(option):

            print("Los comandos existentes son:")
            print("--crear_dir(<nombre>) , es usado para crear un directorio\n")
            print("--crear_archivo(<nombre>) , es usado para crear un archivo\n")
            print("--eliminar(<nombre>) , es usado para eliminar archivo o directorio, si elige un directorio borrara todo lo que tenga dentro de manera recursiva\n")
            print("--leer(<nombre>) , es usado para mostrar el contenido de un archivo\n")
            print("--escribir(<nombre>,<contenido>) , es usado para escribir el contenido en un archivo\n")
            print("--ir(<nombre>) , es usado para ir a un directorio hijo de donde se encuentra. Si no se coloca un nombre, se va al padre del directorio actual\n")
            print("--help , es usado para mostrar los comandos disponibles\n")
            print("--imprimir , es usado para imprimir de manera recursiva los directorios y sus archivos\n")
            print("--salir , es usado para salir del repl\n")
            
        elif p7.match(option):

            tree.imprimir_arbol(arbolito,0)

        elif p8.match(option):
            break
        elif p9.match(option):

            arbolito = tree.celv_importar(option[14:-1])

        else:
            print("No se encontró la instrucción, coloque 'help' para ver los comandos disponibles")



main()