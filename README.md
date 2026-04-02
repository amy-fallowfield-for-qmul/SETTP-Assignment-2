# SETTP Assignment 2

### Tests

To run tests, navigate to the SETTP-Assignment-2 directory and run:
    `python -m pytest Tests/ -v`

### Development

#### Adding new attributes:

1. In `attributeRepository.py`: Add a new AttributeMetadata object to _register_core_attributes()
2. In `digitalID.py`: Add to constructor + Add getter/setter
3. In `attributeValidator.py`: Add validation function to attributeValidator.py if attribute requires special validation rules
4. In `test_digitalID.py`: Add tests for getters and setters
5. In `test_attributeValidation.py`: Add tests for single attribute validation. Also add tests for any specifial validation function that has been added
