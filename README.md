# SETTP Assignment 2 — Digital ID System

**Repository:** https://github.com/amy-fallowfield-for-qmul/SETTP-Assignment-2

This program is a console-based Digital ID system allowing four organisation types (Central Authority, Bank, Employer, HMRC) to interact with a shared store of Digital IDs through organisation-specific operations. Every action is recorded in an audit log.

## Running the system

### Requirements
- Python 3.10 or later
- `pytest` (only needed to run the test suite)

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start the program
From the project root:
```bash
python src/main.py
```

Upon launch users are asked to select their organisation, and then an organisation-specific menu is displayed.
Existing Digital IDs and audit logs are loaded from `src/digital_ids.csv` and `src/logs.csv` on start-up and saved on exit.

### Run the tests
From the project root:
```bash
python -m pytest Tests/ -v
```

A GitHub Actions workflow (`.github/workflows/ci.yml`) runs the same command on every push and pull request.

## System structure and main components

The codebase uses the layered architecture and is stored under the `src/` directory:

```
src/
├── main.py
├── UI/
│   ├── requests.py
│   └── Controllers/
│       ├── mainABC.py
│       ├── centralAuthorityMain.py
│       ├── otherOrganisationsMain.py
│       ├── bank.py
│       ├── employer.py
│       └── hmrc.py
├── Logic/
│   ├── service.py
│   ├── verifier.py
│   ├── attributeValidator.py
│   ├── suspensionAnalyser.py
│   ├── period.py
│   ├── identityClaim.py
│   ├── organisation.py
│   ├── requestContext.py
│   └── exceptionLogger.py
├── Data/
│   ├── dataStorage.py
│   ├── repositoryABC.py
│   ├── DigitalID/
│   │   ├── digitalID.py
│   │   └── digitalIDRepository.py
│   ├── Attributes/
│   │   ├── address.py
│   │   ├── attributeMetadata.py
│   │   └── attributeRegistry.py
│   └── Logging/
│       ├── log.py
│       └── logRepository.py
├── Common/
│   └── singleton.py
└── Config/
    └── constants.py
```

### Key components

| Component | Responsibility |
|---|---|
| `main.py` | Entry point selects an organisation and calls the appropriate controller. |
| `mainABC.py` | Template-method base for all organisation controllers. Each subclass declares its menu, accessible attributes, verifiable attributes, and permitted operations. |
| `centralAuthorityMain.py` | Central Authority controller enabling full access to all implemented commands and all audit logs. |
| `otherOrganisationsMain.py` | Default base for non-Central-Authority controllers. |
| `bank.py` | Bank controller enabling identity verification and minimum-age verification. |
| `employer.py` | Employer controller enabling identity, minimum-age, and National Insurance verification. |
| `hmrc.py` | HMRC controller enabling National Insurance verification and suspension-period verification. |
| `requests.py` | Controls user input and the CLI elements of the program. |
| `service.py` | Coordinates Digital-ID operations with validation, permission checks, and audit logging. |
| `verifier.py` | Performs identity, minimum-age, attribute, and suspension verifications, and audit logging. |
| `requestContext.py` | Couples the organisation and justification for each request and handles permission checks. |
| `organisation.py` | Dictates what attributes and operations an organisation can read, verify, and perform. |
| `attributeValidator.py` | Handles attribute validation. |
| `period.py` | Couples start and end dates for suspension queries and encapsulates operations for periods. |
| `identityClaim.py` | Data clump bundling first name, surname, and date of birth for identity verification. |
| `suspensionAnalyser.py` | Uses logs to determine whether a Digital ID was suspended during a given period. |
| `exceptionLogger.py` | Context manager that records failed operations in the audit log. |
| `repositoryABC.py` | Generic singleton repository base used by both Digital IDs and audit logs. |
| `digitalID.py` | Digital ID entity with status, getters/setters and dictionary serialisation. |
| `digitalIDRepository.py` | Singleton repository containing all Digital IDs. |
| `log.py` | Audit log entity with an `Action` enum and per-action factory constructors. |
| `logRepository.py` | Singleton repository containing all audit logs. |
| `address.py` | Structured address object with separate address line, town/city and postcode components. |
| `attributeMetadata.py` | Describes each Digital ID attribute and its type for validation purposes. |
| `attributeRegistry.py` | Central registry of all known Digital ID attributes and their metadata. |
| `dataStorage.py` | CSV read/write helpers used by all repositories. |
| `singleton.py` | Metaclasses used to enforce single-instance classes. |
| `constants.py` | Stores constants used across the repository. |
| `digital_ids.csv` / `logs.csv` | Loads stored Digital IDs and audit logs on start-up and saves these on exit. |

### Design notes

- **Separation of concerns**
  - The UI layer only collects input and displays results. It never validates domain values or makes permission decisions.
  - The Logic layer owns all domain rules: `Validator` for input validation, `Verifier` for verification operations, `DigitalIDService` for CRUD, and value objects like `Period` and `IdentityClaim` for self-validating types.
  - The Data layer is responsible only for persistence and entity definitions; it has no knowledge of which organisation is acting.
  - Each layer can be tested independently

- **Individual Organisation Portals**
  - Each controller declares three classmethods:`accessible_attributes`, `verifiable_attributes`, and `permitted_operations`.These dictate all abilities of the organisation.
  - These collapse into an immutable `Organisation` dataclass in the Logic layer which is passed into a `RequestContext` object for every request.
  - Modifying what an organisation can do requires minor changes in its controller.

- **Auditability**
  - Every successful operation is added to the audit log through `Log.for_create / for_read / for_update / for_verify` factory constructors, keeping the structure consistent.
  - Every failed operation is added to to the audit log through the `record_failures` context manager which wraps service and verifier methods, writes a rejected log entry on exception, then re-raises the exception so the UI can handle the error.
  - Each log entry records timestamp, organisation, Digital ID number, action, justification, and (where applicable) the previous and new attribute values.

- **Persistence**
  - `dataStorage.py` provides CSV read/write helpers. Each repository extends `RepositoryABC`, which declares the CSV path, headers, and row-mapping methods.
  - On start-up, `Requests.start_program` calls `DigitalIDService.load_csv_data`, which populates both `digital_ids.csv` and `logs.csv` into their repositories. A missing CSV is treated as a clean first-run rather than an error.
  - On exit, `Requests.exit_program` saves both repositories back to their CSVs through the same path.
  - If saving fails, the user is asked whether to continue exiting anyway, so data isn't lost silently.
  - `KeyboardInterrupt` and `EOFError` are caught at the program boundary in `main.py` so the save step still runs even when the user terminates abruptly.

## Capabilities

### Central Authority
Readable attributes:
- `status`
- `first_name`
- `surname`
- `date_of_birth`
- `address`
- `national_insurance`

Operations:
- Create new Digital IDs
- Update existing Digital IDs (mutable attributes only)
- View Digital ID data
- View log data
- Verify a Digital ID's identity
- Verify a Digital ID meets a minimum age
- Verify any Digital ID attribute against a claimed value
- Verify suspension history for any period

### Bank
Readable attributes:
- `status`
- `address`

Operations:
- Verify a Digital ID's identity (Must supply ID number, first name, surname, and date of birth)
- Verify a Digital ID meets a minimum age (Must supply ID number and date of birth)

### Employer
Readable attributes:
- `status`
- `address`

Operations:
- Verify a Digital ID's identity (Must supply ID number, first name, surname, and date of birth)
- Verify a Digital ID meets a minimum age (Must supply ID number and date of birth)
- Verify a provided National Insurance number matches a Digital ID (Must supply ID number and national insurance number)

### HMRC
Readable attributes:
- `address`

Operations:
- Verify a provided National Insurance number matches a Digital ID (Must supply ID number and national insurance number)
- Verify suspension history for any period (Must supply ID number, start of period, and end of period)

## Development

### Adding new organisations:
1. Create a new file `[organisation_name].py` (e.g. hmrc.py for HMRC) + Create a class which inherits from `OtherOrganisationMain` + Define @classmethods `accessible_attributes`, `organisation_name`, and `permitted_operations`. If the organisation uses `verify_attribute`, also override `verifiable_attributes` (defaults to `[]` if not overridden). Override `menu_options` if the organisation needs operations beyond `Query Digital ID by ID` (the default inherited from `OtherOrganisationMain`).
2. In `main.py`: Add new class to `USER_OPTIONS` list
3. In `shared_test_data.py`: Add a matching `<NAME>_ORG = Organisation(...)` entry mirroring the new controller's capabilities, for tests that exercise the new organisation's permissions
4. Add new attribute(s) if required (See below)

#### Adding new attributes:

1. In `attributeRegistry.py`: Add a new AttributeMetadata object to the `CORE_ATTRIBUTE_OBJECTS` list
2. In `digitalID.py`: Add to constructor + Add getter/setter
3. If attribute cannot use an existing validation function:
    - In `attributeMetadata.py` add attribute type to `AttributeType` enum
    - In `attributeValidator.py`: Add validation function and add mapping to `_validate_by_type`
4. In `shared_test_data.py`: Add the new attribute to `new_person_dict` and `from_csv_person_dict` (mandatory if `is_required_for_creation=True`, otherwise existing creation tests will fail validation)
5. In `test_digitalID.py`: Add tests for getters and setters
6. In `test_attributeValidation.py`: Add tests for single attribute validation. Also add tests for any other functions that have been added
