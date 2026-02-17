# 🕉️ ब्रह्म अनुप्रयोग इंजन VERSION 46

import os
import importlib.util

class ब्रह्मअनुप्रयोगइंजन:

    def __init__(self):

        self.स्थापित_पथ = os.path.expanduser("~/सूत्र-तंत्र/ब्रह्म_स्थापित")

        if not os.path.exists(self.स्थापित_पथ):
            os.makedirs(self.स्थापित_पथ)

        print("🕉️ ब्रह्म अनुप्रयोग इंजन सक्रिय")


    def सूची(self):

        apps = os.listdir(self.स्थापित_पथ)

        return {
            "status": "success",
            "apps": apps
        }


    def निष्पादन(self, app_name):

        app_path = os.path.join(self.स्थापित_पथ, app_name)

        if not os.path.exists(app_path):
            return {
                "status": "error",
                "message": "अनुप्रयोग नहीं मिला"
            }

        try:

            spec = importlib.util.spec_from_file_location(
                "app",
                app_path
            )

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

            if hasattr(module, "प्रारंभ"):

                result = module.प्रारंभ()

                return {
                    "status": "success",
                    "result": result
                }

            else:

                return {
                    "status": "error",
                    "message": "प्रारंभ function नहीं मिला"
                }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }


    def स्थापना(self, source_path):

        if not os.path.exists(source_path):

            return {
                "status": "error",
                "message": "source नहीं मिला"
            }

        filename = os.path.basename(source_path)

        dest = os.path.join(self.स्थापित_पथ, filename)

        import shutil

        shutil.copy(source_path, dest)

        return {
            "status": "success",
            "installed": filename
        }
