#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 256

void write_header(FILE *out)
{
    fprintf(out, "#!/data/data/com.termux/files/usr/bin/sh\n");
}

void compile_direct(char *input, char *output)
{
    FILE *in = fopen(input, "r");
    FILE *out = fopen(output, "w");

    if (!in || !out)
    {
        printf("त्रुटि\n");
        return;
    }

    write_header(out);

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
                fprintf(out, "echo %s\n", arg1);
            }

            else if (strcmp(instruction, "प्रदर्शित") == 0)
            {
                fprintf(out, "echo $%s\n", arg1);
            }

            else if (strcmp(instruction, "स्थापित") == 0)
            {
                fprintf(out, "%s=%s\n", arg1, arg2);
            }
        }
    }

    fclose(in);
    fclose(out);

    printf("Direct binary निर्मित\n");
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        printf("उपयोग\n");
        return 1;
    }

    compile_direct(argv[1], argv[2]);

    return 0;
}
