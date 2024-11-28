import pytest

"""
The input data must have the following format (JSON schema):
{
"id": "str", // Unique ID, should be included in the results
"numberOfChildren": "int",
"familyComposition": "str", // Choices are ["single", "couple"]
"familyUnitInPayForDecember": "bool" // Used for eligibility
determination
}
o The output data must have the following format (JSON schema):
{
"id": "str", // ID from input
"isEligible": "bool", // Eligibility, equal to
"familyUnitInPayForDecember"
"baseAmount": "float", // Base amount calculated from family
composition
"childrenAmount": "float", // Additional amount for children
"supplementAmount": "float" // Total amount
}

"""


# Test - Invalid
def test_eligibility_invalid():
    assert False 

# Test - Valid
def test_eligibility_valid():
    assert False

# Test - benefit ranges
def test_benefit():
    assert False