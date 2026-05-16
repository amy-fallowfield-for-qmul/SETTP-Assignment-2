# Valid Digital ID examples used across all tests
# Update with new attributes as needed
from Logic.organisation import Organisation

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

# Valid Organisation examples used across all tests
# Update with new attributes as needed
CENTRAL_AUTHORITY_ORG = Organisation(
    name="Central Authority",
    accessible_attributes=("status", "first_name", "surname", "date_of_birth", "address", "national_insurance"),
    verifiable_attributes=("status", "first_name", "surname", "date_of_birth", "address", "national_insurance"),
    permitted_operations=("create_id", "query_attribute", "update_id", "verify_identity", "verify_minimum_age", "verify_attribute", "verify_suspended_in_period"),
)

BANK_ORG = Organisation(
    name="Bank",
    accessible_attributes=("status", "address"),
    verifiable_attributes=(),
    permitted_operations=("query_attribute", "verify_identity", "verify_minimum_age"),
)

EMPLOYER_ORG = Organisation(
    name="Employer",
    accessible_attributes=("status", "address"),
    verifiable_attributes=("national_insurance",),
    permitted_operations=("verify_identity", "verify_minimum_age", "verify_attribute"),
)

HMRC_ORG = Organisation(
    name="HMRC",
    accessible_attributes=("address",),
    verifiable_attributes=("national_insurance",),
    permitted_operations=("query_attribute", "verify_attribute", "verify_suspended_in_period"),
)
