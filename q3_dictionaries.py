
import re
import random
import time
from collections import Counter

print("Q3 - FARMER HELPLINE COMPLAINT ANALYSIS")
print("=" * 55)

# 1. Given complaint data from the assignment

calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received"
]

STOP = {"not", "high"}


# 2. Count word frequencies using dictionary and get()

def frequencies(texts, stop):
    counts = {}

    for text in texts:
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        for word in words:
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1

    return counts


# 3. Find top k frequent words

def top(counts, k):
    return sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )[:k]


# 4. Display word frequencies

word_counts = frequencies(calls, STOP)

print("\nWORD FREQUENCIES")
print(word_counts)

print("\nTOP 3 FREQUENT WORDS")
print(top(word_counts, 3))


# 5. Group complaints by district using setdefault()

district_complaints = [
    ("Chennai", "seeds not received"),
    ("Madurai", "fertiliser price high"),
    ("Chennai", "subsidy not received"),
    ("Salem", "seeds delayed"),
    ("Madurai", "poor crop production")
]

grouped = {}

for district, complaint in district_complaints:
    grouped.setdefault(district, []).append(complaint)

print("\nCOMPLAINTS GROUPED BY DISTRICT")

for district, complaints in grouped.items():
    print(district, ":", complaints)


# 6. Count complaints per district

print("\nNUMBER OF COMPLAINTS PER DISTRICT")

for district, complaints in grouped.items():
    print(district, ":", len(complaints))


# 7. Compare dictionary counting and Counter

print("\nCOUNTER COMPARISON")

counter_result = Counter()

for text in calls:
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    counter_result.update(
        word for word in words if word not in STOP
    )

print("Counter result:", counter_result)
print("Dictionary result:", word_counts)
print("Both methods match:", dict(counter_result) == word_counts)


# 8. Compare dictionary method with list.count()

print("\nPERFORMANCE INVESTIGATION")

vocabulary = [
    "seeds", "price", "fertiliser", "subsidy",
    "received", "delayed", "crop", "water"
]

for size in [1000, 10000, 100000]:

    # Generate synthetic complaints
    random.seed(42)

    data = [
        " ".join(random.choices(vocabulary, k=4))
        for _ in range(size)
    ]

    all_words = []

    for text in data:
        all_words.extend(text.split())

    # Dictionary method
    start = time.perf_counter()

    dict_counts = {}

    for word in all_words:
        dict_counts[word] = dict_counts.get(word, 0) + 1

    dict_time = time.perf_counter() - start

    # list.count() method
    start = time.perf_counter()

    distinct_words = set(all_words)

    list_counts = {
        word: all_words.count(word)
        for word in distinct_words
    }

    list_time = time.perf_counter() - start

    # Counter method
    start = time.perf_counter()

    counter_counts = Counter(all_words)

    counter_time = time.perf_counter() - start

    print("\nNumber of complaints:", size)
    print("Dictionary time:", round(dict_time, 6), "seconds")
    print("List.count() time:", round(list_time, 6), "seconds")
    print("Counter time:", round(counter_time, 6), "seconds")


# 9. Edge case testing

print("\nEDGE CASE TESTING")

print("Empty text:", frequencies([""], STOP))

print(
    "Uppercase and lowercase:",
    frequencies(["SEEDS seeds Seeds"], STOP)
)

print(
    "Punctuation:",
    frequencies(["Seeds! price, seeds."], STOP)
)


# 10. Test top k with ties

print("\nTOP WORD TEST")

sample = {
    "banana": 2,
    "apple": 2,
    "mango": 3
}

print("Top 2:", top(sample, 2))


print("\nQ3 PROGRAM COMPLETED SUCCESSFULLY")
