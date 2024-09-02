from tkinter import *
from collections import deque
 
 
class Window:
    def __init__(self, master):
        self.master = master
        self.master.option_add("*Font", "Verdana 12")
 
        self.Main = Frame(self.master)
 
        self.stack = deque(maxlen = 10)
        self.stackcursor = 0
 
        self.L1 = Label(self.Main, text = "Syntax Highlighter for Python language")
        self.L1.pack(padx = 5, pady = 5)
 
 
        #---------
 
        self.T1 = Text(self.Main, width = 90, height = 25)
 
        self.T1.tag_configure("orange", foreground = "orange", font = "Verdana 12")
        self.T1.tag_configure("blue", foreground = "blue", font = "Verdana 12")
        self.T1.tag_configure("purple", foreground = "purple", font = "Verdana 12")
        self.T1.tag_configure("green", foreground = "green", font = "Verdana 12")
        self.T1.tag_configure("red", foreground = "red", font = "Verdana 12")
 
        self.tags = ["orange", "blue", "purple", "green", "red"]
 
        self.wordlist = [
    # Python Keywords
    [
        "class", "def", "for", "if", "else", "elif", "import", "from", "as", "break", 
        "while", "print", "return", "try", "except", "finally", "raise", "lambda", 
        "with", "yield", "del", "global", "nonlocal", "assert", "async", "await", 
        "pass", "continue", "True", "False", "None", "nonlocal", "await", "async", 
        "or", "and", "not", "is", "in", "yield", "yield from", "yield from", "def", 
        "type", "super", "self"
    ],
    
    # Python Types
    [
        "int", "float", "complex", "str", "list", "tuple", "dict", "set", "bool", 
        "NoneType", "bytes", "bytearray", "range", "object", "frozenset", "type",
        "MemoryView", "Decimal", "Fraction", "NamedTuple"
    ],
    
    # Python Libraries
    [
        "pygame", "tkinter", "sys", "os", "mysql", "requests", "json", "csv", "re", 
        "math", "datetime", "collections", "itertools", "functools", "logging", 
        "socket", "sqlite3", "xml", "argparse", "urllib", "configparser", "pytz",
        "pytest", "unittest", "asyncio", "queue", "multiprocessing", "shutil", 
        "subprocess", "inspect", "traceback", "ctypes", "threading"
    ],
    
    # Python Numbers
    [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ]
]

 
        self.T1.bind("<Return>", lambda event: self.indent(event.widget))
         
        self.T1.pack(padx = 5, pady = 5)
 
        #---------
 
        self.menu = Menu(self.Main)
        self.menu.add_command(label = "Print", command = self.print_stack)
        self.menu.add_command(label = "Undo", command = self.undo)
        self.menu.add_command(label = "Redo", command = self.redo)
 
        self.master.config(menu = self.menu)
 
        self.B1 = Button(self.Main, text = "Print", width = 8, command = self.display)
        self.B1.pack(padx = 5, pady = 5, side = LEFT)
 
        self.B2 = Button(self.Main, text = "Clear", width = 8, command = self.clear)
        self.B2.pack(padx = 5, pady = 5, side = LEFT)
 
        self.B3 = Button(self.Main, text = "Undo", width = 8, command = self.undo)
        self.B3.pack(padx = 5, pady = 5, side = LEFT)
 
        self.B4 = Button(self.Main, text = "Redo", width = 8, command = self.redo)
        self.B4.pack(padx = 5, pady = 5, side = LEFT)
 
        self.Main.pack(padx = 5, pady = 5)
 
 
    def tagHighlight(self):
        start = "1.0"
        end = "end"
         
        for mylist in self.wordlist:
            num = int(self.wordlist.index(mylist))
 
            for word in mylist:
                self.T1.mark_set("matchStart", start)
                self.T1.mark_set("matchEnd", start)
                self.T1.mark_set("SearchLimit", end)
 
                mycount = IntVar()
                 
                while True:
                    index= self.T1.search(word,"matchEnd","SearchLimit", count=mycount, regexp = False)
 
                    if index == "": break
                    if mycount.get() == 0: break
 
                    self.T1.mark_set("matchStart", index)
                    self.T1.mark_set("matchEnd", "%s+%sc" % (index, mycount.get()))
 
                    preIndex = "%s-%sc" % (index, 1)
                    postIndex = "%s+%sc" % (index, mycount.get())
                     
                    if self.check(index, preIndex, postIndex):
                        self.T1.tag_add(self.tags[num], "matchStart", "matchEnd")
                         
 
    def check(self, index, pre, post):
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p",
                   "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
 
        if self.T1.get(pre) == self.T1.get(index):
            pre = index
        else:
            if self.T1.get(pre) in letters:
                return 0
 
        if self.T1.get(post) in letters:
            return 0
 
        return 1
 
 
    def scan(self):
        start = "1.0"
        end = "end"
        mycount = IntVar()
 
        regex_patterns = [r'".*"', r'#.*']
 
        for pattern in regex_patterns:
            self.T1.mark_set("start", start)
            self.T1.mark_set("end", end)
 
            num = int(regex_patterns.index(pattern))
 
            while True:
                index = self.T1.search(pattern, "start", "end", count=mycount, regexp = True)
 
                if index == "": break
 
                if (num == 1):
                    self.T1.tag_add(self.tags[4], index, index + " lineend")
                elif (num == 0):
                    self.T1.tag_add(self.tags[3], index, "%s+%sc" % (index, mycount.get()))
 
                self.T1.mark_set("start", "%s+%sc" % (index, mycount.get()))
 
 
    def indent(self, widget):
 
        index1 = widget.index("insert")
        index2 = "%s-%sc" % (index1, 1)
        prevIndex = widget.get(index2, index1)
 
        prevIndentLine = widget.index(index1 + "linestart")
        print("prevIndentLine ",prevIndentLine)
        prevIndent = self.getIndex(prevIndentLine)
        print("prevIndent ", prevIndent)
 
 
        if prevIndex == ":":
            widget.insert("insert", "\n" + "     ")
            widget.mark_set("insert", "insert + 1 line + 5char")
 
            while widget.compare(prevIndent, ">", prevIndentLine):
                widget.insert("insert", "     ")
                widget.mark_set("insert", "insert + 5 chars")
                prevIndentLine += "+5c"
            return "break"
         
        elif prevIndent != prevIndentLine:
            widget.insert("insert", "\n")
            widget.mark_set("insert", "insert + 1 line")
 
            while widget.compare(prevIndent, ">", prevIndentLine):
                widget.insert("insert", "     ")
                widget.mark_set("insert", "insert + 5 chars")
                prevIndentLine += "+5c"
            return "break"
 
 
    def getIndex(self, index):
        while True:
            if self.T1.get(index) == " ":
                index = "%s+%sc" % (index, 1)
            else:
                return self.T1.index(index)
            
                    
    def update(self):
        self.stackify()
        self.tagHighlight()
        self.scan()
 
    def display(self):
        print(self.T1.get("1.0", "end"))     
 
    def clear(self):
        self.T1.delete("1.0", "end")
 
    def stackify(self):
        self.stack.append(self.T1.get("1.0", "end - 1c"))
        if self.stackcursor < 9: self.stackcursor += 1
 
    def undo(self):
        if self.stackcursor != 0:
            self.clear()
            if self.stackcursor > 0: self.stackcursor -= 1
            self.T1.insert("0.0", self.stack[self.stackcursor])
 
    def redo(self):
        if len(self.stack) > self.stackcursor + 1:
            self.clear()
            if self.stackcursor < 9: self.stackcursor += 1
            self.T1.insert("0.0", self.stack[self.stackcursor])
 
    def print_stack(self):
        i = 0
        for stack in self.stack:
            print(str(i) + " " + stack)
            i += 1
 
                      
root = Tk()
window = Window(root)
root.bind("<Key>", lambda event: window.update())
root.mainloop()
