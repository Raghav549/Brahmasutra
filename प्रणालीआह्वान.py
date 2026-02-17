# सूत्र तंत्र — प्रणाली आह्वान प्रणाली
# Sanskrit System Call Interface

print("प्रणाली आह्वान प्रणाली आरम्भ")

# system call registry
आह्वानसूची = {}



# register system call
def आह्वान_पंजीकरण(नाम, कार्य):

    आह्वानसूची[नाम] = कार्य

    print("आह्वान पंजीकृत:", नाम)



# execute system call
def आह्वान_चलाओ(नाम, पैरामीटर=None):

    if नाम not in आह्वानसूची:

        print("त्रुटि: आह्वान नहीं मिला")

        return

    कार्य = आह्वानसूची[नाम]

    if पैरामीटर == None:

        return कार्य()

    else:

        return कार्य(पैरामीटर)



# example system calls

def नमस्ते():

    print("नमस्ते सूत्र तंत्र")



def जोड़(मान):

    परिणाम = मान + मान

    print("परिणाम:", परिणाम)

    return परिणाम



# register calls
आह्वान_पंजीकरण("नमस्ते", नमस्ते)

आह्वान_पंजीकरण("जोड़", जोड़)



# execute calls
आह्वान_चलाओ("नमस्ते")

आह्वान_चलाओ("जोड़", 5)



print("प्रणाली आह्वान सक्रिय")
