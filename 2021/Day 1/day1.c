#include <stdio.h>

// The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing
// with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.
//
// To do this, count the number of times a depth measurement increases from the previous measurement.
// (There is no measurement before the first measurement.)

int main() {
    FILE *fileinput;

    fileinput = fopen("./input.txt","r");
    fprintf(fileinput, "This is testing my file reading \n");
    fclose(fileinput);
}