'''

AUTORA: EVELYN TABARES VALENCIA 


'''

from fileinput import filename
from tabulate import tabulate

#Compara dos binarios y busca la posición de la diferencia
def compara_binarios(s1,s2):
    count = 0
    pos = 0
    
    for i in range(len(s1)): 
        if s1[i] != s2[i]:
            count+=1
            pos = i
    if count == 1:
        return True, pos# Retorna la posición de la diferencia en 'pos'
    else:
        return False, None



#Combina pares y hace un nuevo grupo
def combinar_pares(grupo, desmarcado):
    #define longitud
    l = len(grupo)-1

    #check list
    lista_verificacion = []
     
   #nuevo grupo
    siguiente_grupo = [[] for x in range(l)]
   
    #Comenzamos la impresión de la agrupación de primos
    print("\n\n\n")
    print('='*65)
    print("\n  Número de Grupo.  \tMintérminos\t\tExpresión en BCD\n%s"%('='*65))
    #Pasa por cada grupo
    for i in range(l): #Ciclo para recorrer todos los grupos de la lista y comparlos;selecciona las filas
        contar = True # Solo es verdadero al cambiar de número de grupo 
        for w  in range (len (grupo[i])): #Ciclo para seleccionar cada elemento de la fila "i" del primer grupo i;[[elm1][elm2]]
            
            for x in range(len(grupo[i+1])):#Ciclo para seleccionar  cada elemento de la fila "i" del grupo i+2
                
                b, pos = compara_binarios(list(map(str,grupo[i][w][1])),list(map(str,grupo[i+1][x][1]))) #Compara los binarios;retorna la posicion del cambio
                if b == True:#Si los binarios se pueden combinar
                
                    #Agregamos los elementos usados en lista comprobada
                    lista_verificacion.append(grupo[i][w][1])   
                    lista_verificacion.append(grupo[i+1][x][1]) 
                                    
                    #Reemplaza el bit diferente con '-'  
                    nuevo_elemento = list(map(str,grupo[i][w][1]))#genera una lista con cada digito de elem1 en binario ['1','0','1','1']
                                    
                    nuevo_elemento[pos] = '-'  #Reemplaza el digito anterior con '-'; según la posición retornada por compara_binarios
                    nuevo_elemento = "".join(nuevo_elemento)# Se convierte en string  
                    nuevo_dec=grupo[i][w][0]+ " "+ grupo[i+1][x][0] #Agrega a la lista la representación decimal de ambos binarios que se combinaron
                    siguiente_grupo[i].append([ str(nuevo_dec),nuevo_elemento]) #Almacena el nuevo binario combinado, con su representación decimal
                     
                    if contar== True :#Solo se valida 1 vez hasta que se ejecute de nuevo el for principal; es decir, se cambie de grupo 
                        print('-'*65)  
                        print("%8d,%d  "%(i,i+1)) #Imprime el número de ambos grupos que se combinan  
                        contar = False   
                    print( "\t\t\t %s, %-18s"%(grupo[i][w][0], grupo[i+1][x][0]), end=" ")#Imprime números decimales que forman el grupo
                    print("  ", nuevo_elemento)  #el nuevo binario con los cambios 
   #lista de primos                                            
    for i in range(len(grupo)):#Recorremos cada grupo en busca de los binarios que no se combinaron
        for j in range (len(grupo[i])):
            if grupo[i][j][1] not in lista_verificacion: #El binario no se combinó
                desmarcado.append([grupo[i][j][0] ,grupo[i][j][1]]) # Se agrega a lista de números que no se combinaron 

    return siguiente_grupo, desmarcado  #Retorna el grupo de numeros combinados con cambios y lista de números que no se combinaron (primer implicantes)
  
#Remueve los minterminos redundantes de la segunda lista
def eliminar_redundantes(grupo):
    nuevo_grupo = []
    for j in grupo: #filas: Selecciona un grupo  [7 15 , -111]  [11 15 , 1-11]  
        nuevo=[]
        for i in j:#Columna: selecciona cada termnino del grupo [7 15 , -111]
            if i not in nuevo:#Si el termino no está en la lista nueva
                nuevo.append(i) #se agrega a la lista [7 15 , -111] 
        nuevo_grupo.append(nuevo)#Se agregan los elementos sin repeticiones a la nueva lista
    return nuevo_grupo # Retorna lista sin elementos repetidos


#Remueve primos redundantes de la lista de primos implicantes
def eliminar_redundantes_list(list):
    nueva_lista = []
    lista_guardar= []
    for i in range(len(list)): #filas: cada primo
        if list[i][1] not in nueva_lista: # busca que el primo no esté en la lista
            nueva_lista.append(list[i][1])# agrega el primo a la lista
            lista_guardar.append([list[i][0],list[i][1]])# Esta lista guarda tanto el primo como su representación binaria
    return lista_guardar# Retorna lista sin duplicados 


#Devuelve verdadero si está vacío
def comprobar_vacia(grupo):

    if len(grupo) == 0:
        return True
    else:
        count = 0
        for i in grupo:#hay elementos en la lista, entra al ciclo
            if i:
                count+=1#el contador aumenta
        if count == 0:#No hay elementos en la lista
            return True
    return False


#imprimir el código binario a letra
def binario_a_letras(s):#[1,0,0,0] ->  AB'C'D'
    out = ''
    c = 'A'
    more = False
    n = 0
    for i in range(len(s)):
        
        if s[i] == '1':#Si el binario es 1
            out = out + c
        elif s[i] == '0':#si el binario es 0, niega la letra con ' \' '
            out = out + c+'\''
        #cambio de variable
        c = chr(ord(c)+1) #'ord()' Recibe la letra y devuelve su representacion en unicode A=65+1-> B=66 
                              #chr(ord()) Recibe un número y devuelve su representación como carácter
                              # 65 66 67 68 69 ....
                              # A  B  C   D  E
    return out

def tabla_verificacion(primos,a):
    #---------------TABLA DE VERIFICACIÓN-----------------
    #Separación de minterminos según el primo en el que aparecen 
    decimales = [[] for x in range(len(primos))]#lista de minterminos en decimal, los cuales crearon el primo
    for x in range(len(primos)):
        decimales[x]= primos[x][0].split()#pone cada mintermino por separado, como un elemento de la lista ['4 5']--> ['4', '5']
        
    #Creación de encabezado de la tabla: Expresiones y minterminos
    tabla=[[0 for i in range(len(a)+1)] for j in range(len(primos)+1)] #Tabla de verificación fila: #primos(primos) ; columna:#minterminos(a) 
    tabla[0][0]= "Expresiones" 
    for x in range(len(a)):
        tabla[0][x+1]=  str(int(a[x],2))#Asignando todos los minterminos a la fila 0
    #LLenando la tabla 
    for w in range(len(decimales)):#fila: cantidad de expresiones resultantes de primos
        tabla[w+1][0]= binario_a_letras(list(map(str,primos[w][1])))#Se guarda en la tabla la representacion del primo
        for z in range(len(a)): #columna de minterminos
            if  str(int(a[z],2)) in decimales[w] : #Si el mintermino se encuentra en la lista de decimales del primo
                tabla[w+1][z+1]= 'X'  #Se coloca una X en la posición. Indica que el primo de esa fila está conformado por dicho decimal 
            else:
                tabla[w+1][z+1]= ' '# espacio vacio si el mintermino no conforma el primo
    print("\t TABLA DE VALIDACIÓN")
    print(tabulate(tabla))#Imprime la tabla de manera que filas y columnas coincidan, usando  'tabulate'
    
    #------PRIMOS IMPLICANTES ESENCIALES 
    temp=0#Almacena temporalmente una fila
    contmin=0#Contador de minterminos que comparten los primos
    valido=[] #Almacenará las expresiones validas
    
    #Buscar primos validos
    for j in range(len(a)):#columnas
        for i in range(len(tabla)):#filas; Recorremos una sola columna y cada una de sus filas 
            if tabla[i][j] == 'X':#Si el mintermino(columna) pertenece a un primo
               temp= i-1# Almacena la fila donde se encuentra la 'X'. La tabla tiene un indice de más para el encabezado. Entonces i-1
               contmin += 1 
        #El primo es valido si sus minterminos no se encunetran en otro primo
        if contmin == 1 and (primos[temp][1] not in valido):# Se excluye el primo que ya se haya agregado a la lista de validos
            valido.append(primos[temp][1])# Almancenamos la expresión valida en la lista 
        contmin = 0
    
    #Buscar entre los invalidos alguno que pueda ser valido 
    cont_valido=0
    cont_inval=0
    fila_exp =0
    temp_inval=[]#almacena las filas de los invalidos
    invalido=[]
    for j in range(len(a)):#columnas
        for i in range(len(tabla)):#filas; Recorremos una sola columna y cada una de sus filas 
            if tabla[i][j] == 'X':#Si el mintermino(columna) pertenece a un primo
                if primos[i-1][1] in valido: # si es un primo válido 
                    cont_valido+=1
                else :#Si es un primo invalido el que tiene la X 
                    cont_inval+=1 #Contador de expresiones inválidas 
                    temp_inval.append(i-1)# Guardamos en la lista las filas donde encontramos los terminos invalidos
        if cont_valido >= 1 and cont_inval >=1 :#Se convierten en invalidos las expresiones que se relacionan con al menos un valido
             for z in range(len(temp_inval)): 
                 invalido.append( primos[int(temp_inval[z])][1])#Se almacena en la lista de invalidos, aquellos que no están en la lista de validos
                 if primos[fila_exp][1] in valido and primos[fila_exp][1] in invalido:#Si la expresión existe en ambas tablas 
                    valido.remove(primos[fila_exp][1])#Se remueve de los terminos validos
                    
        elif cont_valido == 0 and cont_inval >= 1: #Las expresiones que solo se relacionan con invalidos, se convierten en validos
            for z in range(len(temp_inval)): #Recorremos la lista de temp_inval, para extraer los indices de las filas/primo
                
                if primos[int(temp_inval[z])][1] not in invalido:#Si la expresión/primo no existe en la lista de invalidos 
                    fila_exp = int(temp_inval[z])
                    valido.append(primos[fila_exp][1])#Agregamos la expresión a la lista de validos
                    
                if primos[fila_exp][1] in valido and primos[fila_exp][1] in invalido:#Si la expresión existe en ambas listas
                    valido.remove(primos[fila_exp][1])#Se remueve de los terminos validos
        temp_inval = []
        cont_valido = 0
        cont_inval=0
    return valido  #Retorna lista de las expresiones validas en binario

#main function
def main():
    print("\t","_"*50," \n\t|     MÉTODO DE MINIMIZACIÓN QUINE-McCLUSKEY.       |\n\t|","_"*49,"|\n" )    
    # obtener el numero de variables(bits del numero binario)
    #n_var = int(input("\t Ingrese el número de variables: "))
    ##Obtener los minterms como entrada
    minterms = input("\t Ingrese los minterminos (Ej. 0 1 2 5 9 10) : ")
    a = minterms.split() # lista con cada minterm separado ['0','2']
    #poner los números en la lista en forma int
    a = sorted(list(map(int, a )))#'map(,) convierte strings a numeros, sorted ordenar de menor a mayor los numeros
    #make a grupo list
    num_a = sorted(list(map(int, a )))
    for i in range(len(num_a)): #recorre la lista de minterminos de menor a mayor 
        #convierte a binario
        num_a[i] = bin(num_a[i])[2:] 
        n_var= len(num_a[i])#se mide la longitud del binario ingresado 
    #n_var -> La longitud del mintermino mayor en binario
    grupo = [[] for z in range(n_var+1)]
     #Comenzamos la impresión de la agrupación primaria
    print("\n\n\n")
    print('='*65)
    print("\n  Número de Gpo.  \tMintérminos\t\tExpresión en BCD\n%s"%('='*65))
    
    for i in range(len(a)): 
        #convierte a binario
        a[i] = bin(a[i])[2:]  
   
        if len(a[i]) < n_var:
            #Agrega ceros para llenar los n-bits
            for j in range(n_var - len(a[i])): #for que rellena con ceros a la izquierda el binario
                a[i] = '0'+ a[i]   
        #if incorrect input
        elif len(a[i]) > n_var: 
            print ('\nError : Escoja el número correcto de variables(bits)\n')
            return    
        #contar el numero de unos, que hay en un binario 
        index = a[i].count('1')  
        #agrupar según la cantidad de '1' presente en el binario
        
        grupo[index].append([ str( int(a[i],2)), a[i]])#Se guarda una lista dentro de la lista
        #La lista agregada a 'grupo' contiene -> [str(decimal), binario]
        
        
    #Imprimir primera tabla
    for i in range(len(grupo)): #Ciclo para imprimir tablas
       if grupo[i] != [] : #Se excluye la lista a la que no se le han asignado binarios 
            print("  %5d:"%i)  # Imprime el número de grupo (número de '1' que contiene el binario)
       cont=0
       for j in range(len(grupo[i])):# [5 , 0101]
           for z in range(len(grupo[i][j])): 
                  if cont==0: 
                      print( "\t\t\t     %-20s "%(grupo[i][j][z]), end=" ")#Imprime los minterminos
                      cont+=1
                  else:
                       print("  ", grupo[i][j][z])#imprime los minterminos en binarios
           cont =0
       print('-'*65)
       
    #Combinar los pares en series hasta que nada nuevo pueda ser combinado         
    desmarcado = [] #Tabla en la que almacenaremos los primos   
    while comprobar_vacia(grupo) == False:#Mientras la grupo no está vacío
        siguiente_grupo, desmarcado = combinar_pares(grupo,desmarcado)#Combinacion de pares
        grupo = eliminar_redundantes(siguiente_grupo)#Remueve los terminos redundantes 
       
    primos=eliminar_redundantes_list(desmarcado)#Se remueven los elementos repetidos de la lista de desmarcado: primos 
  
    s = "\n| PRIMOS IMPLICANTES | :\n\n  "
    cont_guion=0
    if len(primos) == 1: # Solo existe un grupo combinado
        numer=  primos[0][1].split()
        for z in range(len(numer)):
           cont_guion= numer[z].count("-")
        if cont_guion == n_var: # la cantidad de cambios en el elemento combinado es igual al numero de variables 
          print(s,"1") #Se han realizado combinaciones con todos los minterminos ingresados 
    else:
        for k in range(len(primos)):
            s= s + binario_a_letras(list(map(str,primos[k][1]))) + " + "
        print (s[:(len(s)-3)], "\n\n")
        

    cad = "\n| PRIMOS IMPLICANTES ESENCIALES |:\n\n   "
    
    valido = tabla_verificacion(primos,a)# Creacion de tabla de verificación; retorna los primos implicantes esenciales
    if  cont_guion == n_var: # la cantidad de cambios en el elemento combinado es igual al numero de variables 
          print(cad,"1") #Se han realizado combinaciones con todos los minterminos ingresados 
    else :
        for k in range(len(valido)):
          cad= cad + binario_a_letras(list(map(str,valido[k]))) + " + "
        print (cad[:(len(cad)-3)],"\n")
    
if __name__ == "__main__":
    main()