class Start:
    def __init__(self):
        self.num = 3
        self.start()
    def start(self):
        start = AdvencedLevel(self.num)
class BasicLevel:
    def __init__(self, num=None):
        print('created lvl')
        self.num = num
        self.load_lvl()
    def load_lvl(self):
        print(self.num)


class AdvencedLevel(BasicLevel):
    def __init__(self, num = None):
        self.num = num
        print('Upgraiding to advenced')
        BasicLevel.__init__(self, num=self.num)


    def load_lvl(self):
        print(self.num)

# Start()
AdvencedLevel(3)
# BasicLevel(3).load_lvl()
# AdvencedLevel().load_lvl()