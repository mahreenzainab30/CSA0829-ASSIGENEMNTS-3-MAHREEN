
import random
import timeit
import sys


# -------------------------------------------------
# PART 1: BUILD TIMETABLE FOR FIVE TRAINS
# -------------------------------------------------

timetable = {
    "12601": {
        "name": "Chennai Express",
        "stops": [
            ("Chennai", "06:00", "06:15"),
            ("Katpadi", "08:00", "08:05"),
            ("Bengaluru", "11:00", "11:10")
        ],
        "days": {"Monday", "Wednesday", "Friday"}
    },

    "12602": {
        "name": "Coimbatore Express",
        "stops": [
            ("Chennai", "07:00", "07:15"),
            ("Salem", "10:00", "10:05"),
            ("Coimbatore", "12:30", "12:40")
        ],
        "days": {"Tuesday", "Thursday", "Saturday"}
    },

    "12603": {
        "name": "Mysuru Express",
        "stops": [
            ("Chennai", "08:00", "08:10"),
            ("Katpadi", "10:00", "10:05"),
            ("Bengaluru", "13:00", "13:10"),
            ("Mysuru", "15:00", "15:10")
        ],
        "days": {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}
    },

    "12604": {
        "name": "Madurai Express",
        "stops": [
            ("Chennai", "09:00", "09:15"),
            ("Villupuram", "11:00", "11:05"),
            ("Trichy", "14:00", "14:05"),
            ("Madurai", "16:00", "16:10")
        ],
        "days": {"Saturday", "Sunday"}
    },

    "12605": {
        "name": "Bengaluru Superfast",
        "stops": [
            ("Chennai", "05:30", "05:45"),
            ("Katpadi", "07:30", "07:35"),
            ("Bengaluru", "10:00", "10:10")
        ],
        "days": {"Monday", "Tuesday", "Thursday", "Saturday"}
    }
}


# -------------------------------------------------
# PART 2: PRINT TIMETABLE NEATLY
# -------------------------------------------------

def print_timetable(data):
    print("\nCOMPLETE RAILWAY TIMETABLE")

    for train_no, details in data.items():
        print("\nTrain Number:", train_no)
        print("Train Name:", details["name"])
        print("Running Days:", ", ".join(sorted(details["days"])))
        print("Route:")

        for station, arrival, departure in details["stops"]:
            print(f"  {station:15} Arrival: {arrival}  Departure: {departure}")


# -------------------------------------------------
# PART 3: SEARCH WITHOUT INDEX
# -------------------------------------------------

def search_without_index(data, station, day):
    results = []

    for train_no, details in data.items():

        if day in details["days"]:

            for stop in details["stops"]:
                stop_station, arrival, departure = stop

                if stop_station.lower() == station.lower():
                    results.append(
                        (train_no, details["name"], departure)
                    )
                    break

    return sorted(results, key=lambda item: item[2])


# -------------------------------------------------
# PART 4: CREATE STATION INDEX
# Station -> list of train numbers
# -------------------------------------------------

def build_station_index(data):
    index = {}

    for train_no, details in data.items():

        for station, arrival, departure in details["stops"]:
            index.setdefault(station.lower(), []).append(train_no)

    return index


# -------------------------------------------------
# PART 5: SEARCH USING INDEX
# -------------------------------------------------

def search_with_index(data, index, station, day):
    results = []

    train_numbers = index.get(station.lower(), [])

    for train_no in train_numbers:
        details = data[train_no]

        if day in details["days"]:

            for stop_station, arrival, departure in details["stops"]:

                if stop_station.lower() == station.lower():
                    results.append(
                        (train_no, details["name"], departure)
                    )
                    break

    return sorted(results, key=lambda item: item[2])


# -------------------------------------------------
# PART 6: DISPLAY SEARCH RESULTS
# -------------------------------------------------

print_timetable(timetable)

station = "Katpadi"
day = "Monday"

print("\nSEARCH WITHOUT INDEX:")
print(search_without_index(timetable, station, day))

station_index = build_station_index(timetable)

print("\nSTATION INDEX:")
print(station_index)

print("\nSEARCH WITH INDEX:")
print(search_with_index(timetable, station_index, station, day))


# -------------------------------------------------
# PART 7: ACCESS THIRD STATION DEPARTURE TIME
# -------------------------------------------------

print("\nTHIRD STATION DEPARTURE TIME:")

third_departure = timetable["12603"]["stops"][2][2]
print("Departure:", third_departure)


# -------------------------------------------------
# PART 8: EDGE CASE TESTS
# -------------------------------------------------

print("\nEDGE CASE TESTS:")

print("Unknown station:")
print(search_with_index(timetable, station_index, "Unknown Station", "Monday"))

print("\nTrain does not run on selected day:")
print(search_with_index(timetable, station_index, "Madurai", "Monday"))


# -------------------------------------------------
# PART 9: GENERATE LARGE TIMETABLES
# -------------------------------------------------

stations = [
    "Chennai", "Katpadi", "Salem", "Bengaluru",
    "Coimbatore", "Madurai", "Trichy", "Mysuru",
    "Villupuram", "Erode"
]

days_list = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]


def generate_timetable(number_of_trains):
    data = {}

    for i in range(number_of_trains):
        train_no = str(20000 + i)

        selected_stations = random.sample(stations, 5)

        stops = []

        for j, station_name in enumerate(selected_stations):
            hour = 5 + j * 2
            arrival = f"{hour:02d}:00"
            departure = f"{hour:02d}:10"

            stops.append((station_name, arrival, departure))

        running_days = set(random.sample(days_list, 5))

        data[train_no] = {
            "name": f"Express Train {i + 1}",
            "stops": stops,
            "days": running_days
        }

    return data


# -------------------------------------------------
# PART 10: PERFORMANCE AND MEMORY EXPERIMENT
# -------------------------------------------------

print("\nPERFORMANCE EXPERIMENT")

random.seed(42)

for size in [100, 1000, 10000]:

    large_timetable = generate_timetable(size)
    large_index = build_station_index(large_timetable)

    query_station = "Chennai"
    query_day = "Monday"

    no_index_time = timeit.timeit(
        lambda: search_without_index(
            large_timetable, query_station, query_day
        ),
        number=100
    )

    index_time = timeit.timeit(
        lambda: search_with_index(
            large_timetable, large_index, query_station, query_day
        ),
        number=100
    )

    # Estimate shallow memory occupied by the index dictionary
    index_memory = sys.getsizeof(large_index)

    for train_list in large_index.values():
        index_memory += sys.getsizeof(train_list)

    print(f"\nNumber of trains: {size}")
    print(f"Query time without index (100 queries): {no_index_time:.6f} seconds")
    print(f"Query time with index (100 queries): {index_time:.6f} seconds")
    print(f"Extra index memory: {index_memory} bytes")


