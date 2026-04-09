from otherOrganisationsMain import OtherOrganisationMain

class HMRC(OtherOrganisationMain):
    @property
    def allowed_attributes(self) -> list:
        return ["status", "address", "national_insurance"]

    @property
    def organisation_name(self) -> str:
        return "HMRC"

if __name__ == "__main__":
    program = HMRC()
