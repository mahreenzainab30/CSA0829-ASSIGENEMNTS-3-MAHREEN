
import random
import timeit
import sys


# Sample temperature readings recorded every minute
readings = [
    4.5, 5.2, 9.1, 7.0, 55.0,
    -60.0, 3.8, 10.5, 6.4, 1.5,
    8.0, 2.0, 52.0, -51.0, 5.5
]


# -------------------------------------------------
# METHOD 1: Using for loop and append()
# -------------------------------------------------
def clean_with_loop(data):
    valid_celsius = []

    for temp in data:
        if -50 <= temp <= 50:
            valid_celsius.append(temp)

    fahrenheit = []

    for temp in valid_celsius:
        fahrenheit.append((temp * 9 / 5) + 32)

    return valid_celsius, fahrenheit


# -------------------------------------------------
# METHOD 2: Using list comprehension
# -------------------------------------------------
def clean_with_comprehension(data):
    valid_celsius = [temp for temp in data if -50 <= temp <= 50]

    fahrenheit = [(temp * 9 / 5) + 32 for temp in valid_celsius]

    return valid_celsius, fahrenheit


# -------------------------------------------------
# METHOD 3: Using filter(), map() and lambda
# -------------------------------------------------
def clean_with_map_filter(data):
    valid_celsius = list(filter(lambda temp: -50 <= temp <= 50, data))

    fahrenheit = list(map(lambda temp: (temp * 9 / 5) + 32,
                           valid_celsius))

    return valid_celsius, fahrenheit


# -------------------------------------------------
# FIND ALARM MINUTES USING enumerate()
# Safe range: 2°C to 8°C
# Minute numbering starts from 1
# Sensor errors are excluded from alarm calculation
# -------------------------------------------------
alarm_minutes = [
    minute
    for minute, temp in enumerate(readings, start=1)
    if -50 <= temp <= 50 and not (2 <= temp <= 8)
]


# -------------------------------------------------
# DISPLAY RESULTS
# -------------------------------------------------
loop_result = clean_with_loop(readings)
comprehension_result = clean_with_comprehension(readings)
map_result = clean_with_map_filter(readings)

print("ORIGINAL SENSOR READINGS:")
print(readings)

print("\nVALID CELSIUS READINGS:")
print(comprehension_result[0])

print("\nCONVERTED FAHRENHEIT READINGS:")
print([round(value, 2) for value in comprehension_result[1]])

print("\nALARM MINUTES:")
print(alarm_minutes)

print("\nVERIFICATION OF THREE METHODS:")
print("Loop and comprehension:", loop_result == comprehension_result)
print("Comprehension and map/filter:", comprehension_result == map_result)


# -------------------------------------------------
# TEST ALL-VALID AND ALL-INVALID READINGS
# -------------------------------------------------
all_valid = [2, 3, 4, 5, 6, 7, 8]
all_invalid = [55, -60, 80, -75]

print("\nEDGE CASE TESTS:")
print("All-valid result:", clean_with_comprehension(all_valid))
print("All-invalid result:", clean_with_comprehension(all_invalid))


# -------------------------------------------------
# EXPERIMENT: TIME THREE METHODS
# -------------------------------------------------
print("\nTIMING EXPERIMENT")

for size in [10000, 100000, 1000000]:
    random.seed(42)
    test_data = [random.uniform(-60, 60) for _ in range(size)]

    loop_time = timeit.timeit(
        lambda: clean_with_loop(test_data), number=3
    )

    comprehension_time = timeit.timeit(
        lambda: clean_with_comprehension(test_data), number=3
    )

    map_time = timeit.timeit(
        lambda: clean_with_map_filter(test_data), number=3
    )

    print(f"\nNumber of readings: {size}")
    print(f"For loop: {loop_time:.6f} seconds")
    print(f"List comprehension: {comprehension_time:.6f} seconds")
    print(f"Map and filter: {map_time:.6f} seconds")


# -------------------------------------------------
# MEMORY COMPARISON
# -------------------------------------------------
valid_list = [temp for temp in readings if -50 <= temp <= 50]
valid_generator = (temp for temp in readings if -50 <= temp <= 50)

print("\nMEMORY COMPARISON:")
print("List comprehension memory:", sys.getsizeof(valid_list), "bytes")
print("Generator expression memory:", sys.getsizeof(valid_generator), "bytes")


# -------------------------------------------------
# DICTIONARY AND SET COMPREHENSIONS
# -------------------------------------------------
fahrenheit_dictionary = {
    temp: round((temp * 9 / 5) + 32, 2)
    for temp in valid_list
}

unique_temperatures = {temp for temp in valid_list}

print("\nDICTIONARY COMPREHENSION:")
print(fahrenheit_dictionary)

print("\nSET COMPREHENSION:")
print(unique_temperatures)
