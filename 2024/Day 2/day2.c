#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define MAX_LEVELS 20
#define MAX_REPORTS 1000

// Object to describe each line of input
typedef struct {
    int levels[MAX_LEVELS];
    int level_count;
} Report;

// Function to parse input into an array of reports
int parse_reports(const char *filename, Report *reports) {
  FILE *file = fopen(filename, "r");
  if (!file) {
    fprintf(stderr, "Error: Unable to open file %s\n", filename);
    return 0;
  }

  char line[512]; // Arbitrary limit
  int report_count = 0;

  while (fgets(line, sizeof(line), file) && report_count < MAX_REPORTS) {
    printf("Processing line: %s", line); // Debugging log
    Report *report = &reports[report_count];
    report->level_count = 0;

    char *token = strtok(line, " ");
    while (token && report->level_count < MAX_LEVELS) {
      report->levels[report->level_count++] = atoi(token);
      token = strtok(NULL, " ");
    }

    if (report->level_count > 0) {
      report_count++;
    } else {
      printf("Skipping empty or invalid line.\n"); // Debugging log
    }
  }

  fclose(file);
  printf("Total reports parsed: %d\n", report_count); // Debugging log
  return report_count;
}

// Function to check if a report is safe
bool is_safe_report(Report *report) {
  bool is_increasing = true;
  bool is_decreasing = true;

  printf("Checking report with %d levels: ", report->level_count);
  for (int i = 0; i < report->level_count; i++) {
    printf("%d ", report->levels[i]);
  }
  printf("\n");

  for (int i = 1; i < report->level_count; i++) {
    int diff = report->levels[i] - report->levels[i - 1];
    // printf("  Comparing levels %d and %d: diff = %d\n", report->levels[i - 1], report->levels[i], diff);

    // Check if the difference is invalid
    if (diff == 0 || diff < -3 || diff > 3) {
      printf("  -> Invalid difference: %d (not between -3 and 3, or no change). Report is unsafe.\n", diff);
      return false;
    }

    // Update flags for increasing and decreasing trends
    if (diff > 0) {
      is_decreasing = false; // If it increases, it's not fully decreasing
    } else if (diff < 0) {
      is_increasing = false; // If it decreases, it's not fully increasing
    }
  }

  // Final safety check
  if (is_increasing) {
    printf("  -> Report is safe: all levels are increasing.\n");
  } else if (is_decreasing) {
    printf("  -> Report is safe: all levels are decreasing.\n");
  } else {
    printf("  -> Report is unsafe: levels are neither consistently increasing nor decreasing.\n");
  }

  return is_increasing || is_decreasing;
}

// Function to check if a report is safe after removing one level
bool is_safe_with_dampener(Report *report) {
  for (int i = 0; i < report->level_count; i++) {
    Report modified_report;
    modified_report.level_count = 0;

    // Copy all levels except the one at index `i`
    for (int j = 0; j < report->level_count; j++) {
      if (j != i) {
        modified_report.levels[modified_report.level_count++] = report->levels[j];
      }
    }

    if (is_safe_report(&modified_report)) {
      return true; // Safe with one level removed
    }
  }
  return false;
}

int main() {
  Report reports[MAX_REPORTS];
  int report_count = parse_reports("input.txt", reports);

  printf("%d\n", report_count);

  if (report_count == 0) {
    printf("No reports found.\n");
    return 1;
  }

  int safe_count_part1 = 0;
  int safe_count_part2 = 0;

  for (int i = 0; i < report_count; i++) {
    // Part 1: Count directly safe reports
    if (is_safe_report(&reports[i])) {
      safe_count_part1++;
      safe_count_part2++; // Also counts for Part 2
    } else {
      // Part 2: Check if it becomes safe with the Problem Dampener
      if (is_safe_with_dampener(&reports[i])) {
        safe_count_part2++;
      }
    }
  }

  printf("\nPart 1\n");
  printf("Number of safe reports: %d\n", safe_count_part1);

  printf("\nPart 2\n");
  printf("Number of safe reports with Problem Dampener: %d\n", safe_count_part2);

  return 0;
}

