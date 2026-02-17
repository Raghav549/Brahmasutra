# ब्रह्म सार्वभौमिक जनक
# VERSION 121

import os
import json
import time

class ब्रह्मसार्वभौमिकजनक:

    def __init__(self, workspace):
        self.workspace = workspace
        print("ब्रह्म सार्वभौमिक जनक सक्रिय")

    # prompt analysis
    def विश्लेषण(self, prompt):

        prompt_lower = prompt.lower()

        analysis = {

            "app": "app" in prompt_lower,
            "website": "website" in prompt_lower,
            "mobile": "mobile" in prompt_lower,
            "backend": True,
            "frontend": True,
            "database": "database" in prompt_lower or "login" in prompt_lower,
            "login": "login" in prompt_lower,
            "dashboard": "dashboard" in prompt_lower,
            "api": True,
            "deployment": True,
            "ai": "ai" in prompt_lower,
            "saas": "saas" in prompt_lower,
            "cloud": "cloud" in prompt_lower

        }

        return analysis

    # architecture generate
    def संरचना_जनन(self, analysis):

        structure = {

            "backend": "python_server",
            "frontend": "html_ui",
            "database": "sqlite",
            "deployment": "local_server",
            "api": True

        }

        return structure

    # save plan
    def योजना_सहेज(self, prompt, analysis, structure):

        data = {

            "prompt": prompt,
            "analysis": analysis,
            "structure": structure,
            "timestamp": time.time()

        }

        path = os.path.join(self.workspace, "brahma_plan.json")

        with open(path, "w", encoding="utf-8") as f:

            json.dump(data, f, indent=4, ensure_ascii=False)

        print("योजना सहेजित:", path)

    # full generation pipeline
    def जनन(self, prompt):

        print("प्रॉम्प्ट प्राप्त")

        analysis = self.विश्लेषण(prompt)

        print("विश्लेषण पूर्ण")

        structure = self.संरचना_जनन(analysis)

        print("संरचना निर्मित")

        self.योजना_सहेज(prompt, analysis, structure)

        print("ब्रह्म जनन पूर्ण")

        return {

            "analysis": analysis,
            "structure": structure

        }
