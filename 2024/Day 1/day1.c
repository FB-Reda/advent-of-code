#include <stdio.h>
#include <stdlib.h>

#define MAX_LINES 1000 // Adjust as needed
#define MAX_VALUE 1000000 // Adjust based on the range of input numbers

// Comparator function for qsort
int compare(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

// Function to parse and sort columns
void parse_and_sort(const char *filename, int *column1, int *column2, int *count) {
    FILE *file = fopen(filename, "r");
    if (file == NULL) {
        printf("Error opening file!\n");
        exit(1);
    }

    *count = 0;

    // Read lines from the file
    while (!feof(file) && *count < MAX_LINES) {
        if (fscanf(file, "%d %d", &column1[*count], &column2[*count]) == 2) {
            (*count)++;
        }
    }

    fclose(file);

    // Sort the columns
    qsort(column1, *count, sizeof(int), compare);
    qsort(column2, *count, sizeof(int), compare);
}

// Function to compute the sum of absolute differences
int sum_of_absolute_differences(int *column1, int *column2, int count) {
    int sum = 0;
    for (int i = 0; i < count; i++) {
        sum += abs(column1[i] - column2[i]);
    }
    return sum;
}

// Function to calculate the total similarity score
long long calculate_similarity_score(int *column1, int *column2, int count) {
    int frequency[MAX_VALUE] = {0};
    long long score = 0;

    // Count occurrences of each number in column2
    for (int i = 0; i < count; i++) {
        if (column2[i] < MAX_VALUE) { // Ensure index is within bounds
            frequency[column2[i]]++;
        }
    }

    // Calculate the similarity score
    for (int i = 0; i < count; i++) {
        if (column1[i] < MAX_VALUE) { // Ensure index is within bounds
            score += (long long)column1[i] * frequency[column1[i]];
        }
    }

    return score;
}

int main() {
    int column1[MAX_LINES], column2[MAX_LINES];
    int count;

    // Call the function to parse and sort
    parse_and_sort("input.txt", column1, column2, &count);

    // Compute the sum of absolute differences
    int difference_sum = sum_of_absolute_differences(column1, column2, count);

    // Calculate the similarity score
    long long similarity_score = calculate_similarity_score(column1, column2, count);


    // Print sorted columns and the result
    // printf("Column 1 (sorted):\n");
    // for (int i = 0; i < count; i++) {
    //     printf("%d\n", column1[i]);
    // }

    // printf("\nColumn 2 (sorted):\n");
    // for (int i = 0; i < count; i++) {
    //     printf("%d\n", column2[i]);
    // }

    printf("\nSum of absolute differences: %d\n", difference_sum);

    printf("Total similarity score: %lld\n", similarity_score);

    return 0;
}
