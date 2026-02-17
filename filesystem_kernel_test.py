from सूत्र_kernel_filesystem import सूत्रKernelFileSystem


fs = सूत्रKernelFileSystem()


fs.create("app1.सूत्र", "print('Sanskrit App 1')")
fs.create("app2.सूत्र", "print('Sanskrit App 2')")


fs.list()


fs.read("app1.सूत्र")
