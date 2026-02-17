#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 256

void compile(char *input, char *output)
{
    FILE *in = fopen(input, "r");
    FILE *out = fopen(output, "w");

    if (!in || !out)
    {
        printf("त्रुटि: file नहीं खुला\n");
        return;
    }

    fprintf(out, "#include <stdio.h>\n");
    fprintf(out, "int main(){\n");

    char line[MAX_LINE];

    while (fgets(line, sizeof(line), in))
    {
        char instruction[50];
        char arg1[50];
        char arg2[50];

        int count = sscanf(line, "%s %s %s", instruction, arg1, arg2);

        if (count >= 1)
        {
            if (strcmp(instruction, "पाठ") == 0)
            {
                fprintf(out, "printf(\"%s\\n\");\n", arg1);
            }

            if (strcmp(instruction, "स्थापित") == 0)
            {
                fprintf(out, "int %s=%s;\n", arg1, arg2);
            }

            if (strcmp(instruction, "प्रदर्शित") == 0)
            {
                fprintf(out, "printf(\"%%d\\n\", %s);\n", arg1);
            }
        }
    }

    fprintf(out, "return 0;\n}\n");

    fclose(in);
    fclose(out);

    printf("Native source निर्मित\n");
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        printf("उपयोग: sutra_compiler input.sutra output.c\n");
        return 1;
    }

    compile(argv[1], argv[2]);

    return 0;
}
