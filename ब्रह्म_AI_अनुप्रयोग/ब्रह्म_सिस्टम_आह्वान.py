# ब्रह्म सिस्टम आह्वान (System Call Layer)

import os
import time


class ब्रह्मसिस्टमआह्वान:

    def __init__(self):

        print("🕉️ ब्रह्म सिस्टम आह्वान सक्रिय")


    # file read
    def पढ़ो(self, path):

        try:

            with open(path, "r", encoding="utf-8") as f:

                data = f.read()

            return {
                "status": "success",
                "data": data
            }

        except Exception as e:

            return {
                "status": "error",
                "error": str(e)
            }


    # file write
    def लिखो(self, path, data):

        try:

            with open(path, "w", encoding="utf-8") as f:

                f.write(data)

            return {
                "status": "success"
            }

        except Exception as e:

            return {
                "status": "error",
                "error": str(e)
            }


    # create directory
    def निर्देशिका_बनाओ(self, path):

        try:

            os.makedirs(path, exist_ok=True)

            return {
                "status": "success"
            }

        except Exception as e:

            return {
                "status": "error",
                "error": str(e)
            }


    # list directory
    def सूची(self, path):

        try:

            files = os.listdir(path)

            return {
                "status": "success",
                "files": files
            }

        except Exception as e:

            return {
                "status": "error",
                "error": str(e)
            }


    # delete file
    def हटाओ(self, path):

        try:

            os.remove(path)

            return {
                "status": "success"
            }

        except Exception as e:

            return {
                "status": "error",
                "error": str(e)
            }


    # execute command
    def आदेश(self, cmd):

        try:

            result = os.popen(cmd).read()

            return {
                "status": "success",
                "output": result
            }

        except Exception as e:

            return {
                "status": "error",
                "error": str(e)
            }


    # system info
    def जानकारी(self):

        return {

            "time": time.ctime(),

            "cwd": os.getcwd(),

            "platform": os.name
        }
