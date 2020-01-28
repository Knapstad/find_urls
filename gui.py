from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from finn_alle_sider import (
    find_urlfragment,
    get_sitemap_obos,
    get_sitemap_nye,
    get_all_sitemaps,
)
import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        print("worker woken")

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        self.fn(*self.args, **self.kwargs)
        print("worker exexute func")


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Finn urler -  OBOS")
        self.left = 500
        self.top = 500
        self.setWindowIcon(QIcon(resource_path("icon2.png")))

        self.sitemap_obos = None
        self.sitemap_nye = None
        self.sitemap_begge = None
        self.threadpool = QThreadPool()

        def execute_add_data():
            print("starting execute")
            worker = Worker(add_data, my_table)
            self.threadpool.start(worker)

        def add_data(table):
            print("in add data")
            table.setColumnCount(1)
            table.setRowCount(0)
            table.setHorizontalHeaderLabels(["Url", "Tittel"])

            if str(site.currentText()) == "obos":
                print("in obos")
                if self.sitemap_obos is None:
                    self.sitemap_obos = get_sitemap_obos()
                urls = find_urlfragment(fragment.text(), self.sitemap_obos)

            if str(site.currentText()) == "nye":
                print("in nye")
                if self.sitemap_nye is None:
                    self.sitemap_nye = get_sitemap_nye()
                urls = find_urlfragment(fragment.text(), self.sitemap_nye)

            if str(site.currentText()) == "begge":
                print("in begge")
                if self.sitemap_begge is None:
                    print(self.sitemap_begge is None)
                    self.sitemap_begge = get_all_sitemaps()
                urls = find_urlfragment(fragment.text(), self.sitemap_begge)

            for url in urls:
                currentRowCount = table.rowCount()
                table.setRowCount(currentRowCount + 1)
                table.setItem(currentRowCount, 0, QTableWidgetItem(f"{url}"))
            table.setColumnWidth(0, 700)
            antall.setText(f"Antall urler: {len(urls)}")

        def lagre_data(table):
            data = "urls"
            for i in range(table.rowCount()):
                data += f"\n{table.item(i,0).text()}"
            filename = QFileDialog.getSaveFileName(
                caption="Lagre fil",
                directory=f"{fragment.text()}".lower(),
                filter="Csv (*.csv)",
            )

            if filename[0]:
                with open(filename[0], "w") as f:
                    f.write(data)

        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QHBoxLayout()
        layout5 = QHBoxLayout()

        layout1.setContentsMargins(0, 0, 0, 0)
        layout2.setContentsMargins(30, 30, 40, 0)
        layout4.setContentsMargins(0, 0, 0, 0)
        layout5.setContentsMargins(0, 0, 0, 0)

        layout1.setSpacing(20)
        layout2.setSpacing(10)
        layout4.setSpacing(2)
        layout5.setSpacing(0)

        layout2.setAlignment(Qt.AlignVCenter)

        fragment_label = QLabel("Urlfragment:")
        fragment = QLineEdit("")
        fragment.returnPressed.connect(execute_add_data)
        fragment_width = (
            fragment_label.fontMetrics().boundingRect(fragment_label.text()).width()
        )
        fragment.setMaximumSize(200 - fragment_width, 20)

        my_table = QTableWidget()
        fragment_label.setMaximumSize(fragment_width + 5, 20)
        layout4.addWidget(fragment_label)
        layout4.addWidget(fragment)

        site_label = QLabel("Hvilken side:")
        site = QComboBox()
        site.addItems(["obos", "nye", "begge"])
        layout5.addWidget(site_label)
        layout5.addWidget(site)

        hent = QPushButton("Hent urler")
        hent.setMaximumSize(200, 30)
        lagre = QPushButton("Lagre urler")
        lagre.setMaximumSize(200, 30)
        hent.clicked.connect(execute_add_data)
        lagre.clicked.connect(lambda: lagre_data(my_table))
        antall = QLabel("")

        shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        shortcut.activated.connect(lambda: lagre_data(my_table))

        layout2.addLayout(layout5)
        layout2.addLayout(layout4)
        layout2.addWidget(hent)
        layout2.addWidget(lagre)
        layout2.addWidget(antall)
        layout1.addLayout(layout2)

        layout3.addWidget(my_table)

        layout1.addLayout(layout3)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


app = QApplication(list(""))

window = MainWindow()
window.resize(1000, 500)
window.show()


# Start the event loop.
app.exec_()
