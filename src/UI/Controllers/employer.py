from .otherOrganisationsMain import OtherOrganisationMain

class Employer(OtherOrganisationMain):
    @property
    def allowed_attributes(self) -> list:
        return ["status", "first_name", "surname", "date_of_birth", "address", "national_insurance"]

    @property
    def organisation_name(self) -> str:
        return "Employer"

if __name__ == "__main__":
    program = Employer()