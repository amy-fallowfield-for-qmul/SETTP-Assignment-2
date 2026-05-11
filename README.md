# SETTP Assignment 2

### Capabilities

#### Central Authority
Central Authority has full access and can individually query the following attributes:
- status
- first_name
- surname
- date_of_birth
- address
- national_insurance

Central Authority can also:
- Create new Digital IDs
- Update existing Digital IDs (mutable attributes only)
- View all Digital ID data
- View all log data
- Query suspension history for any period

#### Bank
Bank can individually query the following attributes:
- status
- first_name
- surname
- date_of_birth
- address

#### Employer
Employer can individually query the following attributes:
- status
- first_name
- surname
- date_of_birth
- address
- national_insurance

#### HMRC
HMRC can individually query the following attributes:
- status
- address
- national_insurance

HMRC also has additional capability to:
- Query suspension history for any period

### Development

### Adding new organisations:
1. Create a new file `[organisation_name].py` (e.g. hmrc.py for HMRC) + Create a class which inherits from `OtherOrganisationMain` + Define @classmethods `allowed_attributes` and `organisation_name`
2. In `main.py`: Add new class to `USER_OPTIONS` list
3. Add new attribute(s) if required (See below)

#### Adding new attributes:

1. In `attributeRepository.py`: Add a new AttributeMetadata object to _register_core_attributes()
2. In `digitalID.py`: Add to constructor + Add getter/setter
3. If attribute cannot use an existing validation function:
    - In `attributeMetadata.py` add attribute type to `AttributeType` enum
    - In `attributeValidator.py`: Add validation function and add mapping to `_validate_by_type`
4. In `test_digitalID.py`: Add tests for getters and setters
5. In `test_attributeValidation.py`: Add tests for single attribute validation. Also add tests for any other functions that have been added

### Tests

To run tests, navigate to the SETTP-Assignment-2 directory and run:
    `python -m pytest Tests/ -v`
