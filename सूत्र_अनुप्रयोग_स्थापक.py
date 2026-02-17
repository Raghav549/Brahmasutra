import os
import shutil

class अनुप्रयोगस्थापक:

    def __init__(self):

        self.स्थापना_पथ = os.path.expanduser("~/सूत्र-तंत्र/स्थापित_अनुप्रयोग")

        if not os.path.exists(self.स्थापना_पथ):
            os.makedirs(self.स्थापना_पथ)

        print("🕉️ सूत्र अनुप्रयोग स्थापक सक्रिय")


    def स्थापना(self, स्रोत):

        नाम = os.path.basename(स्रोत)

        गंतव्य = os.path.join(self.स्थापना_पथ, नाम)

        shutil.copy(स्रोत, गंतव्य)

        print("स्थापित:", नाम)


    def सूची(self):

        print("स्थापित अनुप्रयोग:")

        for f in os.listdir(self.स्थापना_पथ):

            print("•", f)


    def निष्कासन(self, नाम):

        पथ = os.path.join(self.स्थापना_पथ, नाम)

        if os.path.exists(पथ):

            os.remove(पथ)

            print("निष्कासित:", नाम)

        else:

            print("अनुप्रयोग नहीं मिला")


    def निष्पादन(self, नाम):

        from सूत्र_अनुप्रयोग_लोडर import अनुप्रयोगलोडर

        पथ = os.path.join(self.स्थापना_पथ, नाम)

        if os.path.exists(पथ):

            loader = अनुप्रयोगलोडर()

            loader.निष्पादन(पथ)

        else:

            print("अनुप्रयोग नहीं मिला")
