import pytest
import sys
sys.path.append(".")
from src.rule_engine import rule_engine
import json
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
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 0,
        "familyComposition": "single",
        "familyUnitInPayForDecember": False
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == False
    assert result["baseAmount"] == 0.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 0.0

# Test - Valid
def test_eligibility_valid():
    assert False

# Test - benefit ranges
def test_benefit():
    assert False