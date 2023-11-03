#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    int i;
    int a;
    int b;
    
    i = 0;
    a = 0;
    b = 1;
    while ((i < 42))
    {
        a = ((b = (a + b)) - a);
        i = (i + 1);
    }
    printf("%d\n", a);
    return 0;
}
