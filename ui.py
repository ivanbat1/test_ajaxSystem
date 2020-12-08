import json
import requests
import sys
from PyQt5.QtWidgets import (QLabel, QPushButton, QLineEdit, QTableWidget,
                             QTableWidgetItem, QHeaderView, QVBoxLayout)
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "App"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 400
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        button_window_test_results = QPushButton('Search test result', self)
        button_window_test_results.resize(300, 25)
        button_window_test_results.move(100, 100)
        button_window_test_results.clicked.connect(self.button_window_test_results)

        button_window_add_test_result = QPushButton('Add new test result', self)
        button_window_add_test_result.resize(300, 25)
        button_window_add_test_result.move(100, 200)
        button_window_add_test_result.clicked.connect(self.button_window_add_test_result)

        button_window_remove_test_result = QPushButton('Remove test result', self)
        button_window_remove_test_result.resize(300, 25)
        button_window_remove_test_result.move(100, 300)
        button_window_remove_test_result.clicked.connect(self.button_window_remove_test_result)
        self.show()

    @pyqtSlot()
    def button_window_test_results(self):
        self.cams = WindowSearchTestResult()
        self.cams.show()
        self.close()

    @pyqtSlot()
    def button_window_add_test_result(self):
        self.cams = WindowAddNewTestResult()
        self.cams.show()
        self.close()

    @pyqtSlot()
    def button_window_remove_test_result(self):
        self.cams = WindowRemoveTestResult()
        self.cams.show()
        self.close()


class WindowRemoveTestResult(QDialog):
    API_URL = 'http://127.0.0.1:5000/api_v1/test_result/'

    def __init__(self):
        super().__init__()
        self.title = "Remove test result"
        self.init_ui()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.submit_data)
        button_box.rejected.connect(self.go_main_window)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle(self.title)

    def init_ui(self):
        self.form_group_box = QGroupBox("Remove test result")
        layout = QFormLayout()
        self.record_id = QLineEdit()
        layout.addRow(QLabel("Record id:"), self.record_id)
        self.form_group_box.setLayout(layout)

    def submit_data(self):
        record_id = self.record_id.text()
        response = requests.delete(self.API_URL + record_id)
        if response.status_code != 200:
            return f'Error {response.status_code}'
        response_json = json.loads(response.text)
        result = response_json['result']
        print(result)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()


class WindowAddNewTestResult(QDialog):
    API_URL = 'http://127.0.0.1:5000/api_v1/test_result'

    def __init__(self):
        super().__init__()
        self.title = "Add new"
        self.init_ui()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.submit_data)
        button_box.rejected.connect(self.go_main_window)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

        self.setWindowTitle(self.title)

    def init_ui(self):
        self.form_group_box = QGroupBox("Add new test result")
        layout = QFormLayout()
        self.dev_type = QLineEdit()
        layout.addRow(QLabel("Device type:"), self.dev_type)
        self.operator = QLineEdit()
        layout.addRow(QLabel("Operator:"), self.operator)
        self.time = QDateTimeEdit()
        layout.addRow(QLabel("Time:"), self.time)
        self.success = QRadioButton()
        layout.addRow(QLabel("Success:"), self.success)
        self.form_group_box.setLayout(layout)

    def submit_data(self):
        dev_type = self.dev_type.text()
        operator = self.operator.text()
        time = self.time.text()
        success = self.success.isChecked()
        data = {
            'device_type': dev_type,
            'operator': operator,
            'time': time,
            'success': 1 if success else 0,
        }
        response = requests.post(self.API_URL, data=data)
        if response.status_code != 200:
            return f'Error {response.status_code}'
        response_json = json.loads(response.text)
        result = response_json['result']
        print(result)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()


class WindowSearchTestResult(QDialog):
    API_URL = 'http://127.0.0.1:5000/api_v1/stat'

    def __init__(self):
        super().__init__()
        self.title = "Searh test results"
        self.top = 100
        self.left = 100
        self.width = 600
        self.height = 400
        self.init_ui()

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

    def init_ui(self):
        # create input field for name operator.
        self.input_name = QLineEdit(self)
        input_name = QLabel("Operator", self)
        input_name.move(0, 0)
        self.input_name.move(0, 30)

        # create button search name.
        search_button = QPushButton('SEARCH', self)
        search_button.move(220, 30)
        search_button.clicked.connect(self.operator_search)

        # button back to main window.
        back_button = QPushButton('BACK', self)
        back_button.move(300, 30)
        back_button.clicked.connect(self.go_main_window)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 60, 0, 0)

    def operator_search(self):
        """
        Выпадающий список дней.
        """
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        name_operator = self.input_name.text()
        response = requests.get(self.API_URL, params={'operator': name_operator})
        if response.status_code != 200:
            return f'Error {response.status_code}'
        response_json = json.loads(response.text)
        results = response_json.get('result')
        if isinstance(results, list):
            self.table_result(results)
            self.layout.addWidget(self.table)
            self.setLayout(self.layout)
        else:
            print(results)

    def table_result(self, results):
        self.table = QTableWidget(self)
        table_headers = ["Type device", "All tests", "Success tests", "Unsuccessful tests"]
        self.table.setRowCount(len(results))
        self.table.setColumnCount(len(table_headers))
        self.table.setHorizontalHeaderLabels(table_headers)

        for index, result in enumerate(results):
            self.table.setItem(index, 0, QTableWidgetItem(result['device_type']))
            self.table.setItem(index, 1, QTableWidgetItem(result['all_results']))
            self.table.setItem(index, 2, QTableWidgetItem(result['success']))
            self.table.setItem(index, 3, QTableWidgetItem(result['unsuccessful']))

        self.table.resizeColumnsToContents()

        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.move(60, 0)

    def go_main_window(self):
        self.cams = Window()
        self.cams.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    money = Window()
    sys.exit(app.exec_())
