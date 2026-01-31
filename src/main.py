import os
import sys
import random
import time
from PyQt6.QtGui import *
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize
from PyQt6.QtWidgets import *

# 添加当前目录到Python路径，确保可以导入talk_show模块
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def resource_path(relative_path):
    """
    获取资源文件的绝对路径，支持PyInstaller打包
    
    Args:
        relative_path (str): 相对路径
    
    Returns:
        str: 绝对路径
    
    Examples:
        >>> resource_path('images/default.gif')
        'e:/desktop-pet/src/images/default.gif'
    """
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 如果不是打包后的exe，使用当前文件所在目录的父目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
    

# 导入故事大会功能
try:
    from talk_show import Client
    TALK_SHOW_AVAILABLE = True
except ImportError as e:
    print(f"导入talk_show模块失败: {e}")
    TALK_SHOW_AVAILABLE = False
    Client = None


class DesktopPet(QWidget):
    """
    桌面宠物主类，负责实现宠物的主要功能和交互逻辑
    
    该类继承自QWidget，实现了桌面宠物的基本功能，包括：
    - 随机动画与文本显示
    - 点击交互
    - 故事大会功能
    
    Examples:
        >>> pet = DesktopPet()
        >>> pet.show()
    """
    
    def __init__(self, parent=None, **kwargs):
        """
        初始化桌面宠物
        
        Args:
            parent (QWidget): 父窗口部件
            kwargs (dict): 额外参数
        """
        super(DesktopPet, self).__init__(parent)
        # 初始化图片和资源路径成员变量
        self.idle_animation_dir = resource_path('images/idle_animation')
        self.default_pet_gif = resource_path('images/idle_animation/default.gif')
        self.click_animation_gif = resource_path('images/click/click.gif')
        self.dialog_file_path = resource_path('dialog/dialog.txt')
        self.favicon_path = resource_path('images/favicon.ico')
        
        # 窗体初始化
        self.init()
        # 托盘化初始
        self.initPall()
        # 宠物静态gif图加载
        self.initPetImage()
        # 宠物正常待机，实现随机切换动作
        self.petNormalAction()


    def init(self):
        """
        窗体初始化
        
        设置窗口属性，包括无标题栏、置顶显示、透明背景等
        - FrameWindowHint: 无边框窗口
        - WindowStaysOnTopHint: 窗口总显示在最上面
        - SubWindow: 新窗口部件是一个子窗口
        """
        # 初始化
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SubWindow)
        self.setAutoFillBackground(False)
        # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        
        # 设置窗口图标
        if os.path.exists(self.favicon_path):
            self.setWindowIcon(QIcon(self.favicon_path))

        # 重绘组件、刷新
        self.repaint()

    def initPall(self):
        """
        托盘化设置初始化
        
        创建系统托盘图标和右键菜单，包括退出和显示选项
        """
        # 使用新的favicon.ico作为托盘图标
        icons = self.favicon_path
        # 设置右键显示最小化的菜单项
        # 菜单项退出，点击后调用quit函数
        quit_action = QAction('退出', self, triggered=self.quit)
        # 设置这个点击选项的图片
        quit_action.setIcon(QIcon(icons))
        # 菜单项显示，点击后调用showing函数
        showing = QAction(u'显示', self, triggered=self.showwin)
        # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
        # 在菜单栏添加一个无子菜单的菜单项‘退出’
        self.tray_icon_menu.addAction(quit_action)
        # 在菜单栏添加一个无子菜单的菜单项‘显示’
        self.tray_icon_menu.addAction(showing)
        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘化图标
        self.tray_icon.setIcon(QIcon(icons))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # 展示
        self.tray_icon.show()

    def initPetImage(self):
        """
        宠物静态gif图加载
        
        初始化宠物的UI组件，包括：
        - 对话框标签
        - 图片显示标签
        - 布局设置
        - 加载动画和对话资源
        """
        # 对话框定义
        self.talkLabel = QLabel(self)
        # 对话框样式设计
        self.talkLabel.setStyleSheet("font:15pt '楷体';border-width: 1px;color:blue;")
        # 定义显示图片部分
        self.image = QLabel(self)
        # QMovie是一个可以存放动态视频的类，一般是配合QLabel使用的,可以用来存放GIF动态图
        self.movie = QMovie(self.default_pet_gif)
        # 设置标签大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将Qmovie在定义的image中显示
        self.image.setMovie(self.movie)
        self.movie.start()
        self.resize(300, 300)

        # 调用自定义的randomPosition，会使得宠物出现位置随机
        self.randomPosition()

        # 布局设置
        vbox = QVBoxLayout()
        vbox.addWidget(self.talkLabel)
        vbox.addWidget(self.image)

        #加载布局：前面设置好的垂直布局
        self.setLayout(vbox)

        # 展示
        self.show()
        # 将宠物正常待机状态的动图放入idle_animations列表中
        self.idle_animations = []
        idle_dir = self.idle_animation_dir
        for i in os.listdir(idle_dir):
            self.idle_animations.append(os.path.join(idle_dir, i))
        # 将宠物正常待机状态的对话放入pet2中
        self.dialog = []
        # 读取目录下dialog文件
        dialog_path = self.dialog_file_path
        with open(dialog_path, "r", encoding="gbk") as f:
            text = f.read()
            # 以\n 即换行符为分隔符，分割放进dialog中
            self.dialog = text.split("\n")

    def petNormalAction(self):
        """
        宠物正常待机动作
        
        初始化定时器，设置宠物的正常待机状态，包括：
        - 随机动作切换定时器（每5秒）
        - 对话切换定时器（每5秒）
        """
        # 每隔一段时间做个动作
        # 定时器设置
        self.timer = QTimer()
        # 时间到了自动执行
        self.timer.timeout.connect(self.randomAct)
        # 动作时间切换设置
        self.timer.start(5000)
        # 宠物状态设置为正常
        self.condition = 0
        # 每隔一段时间切换对话
        self.talkTimer = QTimer()
        self.talkTimer.timeout.connect(self.talk)
        self.talkTimer.start(5000)
        # 对话状态设置为常态
        self.talk_condition = 0
        # 宠物对话框
        self.talk()   

    def randomAct(self):
        """
        随机动作切换
        
        根据宠物的当前状态切换对应的动画：
        - 状态0：正常待机，随机选择空闲动画
        - 状态1：点击反馈，播放点击动画
        """
        # condition记录宠物状态，宠物状态为0时，代表正常待机
        if not self.condition:
            # 随机选择装载在idle_animations里面的gif图进行展示，实现随机切换
            self.movie = QMovie(random.choice(self.idle_animations))
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
        # condition不为0，转为切换特有的动作，实现宠物的点击反馈
        # 这里可以通过else-if语句往下拓展做更多的交互功能
        elif self.condition == 1:
            # 读取特殊状态图片路径
            self.movie = QMovie(self.click_animation_gif)
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            # 宠物状态设置为正常待机
            self.condition = 0
            self.talk_condition = 0
            

    def talk(self):
        """
        宠物对话框行为处理
        
        根据对话状态显示不同的文本内容：
        - 状态0：随机显示dialog.txt中的对话内容
        - 状态1：显示点击反馈文本"咬你哦！"
        """
        if not self.talk_condition:
            # talk_condition为0则选取加载在dialog中的语句
            self.talkLabel.setText(random.choice(self.dialog))
            # 设置样式
            self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:15pt '楷体';"
                "color:white;"
                "background-color: white"
                "url(:/)"
            )
            # 根据内容自适应大小
            self.talkLabel.adjustSize()
        else:
            # talk_condition为1显示为别点我，这里同样可以通过if-else-if来拓展对应的行为
            self.talkLabel.setText("咬你哦！")
            self.talkLabel.setStyleSheet(
                "font: bold;"
                "font:15pt '楷体';"
                "color:white;"
                "background-color: white"
                "url(:/)"
            )
            self.talkLabel.adjustSize()
            # self.talkLabel.
            # 设置为正常状态
            self.talk_condition = 0

    def quit(self):
        """
        退出操作，关闭程序
        """
        self.close()
        sys.exit()

    def showwin(self):
        """
        显示宠物
        
        通过设置窗体透明度为1来显示宠物
        """
        self.setWindowOpacity(1)

    def randomPosition(self):
        """
        宠物随机位置
        
        设置宠物在屏幕上的初始位置，默认显示在屏幕中央
        """
        # screenGeometry（）函数提供有关可用屏幕几何的信息
        screen = QApplication.primaryScreen()
        screen_geo = screen.availableGeometry()
        # 获取窗口坐标系
        pet_geo = self.geometry()
        # 默认显示在屏幕中央，而不是随机位置（方便找到窗口）
        width = int((screen_geo.width() - pet_geo.width()) / 2)
        height = int((screen_geo.height() - pet_geo.height()) / 2)
        self.move(width, height)

    def mousePressEvent(self, event):
        """
        鼠标左键按下时, 宠物将和鼠标位置绑定
        
        Args:
            event (QMouseEvent): 鼠标事件对象
        """
        # 更改宠物状态为点击
        self.condition = 1
        # 更改宠物对话状态
        self.talk_condition = 1
        # 即可调用对话状态改变
        self.talk()
        # 即刻加载宠物点击动画
        self.randomAct()
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_follow_mouse = True
        # globalPosition() 事件触发点相对于桌面的位置
        # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
        self.mouse_drag_pos = event.globalPosition().toPoint() - self.pos()
        event.accept()
        # 拖动时鼠标图形的设置
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    def mouseMoveEvent(self, event):
        """
        鼠标移动时调用，实现宠物随鼠标移动
        
        Args:
            event (QMouseEvent): 鼠标事件对象
        """
        # 如果鼠标左键按下，且处于绑定状态
        if event.buttons() & Qt.MouseButton.LeftButton and self.is_follow_mouse:
            # 宠物随鼠标进行移动
            self.move(event.globalPosition().toPoint() - self.mouse_drag_pos)
        event.accept()

    def mouseReleaseEvent(self, event):
        """
        鼠标释放调用，取消绑定
        
        Args:
            event (QMouseEvent): 鼠标事件对象
        """
        self.is_follow_mouse = False
        # 鼠标图形设置为箭头
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))

    def enterEvent(self, event):
        """
        鼠标移进时调用
        
        Args:
            event (QEvent): 事件对象
        """
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def contextMenuEvent(self, event):
        """
        宠物右键点击交互
        
        显示右键菜单，包含以下选项：
        - 隐藏：通过设置透明度隐藏宠物
        - 故事大会：打开故事生成功能
        - 退出：关闭程序
        
        Args:
            event (QContextMenuEvent): 右键菜单事件对象
        """
        # 定义菜单
        menu = QMenu(self)
        # 定义菜单项
        hide = menu.addAction("隐藏")
        question_answer = menu.addAction("故事大会")
        menu.addSeparator()
        quitAction = menu.addAction("退出")

        # 使用exec()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = menu.exec(self.mapToGlobal(event.pos()))
        # 点击事件为退出
        if action == quitAction:
            qApp.quit()
        # 点击事件为隐藏
        if action == hide:
            # 通过设置透明度方式隐藏宠物
            self.setWindowOpacity(0)
        # 点击事件为故事大会
        if action == question_answer:
            if TALK_SHOW_AVAILABLE and Client:
                self.client = Client()
                self.client.show()
            else:
                QMessageBox.warning(self, "提示", "故事大会功能当前不可用。")

    def haveRest(self):
        """
        休息时间
        
        显示休息提醒，包括：
        - 显示"休息一下"文本
        - 切换到休息动画
        - 将宠物移动到屏幕中央
        """
        self.show_time_rest.setText("休息一下")
        self.show_time_rest.setStyleSheet(
                "font: bold;"
                "font:25pt '楷体';"
                "color:white;"
                "background-color: white"
                "url(:/)"
            )
        
        # 固定休息图标
        self.condition = 2
        self.randomAct()
        # screenGeometry（）函数提供有关可用屏幕几何的信息
        screen = QApplication.primaryScreen()
        screen_geo = screen.availableGeometry()
        # 获取窗口坐标系
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width())
        height = (screen_geo.height() - pet_geo.height())
        self.move(width / 2, height / 2)

if __name__ == '__main__':
    # 创建了一个QApplication对象，对象名为app，带两个参数argc,argv
    app = QApplication(sys.argv)
    # 窗口组件初始化
    pet = DesktopPet()
    # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec())