#!/usr/bin/env python3
import socket
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import QTimer

class ChatApp(QMainWindow):
    def __init__(self):
        super(ChatApp, self).__init__()

        self.HOST = '127.0.0.1'  # Use um endereço IP válido
        self.PORT = 12345  # Use uma porta válida

        self.is_server = False
        self.start_time = time.time()
        self.username = ""  # Nome de usuário padrão vazio

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.HOST, self.PORT))

        self.initUI()

    def initUI(self):
        self.server_label = QLabel("Servidor: Nenhum")
        self.runtime_label = QLabel("Tempo de Execução: 0 segundos")
        self.username_label = QLabel("Nome:")
        self.username_input = QLineEdit(self)
        self.username_input.setText(self.username)
        self.username_input.editingFinished.connect(self.update_username)

        self.network_label = QLabel("Faixa de Rede:")
        self.network_input = QLineEdit(self)
        self.network_input.setText(self.HOST)
        self.port_label = QLabel("Porta:")
        self.port_input = QLineEdit(self)
        self.port_input.setText(str(self.PORT))

        self.messages = QTextEdit(self)
        self.messages.setReadOnly(True)
        self.messages.setVerticalScrollBarPolicy(0)

        self.message_label = QLabel("Mensagem:")
        self.message_input = QLineEdit(self)

        self.send_button = QPushButton('Enviar', self)
        self.send_button.clicked.connect(self.send_message)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.server_label)
        layout.addWidget(self.runtime_label)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.network_label)
        layout.addWidget(self.network_input)
        layout.addWidget(self.port_label)
        layout.addWidget(self.port_input)
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)
        layout.addWidget(self.messages)

        central_widget.setLayout(layout)

        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()

        self.check_server_thread = threading.Thread(target=self.check_server)
        self.check_server_thread.start()

        self.update_ui_timer = QTimer(self)
        self.update_ui_timer.timeout.connect(self.update_ui)
        self.update_ui_timer.start(1000)

        self.setGeometry(100, 100, 400, 400)
        self.setWindowTitle('Chat App')
        self.show()

    def send_message(self):
        message = self.message_input.text()
        username = self.username or self.HOST  # Use o nome de usuário ou o endereço IP
        self.sock.sendto(f"{username}: {message}".encode(), (self.HOST, self.PORT))
        self.message_input.clear()

    def receive_messages(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = data.decode()
            self.messages.append(message)

    def check_server(self):
        while True:
            if not self.is_server:
                data, addr = self.sock.recvfrom(1024)
                timestamp = float(data.decode())
                if timestamp < self.start_time:
                    self.is_server = True
                    self.start_time = time.time()

    def update_ui(self):
        if self.is_server:
            self.server_label.setText("Servidor: Este Host")
        else:
            self.server_label.setText("Servidor: Outro Host")

        runtime = int(time.time() - self.start_time)
        self.runtime_label.setText(f"Tempo de Execução: {runtime} segundos")

    def update_username(self):
        self.username = self.username_input.text()

    def update_network(self):
        network = self.network_input.text()
        if self.is_valid_network(network):
            self.HOST = network

    def is_valid_network(self, network):
        try:
            ipaddress.ip_network(network, strict=False)
            return True
        except ValueError:
            return False

def main():
    app = QApplication([])
    chat_app = ChatApp()
    app.exec_()

if __name__ == '__main__':
    main()
