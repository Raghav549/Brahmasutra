from ब्रह्म_संस्कृत_अनुप्रयोग_प्रक्षेपक import ब्रह्मअनुप्रयोगप्रक्षेपक


class ब्रह्मअनुप्रयोगप्रबंधक:


    def __init__(self):

        self.launcher = ब्रह्मअनुप्रयोगप्रक्षेपक()

        self.installed_apps = {}

        print("ब्रह्म अनुप्रयोग प्रबंधक सक्रिय")



    # स्थापना (INSTALL)
    def स्थापना(self, path):

        import os

        app_name = os.path.basename(path)

        self.installed_apps[app_name] = path

        print("स्थापित:", app_name)

        return True



    # निष्पादन (EXECUTE)
    def निष्पादन(self, app_name):

        if app_name not in self.installed_apps:

            print("त्रुटि: अनुप्रयोग स्थापित नहीं")

            return False

        path = self.installed_apps[app_name]

        print("अनुप्रयोग निष्पादन:", app_name)

        return self.launcher.प्रक्षेपित(path)



    # सूची
    def सूची(self):

        print("स्थापित अनुप्रयोग:")

        for app in self.installed_apps:

            print(app)
