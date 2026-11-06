# ==============================================================================
# Author:      Delite Manawar
# Date:        November 4, 2026
# Course:      CPSC 50100 Programming Fundamentals
# Assignment:  Week 3 - Personal Fitness Tracker
# Tier:        Advanced (Base, Intermediate and Advanced levels completed)
# Description: Logs any number of workouts until the user types "done", reports
#              the rate and intensity of each one, then displays a workout
#              table, session statistics, an effort trend and a calorie goal
#              check.
#
# Design notes:
# - If every workout burns the same calories, the trend meets the definition of
#   both "Improving" and "Declining". This program reports "Improving".
# - Duration must be at least 1 minute, which prevents division by zero.
# - Workout names longer than the table column are shortened in the table only.
# ==============================================================================


# ------------------------------------------------------------------------------
# Input function
# ------------------------------------------------------------------------------

def get_whole_number(prompt, minimum=1):
    """Keep asking until the user enters a whole number at or above minimum."""
    while True:
        text = input(prompt).strip()
        is_valid = text != ""

        # Nested loop: check every character of the user's entry.
        for character in text:
            if character not in "0123456789":
                is_valid = False

        if is_valid and int(text) >= minimum:
            return int(text)

        print(f"Please enter a whole number of at least {minimum}.")


# ------------------------------------------------------------------------------
# Single-workout functions
# ------------------------------------------------------------------------------

def calories_per_minute(calories, duration):
    """Return the calories burned per minute, rounded to one decimal place."""
    return round(calories / duration, 1)


def get_intensity(rate):
    """Return the intensity label for a calories-per-minute rate."""
    if rate < 5.0:
        return "Low"
    elif rate < 10.0:
        return "Moderate"
    else:
        return "High"


# ------------------------------------------------------------------------------
# List functions
# ------------------------------------------------------------------------------

def calculate_total(values):
    """Return the sum of a list of numbers."""
    total = 0
    for value in values:
        total += value
    return total


def calculate_average(values):
    """Return the average of a list, rounded to one decimal place."""
    if len(values) == 0:
        return 0.0
    return round(calculate_total(values) / len(values), 1)


def find_best_workout(names, calories_list):
    """Return the highest-calorie workout; ties go to the one logged first."""
    best_index = 0
    for index in range(1, len(calories_list)):
        if calories_list[index] > calories_list[best_index]:
            best_index = index
    return names[best_index]


def analyze_trend(calories_list):
    """Return the direction of the calorie burn across consecutive workouts."""
    if len(calories_list) < 2:
        return "Not enough data"

    increases = 0
    decreases = 0

    # Compare each workout with the one logged before it.
    for index in range(1, len(calories_list)):
        if calories_list[index] > calories_list[index - 1]:
            increases += 1
        elif calories_list[index] < calories_list[index - 1]:
            decreases += 1

    if decreases == 0:
        return "Improving"
    elif increases == 0:
        return "Declining"
    else:
        return "Mixed"


# ------------------------------------------------------------------------------
# Output functions
# ------------------------------------------------------------------------------

def check_goal(total_calories, goal):
    """Return a message comparing the calories burned with the goal."""
    if total_calories >= goal:
        return f"Goal reached! You burned {total_calories} calories."
    else:
        calories_short = goal - total_calories
        return f"{calories_short} calories short of your {goal}-calorie goal."


def format_workout_row(name, duration, calories, width=20):
    """Return one formatted row of the workout table."""
    rate = calories_per_minute(calories, duration)
    intensity = get_intensity(rate)

    # Shorten long names so they cannot push the other columns out of line.
    table_name = name[:width]

    return (
        f"{table_name:<{width}}{duration:>10}{calories:>10}"
        f"{rate:>7.1f} c/m  {intensity}"
    )


def print_workout_table(names, durations, calories_list):
    """Print a table of every logged workout."""
    header = f"{'Workout':<20}{'Duration':>10}{'Calories':>10}{'Rate':>11}  Intensity"
    print(header)
    print("-" * len(header))

    for index in range(len(names)):
        print(format_workout_row(names[index], durations[index], calories_list[index]))


def print_session_summary(names, durations, calories_list, goal):
    """Print the workout table and all session statistics."""
    total_calories = calculate_total(calories_list)

    print("\n===== Workout Table =====")
    print_workout_table(names, durations, calories_list)

    print("\n===== Session Summary =====")
    print(f"{'Workouts logged':<16}: {len(names)}")
    print(f"{'Total calories':<16}: {total_calories}")
    print(f"{'Avg calories':<16}: {calculate_average(calories_list)}")
    print(f"{'Avg duration':<16}: {calculate_average(durations)} min")
    print(f"{'Best workout':<16}: {find_best_workout(names, calories_list)}")
    print(f"{'Effort trend':<16}: {analyze_trend(calories_list)}")
    print(f"{'Goal check':<16}: {check_goal(total_calories, goal)}")
    print("===========================")


# ------------------------------------------------------------------------------
# Main program
# ------------------------------------------------------------------------------

print("Welcome to the Personal Fitness Tracker!")
print("Log as many workouts as you like, then type 'done' as the workout name.")

calorie_goal = get_whole_number("Daily calorie burn goal: ")

# Parallel lists: the same index refers to the same workout in all three lists.
workout_names = []
workout_durations = []
workout_calories = []

# Collect workouts until the user enters the sentinel value "done".
while True:
    print(f"\n--- Workout {len(workout_names) + 1} ---")
    workout_name = input("Workout name (or 'done' to finish): ").strip()

    if workout_name.lower() == "done":
        break

    duration_minutes = get_whole_number("Duration (minutes): ")
    calories_burned = get_whole_number("Calories burned: ", 0)

    workout_names.append(workout_name)
    workout_durations.append(duration_minutes)
    workout_calories.append(calories_burned)

    workout_rate = calories_per_minute(calories_burned, duration_minutes)
    workout_intensity = get_intensity(workout_rate)
    print(
        f"Result: {workout_name} | {duration_minutes} min | {calories_burned} cal | "
        f"{workout_rate} cal/min | Intensity: {workout_intensity}"
    )

# Show the summary only if at least one workout was logged.
if len(workout_names) == 0:
    print("\nNo workouts were logged.")
else:
    print_session_summary(
        workout_names, workout_durations, workout_calories, calorie_goal
    )
    print("All workouts logged. Great job staying active!")
