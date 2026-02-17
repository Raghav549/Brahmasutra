# ब्रह्म रनटाइम तंत्र
# VERSION 50

import os
import runpy

from ब्रह्म_AI_अनुप्रयोग.ब्रह्म_अनुप्रयोग_पंजी import ब्रह्मअनुप्रयोगपंजी


class ब्रह्मरनटाइम:

    def __init__(self):

        self.पंजी = ब्रह्मअनुप्रयोगपंजी()

        self.चल_रहे = {}

    def चलाओ(self, नाम):

        ऐप = self.पंजी.प्राप्त(नाम)

        if not ऐप:

            return {
                "status": "error",
                "message": "app not found"
            }

        पथ = ऐप["path"]

        if not os.path.exists(पथ):

            return {
                "status": "error",
                "message": "file missing"
            }

        try:

            runpy.run_path(
                पथ,
                run_name="__main__"
            )

            self.चल_रहे[नाम] = "running"

            return {
                "status": "success",
                "message": f"{नाम} executed"
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }

    def स्थिति(self, नाम):

        return self.चल_रहे.get(
            नाम,
            "not running"
        )

    def सूची(self):

        return self.चल_रहे
