#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_REG 4
#define MAX_LINE 256

int registers[MAX_REG];

void execute(char *filename)
{
    FILE *file = fopen(filename, "r");

    if (!file)
    {
        printf("त्रुटि: file नहीं मिला\n");
        return;
    }

    char line[MAX_LINE];

    printf("सूत्र Native VM प्रारंभ\n");

    while (fgets(line, sizeof(line), file))
    {
        char instruction[50];
        char arg1[50];
        char arg2[50];

        int count = sscanf(line, "%s %s %s", instruction, arg1, arg2);

        if (count >= 1)
        {
            if (strcmp(instruction, "स्थापित") == 0)
            {
                int reg = arg1[1] - '1';
                int value = atoi(arg2);
                registers[reg] = value;
            }

            else if (strcmp(instruction, "प्रदर्शित") == 0)
            {
                int reg = arg1[1] - '1';
                printf("%d\n", registers[reg]);
            }

            else if (strcmp(instruction, "वृद्धि") == 0)
            {
                int reg = arg1[1] - '1';
                int value = atoi(arg2);
                registers[reg] += value;
            }
        }
    }

    fclose(file);

    printf("सूत्र Native VM समाप्त\n");
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("उपयोग: sutra_vm file.sbc\n");
        return 1;
    }

    execute(argv[1]);

    return 0;
}
