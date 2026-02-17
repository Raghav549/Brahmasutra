import os
import json


class ब्रह्मअनुप्रयोगपंजी:


    def __init__(self):

        self.registry_file = os.path.expanduser(
            "~/सूत्र-तंत्र/ब्रह्म_AI_कार्यक्षेत्र/app_registry.json"
        )


        if not os.path.exists(self.registry_file):

            with open(self.registry_file, "w") as f:

                json.dump({}, f)


        print("ब्रह्म अनुप्रयोग पंजी तंत्र सक्रिय")



    def पंजीकरण(self, app_name, app_path):

        registry = self._load()


        registry[app_name] = app_path


        self._save(registry)


        print("पंजीकृत:", app_name)



    def पथ(self, app_name):

        registry = self._load()


        return registry.get(app_name)



    def सूची(self):

        registry = self._load()


        return list(registry.keys())



    def _load(self):

        with open(self.registry_file, "r") as f:

            return json.load(f)



    def _save(self, data):

        with open(self.registry_file, "w") as f:

            json.dump(data, f, indent=4)
