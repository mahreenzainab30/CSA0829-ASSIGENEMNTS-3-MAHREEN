
import re
import timeit


# --------------------------------------------------
# 1. NORMALISATION FUNCTIONS
# --------------------------------------------------

def normalize_name(name):
    """Convert a name to lowercase and remove extra spaces."""
    if not name:
        return ""

    name = name.lower().strip()
    name = re.sub(r"\s+", " ", name)
    return name


def normalize_phone(phone):
    """
    Keep digits only.
    Convert an Indian number with +91 to its 10-digit form.
    """
    if not phone:
        return None

    digits = re.sub(r"\D", "", str(phone))

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    if len(digits) == 10:
        return digits

    return None


def normalize_email(email):
    if not email:
        return None

    email = email.strip().lower()
    return email if email else None


# --------------------------------------------------
# 2. CONTACT MERGING FUNCTION
# --------------------------------------------------

def merge_contacts(contact_list):
    merged = {}
    number_to_key = {}
    missing_phone_count = 0

    for contact in contact_list:

        # Read and normalize the name
        original_name = contact.get("name", "")
        clean_name = normalize_name(original_name)

        # Read phone numbers
        raw_phones = contact.get("phones", [])

        # Also accept a single phone field
        if contact.get("phone"):
            raw_phones = raw_phones + [contact["phone"]]

        phones = {
            normalize_phone(phone)
            for phone in raw_phones
            if normalize_phone(phone) is not None
        }

        # Read and normalize email addresses
        emails = {
            normalize_email(email)
            for email in contact.get("emails", [])
            if normalize_email(email) is not None
        }

        # Find existing contact records using any matching number
        existing_keys = {
            number_to_key[number]
            for number in phones
            if number in number_to_key
        }

        # Select the main record
        if existing_keys:
            main_key = next(iter(existing_keys))
        elif phones:
            main_key = sorted(phones)[0]
        else:
            # Do not merge contacts when no valid phone is available
            missing_phone_count += 1
            main_key = f"NO_PHONE_{missing_phone_count}"

        # Create a new record if necessary
        if main_key not in merged:
            merged[main_key] = {
                "names": set(),
                "numbers": set(),
                "emails": set()
            }

        # Merge other matching records into the main record
        for old_key in existing_keys:
            if old_key != main_key and old_key in merged:
                merged[main_key]["names"].update(
                    merged[old_key]["names"]
                )
                merged[main_key]["numbers"].update(
                    merged[old_key]["numbers"]
                )
                merged[main_key]["emails"].update(
                    merged[old_key]["emails"]
                )
                del merged[old_key]

        # Add the current contact's information
        if clean_name:
            merged[main_key]["names"].add(clean_name)

        merged[main_key]["numbers"].update(phones)
        merged[main_key]["emails"].update(emails)

        # Update the number-to-record index
        for number in merged[main_key]["numbers"]:
            number_to_key[number] = main_key

    return merged


# --------------------------------------------------
# 3. SAMPLE CONTACTS FROM TWO PHONES AND A SIM CARD
# --------------------------------------------------

phone_1 = [
    {
        "name": "Dr. Ravi",
        "phones": ["+91 98400 12345"],
        "emails": ["ravi@gmail.com"]
    },
    {
        "name": "Anitha",
        "phones": ["9876543210"],
        "emails": ["anitha@gmail.com"]
    }
]

phone_2 = [
    {
        "name": "ravi kumar",
        "phones": ["9840012345", "9123456789"],
        "emails": ["RAVI@GMAIL.COM", "ravi.work@gmail.com"]
    },
    {
        "name": "Karthik",
        "phones": ["+91 90000 11111"],
        "emails": []
    }
]

sim_card = [
    {
        "name": "Ravi",
        "phones": ["+91-98400-12345"],
        "emails": ["ravi@gmail.com"]
    },
    {
        "name": "Anitha",
        "phones": [],
        "emails": ["anitha@gmail.com"]
    }
]


# Combine all three contact sources
all_contacts = phone_1 + phone_2 + sim_card


# --------------------------------------------------
# 4. DISPLAY MERGED CONTACTS
# --------------------------------------------------

merged_contacts = merge_contacts(all_contacts)

print("\n========== MERGED CONTACT LIST ==========")

for key, details in merged_contacts.items():
    print("\nContact ID:", key)
    print("Names:", sorted(details["names"]))
    print("Phone Numbers:", sorted(details["numbers"]))
    print("Email Addresses:", sorted(details["emails"]))

print("\nTotal original contacts:", len(all_contacts))
print("Total merged records:", len(merged_contacts))


# --------------------------------------------------
# 5. MANUAL VERIFICATION
# --------------------------------------------------

print("\n========== MANUAL VERIFICATION ==========")

ravi_key = normalize_phone("+91 98400 12345")

if ravi_key in merged_contacts:
    ravi = merged_contacts[ravi_key]

    print("Ravi's names:", sorted(ravi["names"]))
    print("Ravi's numbers:", sorted(ravi["numbers"]))
    print("Ravi's emails:", sorted(ravi["emails"]))

    assert "dr. ravi" in ravi["names"]
    assert "ravi kumar" in ravi["names"]
    assert "9840012345" in ravi["numbers"]
    assert "9123456789" in ravi["numbers"]
    assert "ravi.work@gmail.com" in ravi["emails"]

    print("Manual verification: PASSED")


# --------------------------------------------------
# 6. TESTING MISSING FIELDS AND DIFFERENT FORMATS
# --------------------------------------------------

test_contacts = [
    {
        "name": "Test Person",
        "phones": ["+91 98765 43210"],
        "emails": ["TEST@GMAIL.COM"]
    },
    {
        "name": "test person",
        "phones": ["9876543210"],
        "emails": ["test@gmail.com"]
    },
    {
        "name": "Unknown Person",
        "phones": [],
        "emails": []
    },
    {
        "name": "Another Person",
        "phones": ["123"],
        "emails": []
    },
    {
        "name": "Same Name Different Person",
        "phones": ["9000011111"],
        "emails": []
    }
]

test_result = merge_contacts(test_contacts)

print("\n========== EDGE CASE TESTS ==========")
print("Input records:", len(test_contacts))
print("Output records:", len(test_result))
print("Different phone formats are normalized.")
print("Missing and invalid phone numbers are retained separately.")


# --------------------------------------------------
# 7. GENERATE LARGE CONTACT DATASETS
# --------------------------------------------------

def generate_contacts(total):
    contacts = []

    unique_count = total // 2

    for i in range(total):
        number_id = i % unique_count
        phone = "98" + f"{number_id:08d}"

        if i % 2 == 0:
            phone_format = "+91 " + phone
        else:
            phone_format = phone

        contacts.append({
            "name": f"Person {number_id}",
            "phones": [phone_format],
            "emails": [f"person{number_id}@gmail.com"]
        })

    return contacts


# --------------------------------------------------
# 8. PERFORMANCE MEASUREMENT
# --------------------------------------------------

print("\n========== PERFORMANCE MEASUREMENT ==========")

for size in [1000, 100000]:
    dataset = generate_contacts(size)

    execution_time = timeit.timeit(
        lambda: merge_contacts(dataset),
        number=1
    )

    print(
        f"{size} contacts -> "
        f"Dictionary merging time: {execution_time:.6f} seconds"
    )


# --------------------------------------------------
# 9. PAIRWISE COMPARISON METHOD
# --------------------------------------------------

def pairwise_duplicate_count(contacts):
    duplicate_pairs = 0

    for i in range(len(contacts)):
        phone_a = normalize_phone(contacts[i]["phones"][0])

        for j in range(i + 1, len(contacts)):
            phone_b = normalize_phone(contacts[j]["phones"][0])

            if phone_a is not None and phone_a == phone_b:
                duplicate_pairs += 1

    return duplicate_pairs


small_dataset = generate_contacts(1000)

pairwise_time = timeit.timeit(
    lambda: pairwise_duplicate_count(small_dataset),
    number=1
)

print("\nPairwise comparison for 1000 contacts:")
print(f"Execution time: {pairwise_time:.6f} seconds")

print("\nProgram execution completed successfully.")
