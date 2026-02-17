# 🕉️ सूत्र पूर्ण आभासी यन्त्र

import सूत्र_सीपीयू_तंत्र as cpu
import सूत्र_स्मृति_तंत्र as स्मृति
import सूत्र_सञ्चिका_तंत्र as disk
import सूत्र_यन्त्र_प्रबंधक as device
import सूत्र_व्यवधान_तंत्र as interrupt
import सूत्र_बस_तंत्र as bus
import सूत्र_घड़ी_तंत्र as clock


class सूत्रपूर्णयन्त्र:


    def __init__(self):

        print("🕉️ सूत्र पूर्ण आभासी यन्त्र सक्रिय")

        self.cpu = cpu.सूत्रसीपीयू()

        self.memory = स्मृति.सूत्रस्मृति()

        self.disk = disk.सूत्रसञ्चिका()

        self.device = device.सूत्रयन्त्रप्रबंधक()

        self.interrupt = interrupt.सूत्रव्यवधान()

        self.bus = bus.सूत्रबस()

        self.clock = clock.सूत्रघड़ी()


    def परीक्षण(self):

        self.device.पंजीकरण("प्रदर्शन")

        self.device.पंजीकरण("संग्रहण")

        self.device.सूची()

        self.cpu.स्थापय("अ",50)

        self.cpu.स्थापय("ब",70)

        self.cpu.योग("अ","ब")

        self.cpu.दर्शय()

        self.memory.लेखन(10,1234)

        self.memory.पठन(10)

        self.disk.निर्माण("data")

        self.disk.लेखन("data","सूत्र")

        print(self.disk.पठन("data"))

        self.bus.प्रेषण("CPU","Memory",999)

        self.interrupt.उत्पन्न("I/O")

        self.clock.समय()
