
import random
import time

print("Q4 - ELECTIVE REGISTRATION CLASH DETECTION")
print("=" * 55)

# 1. Create elective registration sets

ai_elective = {
    "192311001", "192311004", "192311007", "192311009"
}

iot_elective = {
    "192311002", "192311004", "192311009", "192311010"
}

all_students = {
    f"1923110{i:02d}" for i in range(1, 11)
}

# 2. Find students using set operators

both = ai_elective & iot_elective

exactly_one = ai_elective ^ iot_elective

neither = all_students - (ai_elective | iot_elective)

print("\nSET OPERATOR RESULTS")

print("AI students:", sorted(ai_elective))
print("IoT students:", sorted(iot_elective))

print("clash      :", sorted(both))
print("exactly one:", sorted(exactly_one))
print("neither    :", sorted(neither))

print("union      :", sorted(ai_elective | iot_elective))
print("AI only    :", sorted(ai_elective - iot_elective))


# 3. Repeat using set methods

both_method = ai_elective.intersection(iot_elective)

exactly_one_method = ai_elective.symmetric_difference(iot_elective)

neither_method = all_students.difference(
    ai_elective.union(iot_elective)
)

print("\nSET METHOD RESULTS")

print("Clash:", sorted(both_method))
print("Exactly one:", sorted(exactly_one_method))
print("Neither:", sorted(neither_method))

print(
    "Both approaches give same results:",
    both == both_method
    and exactly_one == exactly_one_method
    and neither == neither_method
)


# 4. Demonstrate duplicate removal

print("\nDUPLICATE REMOVAL")

registrations = [
    "192311001",
    "192311004",
    "192311001",
    "192311009",
    "192311004"
]

unique_registrations = set(registrations)

print("Original registrations:", registrations)
print("Unique registrations:", sorted(unique_registrations))


# 5. Verify the answer manually for the small example

print("\nMANUAL VERIFICATION")

print("Number in both:", len(both))
print("Number in exactly one:", len(exactly_one))
print("Number in neither:", len(neither))

print(
    "Total students accounted for:",
    len(both) + len(exactly_one) + len(neither)
)


# 6. Test empty and identical electives

print("\nEDGE CASE TESTING")

empty_elective = set()

print("Empty elective intersection:", ai_elective & empty_elective)
print("Empty elective union:", ai_elective | empty_elective)

same_elective = ai_elective.copy()

print("Identical elective intersection:",
      ai_elective & same_elective)

print("Identical elective symmetric difference:",
      ai_elective ^ same_elective)


# 7. Compare membership testing in lists and sets

print("\nMEMBERSHIP PERFORMANCE COMPARISON")

for size in [10000, 100000, 1000000]:

    student_list = list(range(size))
    student_set = set(student_list)

    search_value = size - 1

    start = time.perf_counter()

    for _ in range(1000):
        result = search_value in student_list

    list_time = time.perf_counter() - start

    start = time.perf_counter()

    for _ in range(1000):
        result = search_value in student_set

    set_time = time.perf_counter() - start

    print("\nNumber of students:", size)
    print("List membership time:", round(list_time, 6), "seconds")
    print("Set membership time:", round(set_time, 6), "seconds")


# 8. Compare nested loops with set intersection

print("\nCOMMON STUDENT SEARCH COMPARISON")

random.seed(42)

for size in [500, 1000, 2000]:

    list_a = random.sample(range(size * 2), size)
    list_b = random.sample(range(size * 2), size)

    # Nested loop method
    start = time.perf_counter()

    common_nested = []

    for student in list_a:
        for other in list_b:
            if student == other:
                common_nested.append(student)

    nested_time = time.perf_counter() - start

    # Set intersection method
    start = time.perf_counter()

    common_set = set(list_a) & set(list_b)

    set_time = time.perf_counter() - start

    print("\nDataset size:", size)
    print("Nested loop time:", round(nested_time, 6), "seconds")
    print("Set intersection time:", round(set_time, 6), "seconds")
    print("Both results match:",
          set(common_nested) == common_set)


print("\nQ4 PROGRAM COMPLETED SUCCESSFULLY")
