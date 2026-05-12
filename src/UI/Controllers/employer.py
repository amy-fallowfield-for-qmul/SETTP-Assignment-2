from .otherOrganisationsMain import OtherOrganisationMain

class Employer(OtherOrganisationMain):
    @classmethod
    def accessible_attributes(cls) -> list:
        return ["status", "first_name", "surname", "date_of_birth", "address", "national_insurance"]

    @classmethod
    def organisation_name(cls) -> str:
        return "Employer"

if __name__ == "__main__":
    program = Employer()
