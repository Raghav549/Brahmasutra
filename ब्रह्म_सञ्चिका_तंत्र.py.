import os


class ब्रह्मसञ्चिकातंत्र:


    def __init__(self):

        print("🕉️ ब्रह्म सञ्चिका तंत्र सक्रिय")

        self.root = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_भण्डार")

        if not os.path.exists(self.root):

            os.makedirs(self.root)


    def निर्माण(self,name):

        path = os.path.join(self.root,name)

        open(path,"w",encoding="utf-8").close()

        print("सञ्चिका निर्मित:",path)

        return path


    def लेखन(self,name,data):

        path = os.path.join(self.root,name)

        with open(path,"w",encoding="utf-8") as f:

            f.write(data)

        print("सञ्चिका लिखित:",path)


    def पठन(self,name):

        path = os.path.join(self.root,name)

        with open(path,"r",encoding="utf-8") as f:

            data = f.read()

        print("सञ्चिका पठन:",path)

        return data


    def सूची(self):

        files = os.listdir(self.root)

        print("सञ्चिका सूची:")

        for f in files:

            print("•",f)

        return files


    def विलोपन(self,name):

        path = os.path.join(self.root,name)

        os.remove(path)

        print("सञ्चिका हटाई:",path)
