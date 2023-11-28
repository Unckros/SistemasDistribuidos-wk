import socket
import threading
 
def main(HOST):

    try:
        host = conectar(HOST)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, 50000))
    except:
        return "erro"

    username = input('Usuário> ') #nome do usario para indentificar no chat
    print('\nConectado')

    #criando e iniciando as threads que irão manter as funcioes de receber e enviar menssagens executanto 
    thread1 = threading.Thread(target=receberMenssagem, args=[client]) 
    thread2 = threading.Thread(target=enviarMenssagem, args=[client, username])

    thread1.start()
    thread2.start()


def receberMenssagem(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
            

def enviarMenssagem(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return
        
def conectar(HOST):  
    for host in HOST:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.1)
        try:
            client.connect((host, 50000))
            print(f'Conectado com sucesso ao host {host}')
            return host
        except socket.timeout:
            print(f'Tempo limite excedido para o host {host}')
            client.close()
        except Exception as e:
            print(f'Erro ao conectar ao host {host}: {e}')
            client.close()
    else:
        client.close()
        print('erro de conexão')
        return host


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
    
main(ips)


    


