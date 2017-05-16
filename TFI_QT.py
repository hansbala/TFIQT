import sys
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

path = r"C:/Users/Hans/AppData/Local/tfipy/"

curr_topic = 1
curr_page = 1
topics = ["Welcome","Syntax", "Strings", "Loops", "Functions", "Conditionals"]
num_topics = [2, 12, 16, 19, 19, 15]

class Window(QMainWindow):
	
	def __init__(self):
		super(Window, self).__init__()
		self.setWindowTitle("Python Coding Platform")
		self.parent = QWidget()
		self.setCentralWidget(self.parent)
		self.addMainMenuBar()
		self.addMainLayout()
		self.addMainQuitFunction()
		self.showMaximized()
	
	def addMainMenuBar(self):
		main_menu = self.menuBar()
		syntax_menu = main_menu.addMenu("Syntax")
		strings_menu = main_menu.addMenu("Strings")
		loops_menu = main_menu.addMenu("Loops")
		functions_menu = main_menu.addMenu("Functions")
		conditionals_menu = main_menu.addMenu("Conditionals")
		custom_menu = main_menu.addMenu("Customization")
		#For the customization menu
		color_menu = custom_menu.addMenu("Color Picker")
		text_editor_action = QAction("Change Color of Left Pane", self)
		text_editor_action.triggered.connect(self.createTextColorPickerDialog)
		code_editor_action = QAction("Change Font of Right Pane", self)
		code_editor_action.triggered.connect(self.createCodeColorPickerDialog)
		
		font_action = QAction("Font Picker", self)
		font_action.triggered.connect(self.createFontPickerDialog)
		
		color_menu.addAction(text_editor_action)
		color_menu.addAction(code_editor_action)
		custom_menu.addAction(font_action)
		
	def addMainQuitFunction(self):
		quit_action = QAction("QUIT", self)
		quit_action.setShortcut("Ctrl+Q")
		quit_action.triggered.connect(self.closeApplication)
	
	def addMainLayout(self):
		#Adding Layouts
		parent_hbox = QHBoxLayout()
		left_vbox = QVBoxLayout()
		right_vbox = QVBoxLayout()
		left_butt_hbox = QHBoxLayout()
		right_butt_hbox = QHBoxLayout()
		
		#Adding text editors for left - right panes
		self.text_editor = QPlainTextEdit()
		self.configureTextEditor()
		self.code_editor = QPlainTextEdit()
		self.configureCodeEditor()
		
		#Adding the buttons
		btn_main = QPushButton("BACK TO MAIN PAGE")
		btn_main.clicked.connect(self.goMainPage)
		btn_prev = QPushButton("PREVIOUS")
		btn_prev.clicked.connect(self.goPreviousPage)
		btn_next = QPushButton("NEXT")
		btn_next.clicked.connect(self.goNextPage)
		btn_reset = QPushButton("RESET")
		btn_reset.clicked.connect(self.resetCode)
		btn_ans = QPushButton("SHOW ANSWER")
		btn_ans.clicked.connect(self.showAnswer)
		btn_run = QPushButton("EXECUTE")
		btn_run.clicked.connect(self.executeCode)
		
		#Adding everything to the layout
		left_butt_hbox.addWidget(btn_main)
		left_butt_hbox.addWidget(btn_prev)
		left_butt_hbox.addWidget(btn_next)
		right_butt_hbox.addWidget(btn_reset)
		right_butt_hbox.addWidget(btn_ans)
		right_butt_hbox.addWidget(btn_run)
		left_vbox.addWidget(self.text_editor)
		left_vbox.addLayout(left_butt_hbox)
		right_vbox.addWidget(self.code_editor)
		right_vbox.addLayout(right_butt_hbox)
		parent_hbox.addLayout(left_vbox)
		parent_hbox.addLayout(right_vbox)
		self.parent.setLayout(parent_hbox)
	
	def configureTextEditor(self):
		self.text_editor.setStyleSheet(QString.fromUtf8("background-color: rgb(173, 216, 230);"))
		font = QFont()
		font.setPointSize(16)
		self.text_editor.setFont(font)
		self.text_editor.setReadOnly(True)
		
	def configureCodeEditor(self):
		self.code_editor.setStyleSheet(QString.fromUtf8("background-color: rgb(44, 76, 99);"))
		font = QFont()
		font.setPointSize(16)
		self.code_editor.setFont(font)
		
	def createTextColorPickerDialog(self):
		color = QColorDialog.getColor()
		self.text_editor.setStyleSheet(QString.fromUtf8("background-color: %s;" % color.name()))
	
	def createCodeColorPickerDialog(self):
		color = QColorDialog.getColor()
		self.code_editor.setStyleSheet(QString.fromUtf8("background-color: %s;" % color.name()))
	
	def createFontPickerDialog(self):
		font, valid = QFontDialog.getFont()
		if valid:
			self.text_editor.setFont(font)
			self.code_editor.setFont(font)
			
	def closeApplication(self):
		sys.exit()
		
	def executeCode(self):
		#Use the global variable 'path'
		global path
		# Saving the file
		program_path = path + "text.py"
		with open(program_path, 'w') as program_file:
			program_file.write(str(self.code_editor.toPlainText()))
		# Executing the code
		os.system("python -i " + program_path)
	
	def goMainPage(self):
		global path, curr_topic, curr_page
		curr_topic = 1
		curr_page = 1
		file_path = path+"InfoFiles/welc.txt"
		text = open(file_path).read()
		self.text_editor.setPlainText(text)
	
	def goPreviousPage(self):
		global topics, num_topics, curr_page, curr_topic
		#Edge case, if it is the first topic then do nothing
		if(curr_page == 1 and curr_topic == 1):
			pass
		else:
			if(curr_page == 1):
				curr_topic -= 1 #Go back one topic
				curr_page = num_topics[curr_topic] #Set it to the last lesson in the topic
			else:
				curr_page -= 1
		self.displayInfoFile()
		self.displayCodeFile()
		
	def goNextPage(self):
		global topics, num_topics, curr_page, curr_topic
		#Edge case, if it is the last topic, and last page
		if(curr_topic == (len(topics) - 1) and curr_page == num_topics[curr_topic]):
			pass #Do nothing
		else:
			#If it is the last page in current topic
			if(curr_page == num_topics[curr_topic]):
				curr_topic += 1
				curr_page = 1 #First page of next topic
			else:
				curr_page += 1
		#Display the new File
		self.displayInfoFile()
		self.displayCodeFile()
		
	def resetCode(self):
		self.displayCodeFile()
		
	def showAnswer(self):
		global path
		file_path = path + "FinalCode/" + topics[curr_topic] + "/" + "less" + str(curr_page) + ".py"
		text = open(file_path).read()
		self.code_editor.setPlainText(text)
		
	def displayInfoFile(self):
		global path
		file_path = path + "InfoFiles/" + topics[curr_topic] + "/" + "less" + str(curr_page) + ".txt"
		text = open(file_path).read()
		self.text_editor.setPlainText(text)
		
	def displayCodeFile(self):
		global path
		file_path = path + "InitialCode/" + topics[curr_topic] + "/" + "less" + str(curr_page) + ".py"
		text = open(file_path).read()
		self.code_editor.setPlainText(text)
	
def runGui():
	app = QApplication(sys.argv)
	win = Window()
	app.exec_()

def main():
	runGui()
	
if __name__ == "__main__":
	main()