import sys
import socket
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtCore import QTimer


class JanelaChat(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializarUI()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ehServidor = False
        self.clientes = []
        self.porta_padrao_servidor = 1234
        self.ip_local = self.obter_ip_local()
        self.timestamp_conexao = None
        self.iniciar_como_cliente()

    def inicializarUI(self):
        self.setWindowTitle("Aplicativo de Chat")
        self.setGeometry(100, 100, 400, 500)

        layout = QVBoxLayout()

        self.rotuloStatus = QLabel("Status: Iniciando...")
        layout.addWidget(self.rotuloStatus)

        self.rotuloHoraAtual = QLabel("Hora Atual: " + time.strftime("%H:%M:%S", time.localtime()))
        layout.addWidget(self.rotuloHoraAtual)

        self.caixaChat = QTextEdit()
        self.caixaChat.setReadOnly(True)
        layout.addWidget(self.caixaChat)

        self.caixaMensagem = QLineEdit()
        layout.addWidget(self.caixaMensagem)

        self.botaoEnviar = QPushButton("Enviar", self)
        self.botaoEnviar.clicked.connect(self.enviar_mensagem)
        layout.addWidget(self.botaoEnviar)

        self.setLayout(layout)

        # Timer para atualizar o rótulo da hora
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_hora)
        self.timer.start(1000)

    def atualizar_hora(self):
        self.rotuloHoraAtual.setText("Hora Atual: " + time.strftime("%H:%M:%S", time.localtime()))

    def obter_ip_local(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def iniciar_como_cliente(self):
        self.timestamp_conexao = time.time()
        try:
            self.socket.connect((self.ip_local, self.porta_padrao_servidor))
            self.rotuloStatus.setText("Status: Conectado como Cliente")
            self.caixaChat.append("Conectado ao servidor.")
            threading.Thread(target=self.receber_mensagem).start()
        except:
            self.iniciar_como_servidor()

    def iniciar_como_servidor(self):
        self.ehServidor = True
        self.clientes = []
        self.timestamp_conexao = time.time()
        try:
            self.socket.bind((self.ip_local, self.porta_padrao_servidor))
            self.socket.listen(5)
            self.rotuloStatus.setText("Status: Funcionando como Servidor")
            self.caixaChat.append("Nenhum servidor encontrado. Atuando como servidor...")
            threading.Thread(target=self.aceitar_conexoes).start()
        except OSError as e:
            self.rotuloStatus.setText("Status: Falha ao iniciar servidor")
            self.caixaChat.append(f"Falha ao iniciar servidor: {e}")

    def aceitar_conexoes(self):
        while self.ehServidor:
            cliente, endereco = self.socket.accept()
            self.clientes.append(cliente)
            self.caixaChat.append("Cliente conectado: {}".format(endereco))
            threading.Thread(target=self.manipular_cliente, args=(cliente,)).start()

    def manipular_cliente(self, cliente):
        while True:
            try:
                mensagem = cliente.recv(1024).decode()
                horario = time.strftime("%H:%M:%S", time.localtime())
                mensagem_formatada = "[{}] {}".format(horario, mensagem)
                self.retransmitir(mensagem_formatada)
            except:
                cliente.close()
                self.clientes.remove(cliente)
                break

    def retransmitir(self, mensagem):
        self.caixaChat.append(mensagem)
        for cliente in self.clientes:
            try:
                cliente.send(mensagem.encode())
            except:
                cliente.close()
                self.clientes.remove(cliente)

    def enviar_mensagem(self):
        mensagem = self.caixaMensagem.text()
        horario = time.strftime("%H:%M:%S", time.localtime())
        mensagem_formatada = "[{}] Você: {}".format(horario, mensagem)
        self.caixaChat.append(mensagem_formatada)
        if self.ehServidor:
            self.retransmitir(mensagem_formatada)
        else:
            self.socket.send(mensagem.encode())
        self.caixaMensagem.clear()

    def receber_mensagem(self):
        while not self.ehServidor:
            try:
                mensagem = self.socket.recv(1024).decode()
                self.caixaChat.append(mensagem)
            except:
                self.socket.close()
                self.verificar_e_tornar_servidor()
                break

    def verificar_e_tornar_servidor(self):
        # Aguarda um momento para dar tempo aos outros clientes se tornarem servidores
        time.sleep(2)
        tentativa = self.socket.connect_ex((self.ip_local, self.porta_padrao_servidor))
        if tentativa != 0:
            if not self.ehServidor:
                print("Tornando-se servidor...")
                self.iniciar_como_servidor()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaChat()
    janela.show()
    sys.exit(app.exec_())
