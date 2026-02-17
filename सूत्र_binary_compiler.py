# 🕉️ सूत्र Binary Compiler

import सूत्र_native_compiler as native
import सूत्र_binary_generator as binary


class सूत्रBinaryCompiler:


    def __init__(self):

        print("🕉️ सूत्र Binary Compiler सक्रिय")

        self.native_compiler = native.सूत्रNativeCompiler()

        self.binary_generator = binary.सूत्रBinaryGenerator()


    def compile(self, sutra_code, output_file):

        native_code = self.native_compiler.compile(sutra_code)

        self.binary_generator.generate(native_code, output_file)

        print("Binary Compilation पूर्ण")
