from .otherOrganisationsMain import OtherOrganisationMain

class Bank(OtherOrganisationMain):
    @classmethod
    def allowed_attributes(cls) -> list:
        return ["status", "first_name", "surname", "date_of_birth", "address"]

    @classmethod
    def organisation_name(cls) -> str:
        return "Bank"

if __name__ == "__main__":
    program = Bank()
