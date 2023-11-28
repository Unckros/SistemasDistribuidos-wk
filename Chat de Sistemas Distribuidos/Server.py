import socket
import threading

clientes=[]

def main():
    
    socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        socketServer.bind(('' , 50000)) #subindo servidor 
        socketServer.listen() #deerminando a quantidade maxima de usuarios
        print("server ativo")
    except:
        socketServer.close() #entra no exept de ja houver um server na rede
        return print("Server ja iniciado")
    
    while True:    
        cliente, endereco = socketServer.accept() #aceitando conexões
        clientes.append(cliente) #adicionando clientes a lista de clientes do servidor
        #criando e iniciando a threads que da função menssagem 
        thread = threading.Thread(target=menssagem , args=[cliente])
        thread.start()  
                   
#função que faz o brodcast recebendo a menssagem de um cliente e enviando para dtodos conectados
def menssagem(cliente):
    while True:
        try: #tentando mandar menssagem
            msg = cliente.recv(2048)
            mandarMenssagem(cliente, msg)
        except: #se der erro remove o cliente que deu o erro por estar desconectado
            clientes.remove(cliente)
            break

def mandarMenssagem(cliente, msg):
    for clienteItem in clientes:
        if clienteItem != cliente:
            try:
                clienteItem.send(msg)
            except:
                clientes.remove(clienteItem)
                
                
def verificarServidor(HOST):
    for host in HOST:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)     
        try:
            client.connect((host, 50000))
            print("ja existe um serve na rede")
            return False
        except socket.timeout:
            client.close()
        except Exception as e:            
            client.close()
    else:
        client.close()
        return True
   
                
########################
#coloque o ip da sua maquina sem o ultimo digito e o inico e o fim para criar a faixa de rede
##########################
ip = '172.16.210.'
inicio = 0
fim = 35

ips= [] #lista que vai armazenar os ips 

#preenchendo a lista de ips
while inicio<=fim:
    aux_ip = ip 
    ips.append(aux_ip+str(inicio))
    inicio+=1

if verificarServidor(ips):
    print("conectado")
    main()

    