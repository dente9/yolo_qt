import csv
from pathlib import Path
from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableView, QHeaderView

class CsvModel(QAbstractTableModel):
    def __init__(self, path: Path):
        super().__init__()
        with path.open(newline='', encoding='utf-8') as f:
            self._data = list(csv.reader(f))

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

class CsvViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._table = QTableView()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self._table)

    def load(self, path: Path):
        model = CsvModel(path)
        self._table.setModel(model)
        for i in range(model.columnCount()):
            self._table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)