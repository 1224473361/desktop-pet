from PyQt6 import QtGui
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import *
from PyQt6 import QtWidgets
import sys
import os
import socket
import random
import time
from threading import Thread

# 常量定义
# 窗口参数
WINDOW_TITLE = "故事大会"
WINDOW_X = 600
WINDOW_Y = 300
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 337

# 背景图片
BACKGROUND_IMAGE_PATH = "images/talk_background.jpg"

# UI组件参数
CONTENT_X = 30
CONTENT_Y = 30
CONTENT_WIDTH = 550
CONTENT_HEIGHT = 150

MESSAGE_X = 30
MESSAGE_Y = 220
MESSAGE_WIDTH = 550
MESSAGE_HEIGHT = 30
MESSAGE_PLACEHOLDER = "请输入故事主题或关键词"

BUTTON_TEXT = "生成故事"
BUTTON_X = 520
BUTTON_Y = 270
BUTTON_WIDTH = 60
BUTTON_HEIGHT = 30
BUTTON_FONT_NAME = "微软雅黑"
BUTTON_FONT_SIZE = 10

# 退出命令
EXIT_COMMAND = "Q"

# 故事生成模板
STORY_TEMPLATES = [
    "从前有{character}，{character}非常{adjective}。有一天，{character}遇到了{event}，于是{character}决定{action}。最后，{character}学会了{lesson}。",
    "在{place}，住着一位{character}。{character}每天都会{activity}。有一天，{character}发现{discovery}，这改变了{character}的生活。",
    "很久以前，{character}在{place}过着{adjective}的生活。突然，{event}发生了，{character}必须{action}。经过努力，{character}终于{outcome}。",
    "{character}是一个{adjective}的人，总是喜欢{activity}。有一天，{character}遇到了{challenge}，通过{action}，{character}获得了{reward}。",
    "在{place}，{character}和{friend}是最好的朋友。他们一起{activity}，直到有一天{event}改变了他们的关系。"
]

# 故事元素库
STORY_ELEMENTS = {
    "character": ["小兔子", "小猫咪", "小狗", "小松鼠", "小鸟", "小熊", "小狐狸", "小鹿", "小猴子", "小企鹅"],
    "adjective": ["勇敢", "聪明", "善良", "快乐", "好奇", "勤奋", "友好", "乐观", "诚实", "有爱心"],
    "place": ["森林里", "小河边", "山坡上", "花园中", "村庄里", "城市中", "海边", "山谷里", "草原上", "雪山上"],
    "activity": ["唱歌", "跳舞", "画画", "读书", "探险", "帮助别人", "学习新技能", "交朋友", "照顾植物", "观察星星"],
    "event": ["一场大雨", "一阵大风", "一个神秘的礼物", "一次意外的相遇", "一个重要的决定", "一个美丽的梦境", "一次难忘的旅行", "一个特别的节日"],
    "action": ["勇敢面对", "寻求帮助", "努力学习", "坚持不懈", "团结合作", "发挥创意", "保持耐心", "分享快乐"],
    "lesson": ["友谊的重要性", "勇敢面对困难", "分享的快乐", "坚持的力量", "诚实的美德", "帮助他人的意义", "珍惜时间", "感恩的心"],
    "friend": ["小兔子", "小猫咪", "小狗", "小松鼠", "小鸟", "小熊", "小狐狸", "小鹿"],
    "challenge": ["一道难题", "一次考验", "一个困难的选择", "一次失败的经历", "一个误解", "一次意外"],
    "discovery": ["一个秘密花园", "一本神奇的书", "一个古老的传说", "一个隐藏的宝藏", "一个特别的才能"],
    "outcome": ["实现了梦想", "找到了真正的朋友", "学会了重要的道理", "获得了大家的认可", "变得更加快乐"],
    "reward": ["大家的喜爱", "内心的满足", "新的朋友", "宝贵的经验", "美好的回忆"]
}

def resource_path(relative_path):
    """
    获取资源文件的绝对路径，支持PyInstaller打包
    
    Args:
        relative_path (str): 相对路径
    
    Returns:
        str: 绝对路径
    
    Examples:
        >>> resource_path('images/talk_background.jpg')
        'e://desktop-pet/src/images/talk_background.jpg'
    """
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 如果不是打包后的exe，使用当前文件所在目录
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class LocalStoryGenerator:
    """
    本地故事生成器
    
    使用预定义的故事模板和元素库生成随机故事，无需网络连接，完全离线运行
    """
    
    def __init__(self):
        """
        初始化本地故事生成器
        """
        self.templates = STORY_TEMPLATES
        self.elements = STORY_ELEMENTS
    
    def generate_story(self, user_input=""):
        """
        生成随机故事，响应时间控制在500ms以内
        
        Args:
            user_input (str): 故事主题或关键词
        
        Returns:
            str: 生成的故事文本
        
        Examples:
            >>> generator = LocalStoryGenerator()
            >>> story = generator.generate_story("友谊")
            >>> print(story)
            关于'友谊'的故事：
            
            在森林里，小兔子和小猫咪是最好的朋友。他们一起探险，直到有一天一个神秘的礼物改变了他们的关系。
        """
        start_time = time.time()
        
        # 选择随机模板
        template = random.choice(self.templates)
        
        # 填充模板中的占位符
        story = template
        while "{" in story and "}" in story:
            start = story.find("{")
            end = story.find("}")
            if start != -1 and end != -1:
                placeholder = story[start+1:end]
                if placeholder in self.elements:
                    replacement = random.choice(self.elements[placeholder])
                    story = story[:start] + replacement + story[end+1:]
                else:
                    # 如果占位符不在元素库中，使用默认值
                    story = story[:start] + "未知" + story[end+1:]
        
        # 添加用户输入的影响（如果提供了输入）
        if user_input and len(user_input) > 0:
            story = f"关于'{user_input}'的故事：\n\n" + story
        
        # 确保响应时间不超过500ms
        elapsed_time = (time.time() - start_time) * 1000
        if elapsed_time < 500:
            # 添加一点随机延迟，使响应更自然
            remaining_time = 500 - elapsed_time
            time.sleep(remaining_time / 1000)
        
        return story

# 创建全局故事生成器实例
story_generator = LocalStoryGenerator()

class Client(QWidget):
    """
    故事大会客户端界面
    
    提供用户输入故事主题，生成并展示故事的界面
    """
    
    def __init__(self, parent=None, **kwargs):
        """
        初始化界面
        
        Args:
            parent (QWidget): 父窗口部件
            kwargs (dict): 额外参数
        """
        # QWidget.__init__(self)
        super(Client, self).__init__(parent)
        # 设置窗口的大小和位置
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        # 设置标题
        self.setWindowTitle(WINDOW_TITLE)
        # 添加背景
        palette = QtGui.QPalette()
        bg = QtGui.QPixmap(resource_path(BACKGROUND_IMAGE_PATH))
        palette.setBrush(self.backgroundRole(), QtGui.QBrush(bg))
        self.setPalette(palette)
        self.add_ui()
 
        # 启动线程
        self.work_thread()

        # # 展示
        # self.show()
 
    def add_ui(self):
        """
        设置界面当中的组件
        
        初始化并布局以下UI组件：
        - 多行文本显示框：显示聊天信息和生成的故事
        - 单行文本输入框：输入故事主题或关键词
        - 生成按钮：触发故事生成
        """
        # 多行文本显示，显示所有的聊天信息
        self.content = QTextBrowser(self)
        self.content.setGeometry(CONTENT_X, CONTENT_Y, CONTENT_WIDTH, CONTENT_HEIGHT)
 
        # 单行文本，消息发送框
        self.message = QLineEdit(self)
        self.message.setGeometry(MESSAGE_X, MESSAGE_Y, MESSAGE_WIDTH, MESSAGE_HEIGHT)
        self.message.setPlaceholderText(MESSAGE_PLACEHOLDER)
 
        # 发送按钮
        self.button = QPushButton(BUTTON_TEXT, self)
        self.button.setFont(QFont(BUTTON_FONT_NAME, BUTTON_FONT_SIZE, QFont.Weight.Bold))
        self.button.setGeometry(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
 
    def generate_story(self):
        """
        生成故事
        
        从输入框获取用户输入，调用故事生成器生成故事，并在界面上显示结果
        - 如果输入"Q"或"q"，则关闭窗口
        - 如果有输入内容，则基于该内容生成故事
        - 如果没有输入内容，则生成随机故事
        """
        user_input = self.message.text()
        if user_input:
            self.content.append(f"用户: {user_input}")
            if user_input.upper() == EXIT_COMMAND:
                self.close()
                return
            
            # 显示生成中提示
            self.content.append("故事生成器: 正在为您生成故事...")
            
            # 生成故事
            story = story_generator.generate_story(user_input)
            
            # 显示生成的故事
            self.content.append(f"故事生成器: {story}")
            
            # 清空输入框
            self.message.clear()
        else:
            # 如果没有输入，生成随机故事
            self.content.append("故事生成器: 正在为您生成随机故事...")
            story = story_generator.generate_story()
            self.content.append(f"故事生成器: {story}")

    def btn_generate(self):
        """
        点击按钮生成故事
        
        为生成按钮绑定点击事件，触发故事生成
        """
        self.button.clicked.connect(self.generate_story)
 
    def work_thread(self):
        """
        线程处理
        
        在新线程中执行btn_generate方法，为生成按钮绑定点击事件
        """
        Thread(target=self.btn_generate).start()

    def closeEvent(self, event):
        """
        推出销毁对话窗口
        
        处理窗口关闭事件
        
        Args:
            event (QCloseEvent): 关闭事件对象
        """
        self.close()
        event.accept()


if __name__ == '__main__':
    # 创建了一个QApplication对象，对象名为app，带两个参数argc,argv
    # 所有的PyQt5应用必须创建一个应用（Application）对象。sys.argv参数是一个来自命令行的参数列表。
    app = QApplication(sys.argv)
    # 窗口组件初始化
    client = Client()
    client.show()
    # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec_())