#include <stdio.h>
#define MAX_MEASUREMENTS 5000 // Adjust as needed based on input size


// The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing
// with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.
//
// To do this, count the number of times a depth measurement increases from the previous measurement.
// (There is no measurement before the first measurement.)

// Function to count depth increases
int count_increases(const int *depths, int count) {
    int increases = 0;

    for (int i = 1; i < count; i++) {
        if (depths[i] > depths[i - 1]) {
            increases++;
        }
    }

    return increases;
}

// Function to count increases in the three-measurement sliding window
int count_sliding_window_increases(const int *depths, int count) {
    if (count < 3) {
        return 0; // Not enough measurements for a sliding window
    }

    int increases = 0;
    int previous_sum = depths[0] + depths[1] + depths[2];

    for (int i = 3; i < count; i++) {
        int current_sum = previous_sum - depths[i - 3] + depths[i];
        if (current_sum > previous_sum) {
            increases++;
        }
        previous_sum = current_sum;
    }

    return increases;
}

int main() {
    int depths[MAX_MEASUREMENTS];
    int count = 0;

    // Read input file
    FILE *file = fopen("input.txt", "r");
    if (file == NULL) {
        printf("Error: Unable to open input file.\n");
        return 1;
    }

    // Parse depths from the file
    while (fscanf(file, "%d", &depths[count]) != EOF && count < MAX_MEASUREMENTS) {
        count++;
    }

    fclose(file);

    // Calculate and print the result for part one
    int increases = count_increases(depths, count);
    printf("Number of depth increases: %d\n", increases);

    // Calculate and print the result for part two
    int sliding_window_increases = count_sliding_window_increases(depths, count);
    printf("Number of sliding window increases: %d\n", sliding_window_increases);

    return 0;
}
