from __future__ import annotations

from enum import Enum
from typing import Optional

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPen, QBrush, QPainter, QMouseEvent
from PyQt5.QtWidgets import (
    QMainWindow,
    QToolBar,
    QActionGroup,
    QAction,
    QFrame,
    QDialog,
    QFileDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QDialogButtonBox,
)

from backend import graph_utils
from ui.polynomial_show import PolynomialShowWindow
from ui.utils import Node, Edge


class ChangeNodeIdDialog(QDialog):
    def __init__(self, parent, node_name):
        super().__init__(parent)

        self.setWindowTitle("Изменить имя вершины")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите новое имя вершины:"))
        line_edit = QLineEdit()
        if node_name is not None:
            line_edit.setText(str(node_name))

        layout.addWidget(line_edit)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        layout.addWidget(button_box)
        self.setLayout(layout)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        line_edit.returnPressed.connect(self.accept)

        self.setModal(True)

        self.line_edit = line_edit

    def accept(self):
        self.done(QDialog.Accepted)

    def reject(self):
        self.done(QDialog.Rejected)

    def get_node_name(self):
        return self.line_edit.text()


class ChangeEdgeIdDialog(QDialog):
    def __init__(self, parent, edge_name):
        super().__init__(parent)

        self.setWindowTitle("Изменить имя ребра")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите новое имя ребра"))
        line_edit = QLineEdit()
        if edge_name is not None:
            line_edit.setText(str(edge_name))

        layout.addWidget(line_edit)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        layout.addWidget(button_box)
        self.setLayout(layout)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        line_edit.returnPressed.connect(self.accept)

        self.setModal(True)

        self.line_edit = line_edit

    def accept(self):
        self.done(QDialog.Accepted)

    def reject(self):
        self.done(QDialog.Rejected)

    def get_edge_name(self):
        return self.line_edit.text()


class Window(QMainWindow):
    class Modes(Enum):
        ADD_NODE = 1
        DELETE_NODE = 2
        ADD_EDGE = 3
        DELETE_EDGE = 4
        MOVE = 5

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Polynomials")

        self.setGeometry(100, 100, 1280, 720)

        self.graph_area = GraphArea(self)

        self.setCentralWidget(self.graph_area)
        self.mode: Optional[Window.Modes] = None

        self.create_toolbar()

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(Qt.RightToolBarArea, toolbar)

        group = QActionGroup(self)
        group.setExclusive(True)
        group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)

        actions = [
            ("Добавить вершину", Window.Modes.ADD_NODE),
            ("Удалить вершину", Window.Modes.DELETE_NODE),
            ("Добавить ребро", Window.Modes.ADD_EDGE),
            ("Удалить ребро", Window.Modes.DELETE_EDGE),
            ("Переместить", Window.Modes.MOVE),
        ]

        for title, cur_action in actions:
            button = QAction(title, group)
            button.setCheckable(True)
            button.triggered.connect(
                lambda checked, mode=cur_action: self.set_mode(checked, mode)
            )
            toolbar.addAction(button)

        toolbar.addActions(group.actions())

        command_group = QActionGroup(self)
        command_group.setExclusive(False)
        command_group.setExclusionPolicy(
            QActionGroup.ExclusionPolicy.ExclusiveOptional
        )

        commands = [
            ("Очистить", self.graph_area.clear),
            ("Сохранить", self.graph_area.save),
            ("Открыть", self.graph_area.load),
            ("PC-многочлен", self.graph_area.count_pc_polynomial),
            (
                "Critical configuration многочлен",
                self.graph_area.count_pc_polynomial,
            ),
        ]

        for title, cur_action in commands:
            button = QAction(title, command_group)
            button.triggered.connect(cur_action)
            toolbar.addAction(button)

    def set_mode(self, checked: bool, mode: Window.Modes):
        if checked:
            self.mode = mode
        else:
            self.mode = None
        self.graph_area.on_mode_update(mode)


class GraphArea(QFrame):
    NODE_RADIUS = 20

    def __init__(self, parent: QMainWindow):
        super(GraphArea, self).__init__(parent)

        self.nodes: list[Node] = []
        self.edges: list[Edge] = []
        self.setStyleSheet("background-color: white")

        self.selected_node: Optional[Node] = None
        self.last_pos = QPoint()
        self.setFocusPolicy(Qt.StrongFocus)

    @staticmethod
    def node_radius() -> float:
        return GraphArea.NODE_RADIUS

    def draw_node(self, painter, node: Node):
        node_radius = int(self.node_radius())
        color = (
            QColor(Qt.gray) if node == self.selected_node else QColor(Qt.white)
        )
        painter.setPen(QPen(QColor(Qt.black), 3, Qt.SolidLine))
        painter.setBrush(QBrush(color))
        painter.drawEllipse(
            int(node.x * self.width() - node_radius),
            int(node.y * self.height() - node_radius),
            int(node_radius * 2),
            int(node_radius * 2),
        )
        painter.setPen(QPen(QColor(Qt.black), 1, Qt.SolidLine))
        painter.drawText(
            int(node.x * self.width() - node_radius),
            int(node.y * self.height() - node_radius),
            int(node_radius * 2),
            int(node_radius * 2),
            Qt.AlignCenter,
            node.name,
        )

        self.update()

    def draw_edge(self, painter, edge: Edge):
        painter.setPen(QPen(QColor(Qt.black), 2, Qt.SolidLine))
        painter.drawLine(
            int(edge.node1.x * self.width()),
            int(edge.node1.y * self.height()),
            int(edge.node2.x * self.width()),
            int(edge.node2.y * self.height()),
        )

        painter.setPen(QPen(QColor(Qt.black), 1, Qt.SolidLine))
        posx = (edge.node1.x + edge.node2.x) / 2
        posy = (edge.node1.y + edge.node2.y) / 2
        name = f"e_{edge.name}"
        width = len(name) * 10
        painter.setBrush(QBrush(QColor(Qt.white)))
        painter.drawRect(
            int(posx * self.width() - width // 2),
            int(posy * self.height() - 10),
            width,
            20,
        )
        painter.drawText(
            int(posx * self.width() - width // 2),
            int(posy * self.height() - 10),
            width,
            20,
            Qt.AlignCenter,
            name,
        )
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for edge in self.edges:
            self.draw_edge(painter, edge)
        for node in self.nodes:
            self.draw_node(painter, node)
        self.update()

    def clicked_on_node(self, node, event):
        node_radius = self.node_radius()
        return (node.x * self.width() - event.x()) ** 2 + (
            node.y * self.height() - event.y()
        ) ** 2 <= node_radius ** 2

    def clicked_on_edge(self, edge, event):
        delta = 0.01
        x1, y1 = edge.node1.x, edge.node1.y
        x2, y2 = edge.node2.x, edge.node2.y
        x, y = event.x() / self.width(), event.y() / self.height()

        v1x = x1 - x
        v1y = y1 - y
        v2x = x2 - x
        v2y = y2 - y
        ex = x2 - x1
        ey = y2 - y1
        if ex * -v1x + ey * -v1y < 0 or ex * v2x + ey * v2y < 0:
            return False

        dist_to_line = (v1x * v2y - v2x * v1y) / (
            (x1 - x2) ** 2 + (y1 - y2) ** 2
        ) ** 0.5
        return abs(dist_to_line) < delta

    def delete_node(self, node: Node):
        self.nodes.remove(node)
        self.edges = list(
            filter(lambda x: x.node1 != node and x.node2 != node, self.edges)
        )

    def get_vacant_node_name(self) -> str:
        names = [node.name for node in self.nodes]
        i = 0
        while str(i) in names:
            i += 1
        return str(i)

    def get_vacant_edge_name(self) -> str:
        names = [edge.name for edge in self.edges]
        i = 0
        while str(i) in names:
            i += 1
        return str(i)

    def add_node(self, x: float, y: float, name: Optional[str] = None) -> Node:
        if name is None:
            name = self.get_vacant_node_name()
        node = Node(x, y, name)
        self.nodes.append(node)
        return node

    def add_edge(self, node1: Node, node2: Node, name: Optional[str] = None) -> Edge:
        if name is None:
            name = self.get_vacant_edge_name()
        edge = Edge(node1, node2, name)
        self.edges.append(edge)
        return edge

    def pressed_left_button(self, event: QMouseEvent):
        match self.parent().mode:
            case Window.Modes.ADD_NODE:
                self.add_node(
                    event.x() / self.width(), event.y() / self.height()
                )
                return
            case Window.Modes.DELETE_NODE:
                for node in self.nodes:
                    if self.clicked_on_node(node, event):
                        self.delete_node(node)
                        return
            case Window.Modes.ADD_EDGE:
                for i, node in enumerate(self.nodes):
                    if self.clicked_on_node(node, event):
                        if self.selected_node is not None:
                            if node != self.selected_node:
                                self.add_edge(self.selected_node, node)
                            self.selected_node = None
                        else:
                            self.selected_node = node
                        return
            case Window.Modes.DELETE_EDGE:
                for edge in self.edges:
                    if self.clicked_on_edge(edge, event):
                        self.edges.remove(edge)
                        return
            case Window.Modes.MOVE:
                for node in self.nodes:
                    if self.clicked_on_node(node, event):
                        self.selected_node = node
                        return
                else:
                    self.last_pos = event.pos()

    def rename_node(self, node: Node, name: str):
        node.name = name
        for other_node in self.nodes:
            if node == other_node:
                continue
            if other_node.name == name:
                other_node.name = self.get_vacant_node_name()

    def rename_edge(self, edge: Edge, name: str):
        edge.name = name
        for other_edge in self.edges:
            if edge == other_edge:
                continue
            if other_edge.name == name:
                other_edge.name = self.get_vacant_edge_name()

    def pressed_right_button(self, event: QMouseEvent):
        for node in self.nodes:
            if self.clicked_on_node(node, event):
                dialog = ChangeNodeIdDialog(self, node.name)
                result = dialog.exec_()
                if result == QDialog.Accepted:
                    new_name = dialog.get_node_name()
                    self.rename_node(node, new_name)
                return

        for edge in self.edges:
            if self.clicked_on_edge(edge, event):
                dialog = ChangeEdgeIdDialog(self, edge.name)
                result = dialog.exec_()
                if result == QDialog.Accepted:
                    new_name = dialog.get_edge_name()
                    self.rename_edge(edge, new_name)
                return

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.pressed_left_button(event)
        if event.button() == Qt.RightButton:
            self.pressed_right_button(event)

        self.update()

    def on_mode_update(self, _: Window.Modes):
        self.selected_node = None

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.parent().mode == Window.Modes.MOVE:
            if self.selected_node is not None:
                self.selected_node.x = event.x() / self.width()
                self.selected_node.y = event.y() / self.height()
                self.selected_node.x = min(1.0, max(0.0, self.selected_node.x))
                self.selected_node.y = min(1.0, max(0.0, self.selected_node.y))
            else:
                for node in self.nodes:
                    node.x += (event.x() - self.last_pos.x()) / self.width()
                    node.y += (event.y() - self.last_pos.y()) / self.height()
                    node.x = min(1.0, max(0.0, node.x))
                    node.y = min(1.0, max(0.0, node.y))
                self.last_pos = event.pos()
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.parent().mode == Window.Modes.MOVE:
            self.selected_node = None

    def clear(self):
        self.nodes.clear()
        self.edges.clear()
        self.update()

    def save(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setNameFilter("Graph files (*.graph);;All files (*)")
        dialog.setDefaultSuffix("graph")
        if dialog.exec_() == QDialog.Accepted:
            with open(dialog.selectedFiles()[0], "w") as file:
                file.write(self.get_graph_string())

    def get_graph_string(self):
        graph_string = ""
        graph_string += str(len(self.nodes)) + " " + str(len(self.edges)) + "\n"
        for node in self.nodes:
            graph_string += node.get_node_string() + "\n"
        for edge in self.edges:
            graph_string += edge.get_edge_string() + "\n"
        return graph_string

    def load(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilter("Graph files (*.graph);;All files (*)")
        dialog.setDefaultSuffix("graph")

        if dialog.exec_() == QDialog.Accepted:
            with open(dialog.selectedFiles()[0], "r") as file:
                self.clear()
                lines = file.readlines()
                num_nodes, num_edges = map(int, lines[0].split())
                for i in range(1, num_nodes + 1):
                    node = Node.from_string(lines[i])
                    self.nodes.append(node)
                for i in range(num_nodes + 1, num_nodes + num_edges + 1):
                    source, target, name = map(str, lines[i].split())
                    source_node = next(
                        node for node in self.nodes if node.name == source
                    )
                    target_node = next(
                        node for node in self.nodes if node.name == target
                    )
                    self.edges.append(Edge(source_node, target_node, name))
            self.update()

    def get_graph(self):
        n, m = len(self.nodes), len(self.edges)
        g = graph_utils.Graph()
        node_name_to_index = {}

        for i, node in enumerate(self.nodes):
            node_name_to_index[node.name] = i

        ts = graph_utils.get_symbols(len(self.edges))
        for edge, t in zip(self.edges, ts):
            g.add_edge(
                graph_utils.Edge(
                    node_name_to_index[edge.node1.name],
                    node_name_to_index[edge.node2.name],
                    t,
                )
            )
        return n, m, g

    def count_pc_polynomial(self):
        polynomial_window = PolynomialShowWindow(self)
        polynomial_window.show()
