import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket

class SimpleGUI(QWidget):
    def _init_(self):
        super()._init_()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simple GUI')

        self.label = QLabel('Waiting for the number...', self)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)
        self.show()

        self.tcp_socket = QTcpSocket()
        self.tcp_socket.connected.connect(self.on_connected)
        self.tcp_socket.readyRead.connect(self.on_readyRead)
        self.tcp_socket.error.connect(self.on_error)

        # Connect to the Raspberry Pi's IP address and port
        self.tcp_socket.connectToHost('192.168.1.62', 5000)

    def on_connected(self):
        print('Connected to the Raspberry Pi.')

    def on_readyRead(self):
        # Read the received data from the socket
        data = self.tcp_socket.readAll().data().decode()

        # Update the label with the received number
        self.label.setText('Received number: ' + data)

    def on_error(self, socket_error):
        print('Socket error:', socket_error)

        # Close the socket
        self.tcp_socket.close()

if _name_ == '_main_':
    app = QApplication(sys.argv)
    gui = SimpleGUI()
    sys.exit(app.exec_())