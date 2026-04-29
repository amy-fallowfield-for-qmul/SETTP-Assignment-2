from .otherOrganisationsMain import OtherOrganisationMain

class Bank(OtherOrganisationMain):
    @property
    def allowed_attributes(self) -> list:
        return ["status", "first_name", "surname", "date_of_birth", "address"]

    @property
    def organisation_name(self) -> str:
        return "Bank"

if __name__ == "__main__":
    program = Bank()