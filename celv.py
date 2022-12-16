import re
from Resources import treeFilesFunctions as tree

def main():
    print("")
    print("Bienvenidos a..... Como era la cosa?\n")
    print("Ah cierto, un manejador de versiones de archivos")
    print("Puedes Crear Directorios, archivos asi como eliminarlos")
    print("Si desea saber los comandos a usar escriba 'help' en el repl")
    
    arbolito = None
    version = 0

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
    p10 = re.compile('^celv_iniciar\(\)$')
    p11 = re.compile('^celv_vamos\((\d)+\)$')
    p12 = re.compile('^pwd$')
    p13 = re.compile('^celv_historia\(\)$')
    p20 = re.compile('^hijos\(\)$')
    p21 = re.compile('^version$')
    p22 = re.compile('^safe$')

    path = "/"
    while True:
        
        option = input(path+"> ")
        if p.match(option):
            try:
                [arbolito,version] = tree.crear_dir(arbolito,option[10:-1],version)
            except:
                print('Error: Nombre ya en uso!!')
        elif p1.match(option):
            try:
                [arbolito,version] = tree.crear_archivo(arbolito,option[14:-1],version)
            except:
                print('Error: Nombre ya en uso!!')
        elif p2.match(option):
            print(option[9:-1])
            try:
                [arbolito,version] = tree.eliminar(arbolito,option[9:-1],version)
            except:
                print('Error: Archivo No existe!!')
        elif p3.match(option):

            try:
                tree.leer(arbolito,option[5:-1],version)
            except:
                print('Error: Archivo No existe!!')

        elif p4.match(option):

            token = option[9:-1].split(",")
            try:
                [arbolito,version] = tree.escribir(arbolito,token[0],token[1],version)
            except:
                print('Error: Archivo No existe!!')

        elif p5.match(option):
            try:
                [arbolito,version] = tree.ir(arbolito,option[3:-1],version)
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
            print("--pwd , es usado para saber tu posicion en el arbol.\n")
            print("--version , es usado para saber la version actual en la que se encuentra.\n")
            print("--imprimir , es usado para imprimir de manera recursiva los directorios y sus archivos\n")
            print("--celv_iniciar() , es usado para inicializar el arbol de versiones desde el nodo invocado, si ya esta inicializado dara error.\n")
            print("--celv_historia() , es usado para mostrar los cambios realizados en el arbol de persistencia.\n")
            print("--celv_importar(<Dirección>) , es usado para importar de manera recursiva una dirección de tu PC a memoria, para poblar el arbol.\n")
            print("--celv_vamos(<nro>) , es usado para viajar a alguna version del arbol, siempre y cuando ya se haya inicializado.\n")
            print("--salir , es usado para salir del repl\n")
            
        elif p7.match(option):
            tree.imprimir_arbol(arbolito,0,version)

        elif p8.match(option):
            break
        elif p9.match(option):

            arbolito = tree.celv_importar(option[14:-1])

        elif p10.match(option):

            tree.celv_iniciar(arbolito)

        elif p11.match(option):
        
            [arbolito,version]=tree.celv_vamos(arbolito,int(option[11:-1]))

        elif p12.match(option):
            try:
                tree.pwd(arbolito,version)
            except:
                print("Arbol No Generado")

        elif p13.match(option):
            try:
                tree.celv_historia(arbolito)
            except:
                print("Arbol No Inicializado")
        elif p20.match(option):

            tree.print_hijos(arbolito)

        elif p21.match(option):

            print(version)

        elif p22.match(option):

            tree.printSafelock(arbolito)

        else:
            print("No se encontró la instrucción, coloque 'help' para ver los comandos disponibles")


main()