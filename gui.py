from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from finn_alle_sider import  find_urlfragment, get_sitemap
# Only needed for access to command line arguments
import sys



class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        
        self.setWindowTitle("Finn urler -  OBOS")
        self.left = 500
        self.top = 500
        self.setWindowIcon(QIcon('icon2.png'))  

        def add_data(table):
            table.setColumnCount(1)
            table.setHorizontalHeaderLabels(["Urler"])
            urls = find_urlfragment(fragment.text(), get_sitemap())
            maks=0
            for url in urls:
                if len(url) > maks:
                    maks=len(url)
                currentRowCount = table.rowCount()
                table.setRowCount(currentRowCount+1)
                table.setItem(currentRowCount, 0, QTableWidgetItem(f"{url}"))
            table.setColumnWidth(0,700)
            antall.setText(f"Antall urler: {len(urls)}")

        def lagre_data(table):
            data="urls"
            for i in range(table.rowCount()):
                data+=f"\n{table.item(i,0).text()}"
            filename=QFileDialog.getSaveFileName(caption="Lagre fil", directory=f"{fragment.text()}".lower(), filter="Csv (*.csv)")
            
            if filename[0]:
                with open(filename[0],"w") as f:
                    f.write(data)

        
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QHBoxLayout()

        layout1.setContentsMargins(0,0,0,0)
        layout2.setContentsMargins(30,30,40,0)
        layout4.setContentsMargins(0,0,0,0)

        layout1.setSpacing(20)
        layout2.setSpacing(10)
        layout4.setSpacing(2)

        layout2.setAlignment(Qt.AlignVCenter)
        
        fragment_label = QLabel("Urlfragment:")
        fragment = QLineEdit("")
        fragment.returnPressed.connect(lambda :add_data(my_table))
        fragment_width = fragment_label.fontMetrics().boundingRect(fragment_label.text()).width()
        fragment.setMaximumSize(200-fragment_width,20)

        my_table = QTableWidget()
        fragment_label.setMaximumSize(fragment_width+5,20)
        layout4.addWidget(fragment_label)
        layout4.addWidget(fragment)
        
        hent = QPushButton("Hent urler")
        hent.setMaximumSize(200,30)
        lagre = QPushButton("Lagre urler")
        lagre.setMaximumSize(200,30)
        hent.clicked.connect(lambda:add_data(my_table))
        lagre.clicked.connect(lambda:lagre_data(my_table))
        antall = QLabel("")

        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(lambda :lagre_data(my_table))

        layout2.addLayout(layout4)
        layout2.addWidget(hent)
        layout2.addWidget(lagre)
        layout2.addWidget(antall)
        layout1.addLayout(layout2)

        layout3.addWidget(my_table)
        
        layout1.addLayout( layout3 )
        
        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)

app = QApplication(list(""))

window = MainWindow()
window.resize(1000,500)
window.show() 


# Start the event loop.
app.exec_()
