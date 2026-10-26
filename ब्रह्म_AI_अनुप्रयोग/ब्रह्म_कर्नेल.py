import os as _os
import sys as _sys

_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
if _ROOT not in _sys.path:  # रिपॉज़िटरी रूट से sibling packages import करें
    _sys.path.append(_ROOT)

# ब्रह्म कर्नेल (Unified Master Kernel)

from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_सिस्टम_आह्वान import ब्रह्मसिस्टमआह्वान
from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_प्रोसेस_कर्नेल import ब्रह्मप्रोसेसकर्नेल
from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_स्मृति_प्रबंधक import ब्रह्मस्मृति
from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_शेड्यूलर import ब्रह्मशेड्यूलर


class ब्रह्मकर्नेल:

    def __init__(self):

        print("🕉️ ब्रह्म कर्नेल प्रारंभ")

        self.sys = ब्रह्मसिस्टमआह्वान()

        self.memory = ब्रह्मस्मृति()

        self.process = ब्रह्मप्रोसेसकर्नेल()

        self.scheduler = ब्रह्मशेड्यूलर()


    # create process
    def प्रक्रिया_बनाओ(self, name):

        return self.process.चलाओ(name)


    # stop process
    def प्रक्रिया_रोको(self, pid):

        return self.process.रोको(pid)


    # memory write
    def स्मृति_लिखो(self, key, value):

        return self.memory.लिखो(key, value)


    # memory read
    def स्मृति_पढ़ो(self, key):

        return self.memory.पढ़ो(key)


    # file write
    def फ़ाइल_लिखो(self, path, data):

        return self.sys.लिखो(path, data)


    # file read
    def फ़ाइल_पढ़ो(self, path):

        return self.sys.पढ़ो(path)


    # system info
    def जानकारी(self):

        return self.sys.जानकारी()


    # scheduler add
    def कार्य_जोड़ो(self, name, func):

        return self.scheduler.जोड़ो(name, func)


    # scheduler stop
    def कार्य_रोको(self):

        return self.scheduler.रोको()


    # full status
    def स्थिति(self):

        return {

            "memory": self.memory.सूची(),

            "process": self.process.सूची(),

            "system": self.sys.जानकारी()

        }
