# Valid Digital ID examples used across all tests
# Update with new attributes as needed
new_person_dict = {
    "first_name": "John",
    "surname": "Smith", 
    "date_of_birth": "2000-01-01",
    "address": "123 This Street, London, M2 1AA",
    "national_insurance": "AB123456C"
}

from_csv_person_dict = {
    "id": 2,
    "status": "active",
    "first_name": "Alice",
    "surname": "Johnson",
    "date_of_birth": "1995-05-15",
    "address": "456 That Street, Manchester, M1 1AA",
    "national_insurance": "CD789012D"
}

justification_person_dict = new_person_dict.copy()
justification_person_dict["justification"] = "New registration"
