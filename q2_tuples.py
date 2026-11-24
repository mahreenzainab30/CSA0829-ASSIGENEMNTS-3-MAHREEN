
import copy
import sys
import timeit

print("Q2 - TUPLES, MUTABILITY AND COPYING")
print("=" * 50)

# 1. Create a bus-stop dictionary using tuple keys

stops = {
    (13.0827, 80.2707): "Chennai Central",
    (13.0418, 80.2341): "T. Nagar",
    (13.0674, 80.2376): "Nungambakkam",
    (13.0569, 80.2425): "Teynampet"
}

print("\nBUS STOP DETAILS")

for (latitude, longitude), name in stops.items():
    print(name, ":", latitude, longitude)


# 2. Create a passenger zone grid correctly

rows, cols = 3, 4

bad = [[0] * cols] * rows
bad[0][1] = 7

# Correct grid using list comprehension
good = [[0 for j in range(cols)] for i in range(rows)]

good[0][1] = 7

print("\nGRID COMPARISON")
print("Bad grid :", bad)
print("Good grid:", good)

print("Bad rows are same object:", bad[0] is bad[1])
print("Good rows are same object:", good[0] is good[1])


# 3. Demonstrate aliasing

print("\nALIASING")

original = [10, 20, 30]
alias = original

alias[0] = 100

print("Original:", original)
print("Alias:", alias)
print("Same object:", original is alias)
print("Original ID:", id(original))
print("Alias ID:", id(alias))


# 4. Demonstrate shallow copying

print("\nSHALLOW COPYING")

original_list = [[1, 2], [3, 4]]

copy_method = copy.copy(original_list)
slice_copy = original_list[:]

original_list[0][0] = 99

print("Original:", original_list)
print("Copy.copy():", copy_method)
print("Slicing copy:", slice_copy)
print("Outer objects same:", original_list is copy_method)
print("Inner objects same:", original_list[0] is copy_method[0])


# 5. Demonstrate deep copying

print("\nDEEP COPYING")

original_data = [[1, 2], [3, 4]]

deep_copy = copy.deepcopy(original_data)

original_data[0][0] = 500

print("Original:", original_data)
print("Deep copy:", deep_copy)
print("Inner objects same:", original_data[0] is deep_copy[0])


# 6. Demonstrate tuple unpacking

print("\nTUPLE UNPACKING")

bus_stops = [
    ("Chennai Central", 13.0827, 80.2707),
    ("T. Nagar", 13.0418, 80.2341),
    ("Teynampet", 13.0569, 80.2425)
]

for name, latitude, longitude in bus_stops:
    print("Stop:", name)
    print("Latitude:", latitude)
    print("Longitude:", longitude)


# 7. Demonstrate that lists cannot be dictionary keys

print("\nDICTIONARY KEY TEST")

try:
    location = {[13.0418, 80.2341]: "T. Nagar"}
except TypeError as error:
    print("Error:", error)


# 8. Test changing a list stored inside a tuple

print("\nLIST INSIDE A TUPLE")

data = ("Passenger details", [10, 20, 30])

data[1].append(40)

print("Updated tuple:", data)

# Reassigning a tuple element is not allowed
try:
    data[1] = [50, 60]
except TypeError as error:
    print("Error:", error)


# 9. Compare memory of a list and tuple with 1 million values

print("\nMEMORY COMPARISON")

values_list = list(range(1000000))
values_tuple = tuple(range(1000000))

list_memory = sys.getsizeof(values_list)
tuple_memory = sys.getsizeof(values_tuple)

print("List memory:", list_memory, "bytes")
print("Tuple memory:", tuple_memory, "bytes")


# 10. Compare creation time

print("\nCREATION TIME COMPARISON")

list_creation = timeit.timeit(
    "list(range(100000))",
    number=5
)

tuple_creation = timeit.timeit(
    "tuple(range(100000))",
    number=5
)

print("List creation time:", round(list_creation, 6), "seconds")
print("Tuple creation time:", round(tuple_creation, 6), "seconds")


# 11. Compare indexing time

print("\nINDEXING TIME COMPARISON")

list_index_time = timeit.timeit(
    "values_list[500000]",
    globals=globals(),
    number=1000000
)

tuple_index_time = timeit.timeit(
    "values_tuple[500000]",
    globals=globals(),
    number=1000000
)

print("List indexing time:", round(list_index_time, 6), "seconds")
print("Tuple indexing time:", round(tuple_index_time, 6), "seconds")


print("\nQ2 PROGRAM COMPLETED SUCCESSFULLY")
