#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CMD 100

void initialize_memory()
{
    printf("स्मृति प्रारंभ\n");
}

void initialize_cpu()
{
    printf("CPU प्रारंभ\n");
}

void initialize_vm()
{
    printf("VM प्रारंभ\n");
}

void shell()
{
    char cmd[MAX_CMD];

    while (1)
    {
        printf("सूत्र> ");

        fgets(cmd, MAX_CMD, stdin);

        cmd[strcspn(cmd, "\n")] = 0;

        if (strcmp(cmd, "exit") == 0)
        {
            break;
        }

        else if (strcmp(cmd, "स्थिति") == 0)
        {
            printf("सूत्र Kernel सक्रिय\n");
        }

        else if (strncmp(cmd, "चलाओ ", 6) == 0)
        {
            char *file = cmd + 6;

            char exec_cmd[200];

            sprintf(exec_cmd, "../native_vm/sutra_vm %s", file);

            system(exec_cmd);
        }

        else
        {
            printf("अज्ञात आदेश\n");
        }
    }
}

int main()
{
    printf("सूत्र Kernel प्रारंभ\n");

    initialize_memory();

    initialize_cpu();

    initialize_vm();

    shell();

    printf("सूत्र Kernel समाप्त\n");

    return 0;
}
