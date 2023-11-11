#!/usr/bin/env python
import socket
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton, QLabel, QMenuBar, QAction, QMenu, QInputDialog
from PyQt5.QtCore import QTimer
import logging

logging.basicConfig(filename='log.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.HOST = '0.0.0.0'
        self.PORT = 12345

        self.is_server = False
        self.start_time = time.time()
        self.username = ""

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.initUI()

    def initUI(self):
        self.server_label = QLabel("Servidor: Nenhum")
        self.runtime_label = QLabel("Tempo de Execução: 0 segundos")

        self.menu_bar = self.menuBar()
        self.config_menu = self.menu_bar.addMenu("Configuração")

        self.name_action = QAction("Nome", self)
        self.name_action.triggered.connect(self.set_name)
        self.config_menu.addAction(self.name_action)

        self.ip_action = QAction("Endereço IP de Destino", self)
        self.ip_action.triggered.connect(self.set_ip)
        self.config_menu.addAction(self.ip_action)

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
        layout.addWidget(self.messages)
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_input)
        layout.addWidget(self.send_button)

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
        username = self.username or self.HOST
        self.sock.sendto(f"{username}: {message}".encode(), (self.HOST, self.PORT))
        self.message_input.clear()
        logging.info(f"{username}: {message}")

    def receive_messages(self):
        while True:
            data, addr = self.sock.recvfrom(1024)
            message = data.decode()
            self.messages.append(message)
            logging.info(message)

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

    def set_name(self):
        text, ok = QInputDialog.getText(self, "Nome", "Digite seu nome:")
        if ok and text:
            self.username = text

    def set_ip(self):
        text, ok = QInputDialog.getText(self, "Endereço IP de Destino", "Digite o endereço IP de destino (Opcional):")
        if ok:
            self.HOST = text

def main():
    app = QApplication([])
    chat_app = ChatApp()
    app.exec_()

if __name__ == '__main__':
    main()

