import os
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QSizePolicy, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTabBar, QTabWidget, QGridLayout, \
    QFrame, QSpacerItem, QToolBar, QCheckBox
    
class RibbonToolBar(QToolBar):
    def __init__(self, parent=None):
        super(RibbonToolBar, self).__init__(parent)

        self.setStyleSheet(open(os.path.join(os.path.dirname(__file__), 'RibbonWidget.qss')).read())

        self.ribbon_widget = RibbonWidget(self)
        self.addWidget(self.ribbon_widget)
        self.setMovable(False)
        self.setFloatable(False)

        self.setMouseTracking(True)

        self.addMenu = self.ribbon_widget.menu_bar.addMenu
        self.addGroup = self.ribbon_widget.menu_bar.addGroup
        self.addSliderChoiceWidget = self.ribbon_widget.menu_bar.addSliderChoiceWidget
    
class RibbonWidget(QWidget):
    def __init__(self, parent=None):
        super(RibbonWidget, self).__init__(parent)

        self.menu_bar = MenuBar(self)

        vlayout = QVBoxLayout(self)
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setSpacing(0)
        vlayout.addWidget(self.menu_bar)

        self.setMouseTracking(True)

class WindowWidget(QMainWindow):
    def __init__(self):
        super(WindowWidget, self).__init__()
        self.margin = 4
        self.setMouseTracking(True)
        
class BaseWidget(QWidget):
    def __init__(self, *args):
        super(BaseWidget, self).__init__(*args)
        self.setMouseTracking(True)
        
class MenuWidget(QWidget):
    def __init__(self, *args):
        super(MenuWidget, self).__init__(*args)
        self.setMouseTracking(True)

    def _setHeight(self, height):
        self.setFixedHeight(height)

    _height = pyqtProperty(int, fset=_setHeight)
    
class GroupWidget(QWidget):
    def __init__(self, p_str, parent=None):
        super(GroupWidget, self).__init__(parent)
        self.title = p_str
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.setMouseTracking(True)
        self.glayout = QGridLayout(self)
        self.glayout.setContentsMargins(3, 10, 3, 3)
        self.glayout.setSpacing(5)
        self.glayout.setVerticalSpacing(1)
        self.button = QPushButton()
        self.button.setText(p_str)
        self.button.setFlat(True)
        self.button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.glayout.addWidget(self.button, 1, 0, 1, 1)
        line = QFrame(self)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Raised)
        self.glayout.addWidget(line, 0, 1, 3, 1)
    
class TabBar(QTabBar):
    def __init__(self, *args):
        super(TabBar, self).__init__(*args)
        self.setMouseTracking(True)
        self.setFixedWidth(600)
        
class MenuBar(QTabWidget):
    def __init__(self, parent=None):
        super(MenuBar, self).__init__(parent)

        tabbar = TabBar(parent)
        self.setTabBar(tabbar)
        self.setMinimumHeight(135)
        self.setMouseTracking(True)

        self._drop = False
        self.currentChanged.connect(self.currentChangedFunc)

    def currentChangedFunc(self, index):
        tab_text = self.tabText(index)
        menu = self.findChild(MenuWidget, tab_text)
        self.anim = QPropertyAnimation(menu, b'_height')
        self.anim.setDuration(100)
        self.anim.setStartValue(0)
        self.anim.setEndValue(100)
        self.anim.start()

    def addMenu(self, p_str):
        p_str = "  {p_str}  ".format(p_str=p_str)
        menu = MenuWidget()
        menu.setObjectName(p_str)
        self.addTab(menu, p_str)
        self.hlayout = QHBoxLayout(menu)
        self.hlayout.setObjectName(p_str)
        self.hlayout.setContentsMargins(0, 0, 0, 0)
        self.hlayout.setSpacing(0)
        hs = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.hlayout.addItem(hs)
        return(menu)

    def addGroup(self, p_str, menu):
        group = GroupWidget(p_str, menu)
        group.setFixedWidth(100)
        group.setObjectName('group')
        insert_index = len(menu.findChildren(GroupWidget, 'group')) - 1
        self.hlayout.insertWidget(insert_index, group)
        return(group)

    def listGroups(self, menu):
        self.group_list = []
        for i in range(self.hlayout.count()):
            try:
                w = self.hlayout.itemAt(i).widget()
                self.group_list.append(w._title)
            except: AttributeError
        return(self.group_list)
    
    def addSliderChoiceWidget(self, menu):
        slider_choice = SliderChoiceWidget()
        slider_choice.setObjectName('param')
        insert_index = len(menu.findChildren(GroupWidget, 'group'))
        self.hlayout.insertWidget(insert_index, slider_choice)
        return(slider_choice)
    
class SliderCheckBox(QCheckBox):
    def __init__(self, p_str):
        super(SliderCheckBox, self).__init__()
        self.setMouseTracking(True)
        self.setText(p_str)
        self.setStyleSheet('''QCheckBox { font-size: 10px;}''')
        self.setStyleSheet('''QCheckBox::indicator{ height: 10px;
                           width: 10px}''')
        
class SliderChoiceWidget(QWidget):
    def __init__(self):
        super(SliderChoiceWidget, self).__init__()
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        self.setMouseTracking(True)
        self.glayout = QGridLayout(self)
        self.glayout.setContentsMargins(10, 10, 3, 3)
        self.glayout.setSpacing(5)
        self.glayout.setVerticalSpacing(1)
        label = QLabel('Sliders')
        label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        label.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Maximum)
        self.glayout.addWidget(label, 2, 0, 1, 1)
        self.clayout = QGridLayout()
        self.clayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.clayout.setSpacing(3)
        self.clayout.setContentsMargins(0, 0, 0, 5)
        self.glayout.addLayout(self.clayout, 0, 0, 2, 1)
        line = QFrame(self)
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Raised)
        self.glayout.addWidget(line, 0, 1, 3, 1)
        
    def addSliderChoice(self, p_str):
        check = SliderCheckBox(p_str)
        count = self.clayout.count()
        if count < 3:
            self.clayout.addWidget(check, count, 0, 1, 1)
            self.setFixedWidth(150)
        if count >= 3:
            cols = (count-(count%3))/3
            self.clayout.addWidget(check, count%3, cols, 1, 1)
            self.setFixedWidth((cols+1) * 150)
        return(check)