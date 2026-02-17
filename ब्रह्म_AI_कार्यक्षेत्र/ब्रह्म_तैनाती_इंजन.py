import os

from ब्रह्म_अनुप्रयोग_प्रबंधक import ब्रह्मअनुप्रयोगप्रबंधक
from ब्रह्म_HTTP_इंजन import प्रारंभ as HTTP_प्रारंभ


class ब्रह्मतैनातीइंजन:


    def __init__(self):

        self.manager = ब्रह्मअनुप्रयोगप्रबंधक()

        print("ब्रह्म तैनाती इंजन सक्रिय")



    def तैनात(self, app_path):

        if not os.path.exists(app_path):

            print("त्रुटि: अनुप्रयोग पथ नहीं मिला")
            return


        app_name = os.path.basename(app_path)


        print("स्थापना प्रारंभ:", app_name)


        self.manager.स्थापना(app_path)


        print("निष्पादन प्रारंभ:", app_name)


        self.manager.निष्पादन(app_name)


        print("सर्वर प्रारंभ")


        HTTP_प्रारंभ()


        print("पूर्ण तैनाती सफल:", app_name)
