
import random
import time
import sys

# Q1: Daily Rainfall Records

# 1. Generate rainfall readings for 365 days
random.seed(42)
readings = [round(random.uniform(0, 30), 2) for _ in range(365)]

# Include some dry days
for i in range(0, 365, 25):
    readings[i] = 0.0

print("DAILY RAINFALL ANALYSIS")
print("-" * 40)

# 2. Calculate weekly rainfall totals using slicing
weekly_totals = []

for i in range(0, len(readings), 7):
    week_total = sum(readings[i:i + 7])
    weekly_totals.append(round(week_total, 2))

print("Total number of weeks:", len(weekly_totals))
print("Weekly rainfall totals:", weekly_totals)

# 3. Find wettest and driest weeks
wettest_week = weekly_totals.index(max(weekly_totals)) + 1
driest_week = weekly_totals.index(min(weekly_totals)) + 1

print("Wettest week:", wettest_week)
print("Highest weekly rainfall:", max(weekly_totals), "mm")

print("Driest week:", driest_week)
print("Lowest weekly rainfall:", min(weekly_totals), "mm")

# 4. Find maximum and minimum daily rainfall
max_rain = max(readings)
min_rain = min(readings)

print("Maximum daily rainfall:", max_rain, "mm")
print("Maximum rainfall day:", readings.index(max_rain) + 1)

print("Minimum daily rainfall:", min_rain, "mm")
print("Minimum rainfall day:", readings.index(min_rain) + 1)

# 5. Calculate 7-day moving average using naive method
def naive_average(data):
    averages = []

    for i in range(len(data) - 6):
        avg = sum(data[i:i + 7]) / 7
        averages.append(round(avg, 2))

    return averages

# 6. Calculate moving average using running sum
def running_average(data):
    averages = []

    if len(data) < 7:
        return averages

    current_sum = sum(data[:7])
    averages.append(round(current_sum / 7, 2))

    for i in range(7, len(data)):
        current_sum = current_sum - data[i - 7] + data[i]
        averages.append(round(current_sum / 7, 2))

    return averages

# 7. Display moving averages
naive_result = naive_average(readings)
running_result = running_average(readings)

print("Number of 7-day averages:", len(naive_result))
print("First five moving averages:", naive_result[:5])
print("Both methods give same result:",
      naive_result == running_result)

# 8. Identify dry days
dry_days = []

for i in range(len(readings)):
    if readings[i] == 0:
        dry_days.append(i + 1)

print("Dry days:", dry_days)

# 9. Demonstrate list slicing
print("readings[7:14]:", readings[7:14])
print("readings[-7:]:", readings[-7:])
print("readings[::7]:", readings[::7])

# 10. Experimental investigation
print("\nEXPERIMENTAL INVESTIGATION")
print("-" * 40)

for size in [365, 36500, 365000]:
    data = [random.uniform(0, 30) for _ in range(size)]

    start = time.perf_counter()
    naive_average(data)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    running_average(data)
    running_time = time.perf_counter() - start

    print("\nDataset size:", size)
    print("Naive method time:", round(naive_time, 6), "seconds")
    print("Running sum time:", round(running_time, 6), "seconds")

# 11. Edge case testing
print("\nEDGE CASE TESTING")

print("Empty list:", naive_average([]))
print("List shorter than 7:", naive_average([2, 4, 6]))

# 12. List memory measurement
print("\nMemory occupied by rainfall list:",
      sys.getsizeof(readings), "bytes")
