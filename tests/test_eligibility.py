import pytest
import sys
sys.path.append(".")
from src.rule_engine import rule_engine
import json

# Test - Invalid inputs
def test_invalid_input_null_id():
    test_message = {
        "id": None,
        "numberOfChildren": 0,
        "familyComposition": "single",
        "familyUnitInPayForDecember": False
        }
    result = rule_engine(json.dumps(test_message))
    assert result is None

def test_invalid_input_empty_id():
    test_message = {
        "id": "",
        "numberOfChildren": 0,
        "familyComposition": "single",
        "familyUnitInPayForDecember": False
        }
    result = rule_engine(json.dumps(test_message))
    assert result is None

def test_missing_input_id():
    test_message = {
        "numberOfChildren": 0,
        "familyComposition": "single",
        "familyUnitInPayForDecember": False
        }
    result = rule_engine(json.dumps(test_message))
    assert result is None

def test_invalid_input_neg_children():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": -1,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == False
    assert result["baseAmount"] == 0.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 0.0

def test_invalid_input_float_child_0():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 0.0,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == True
    assert result["baseAmount"] == 60.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 60.0

# Assumption: Type enforcement on integer handled by input processors
def test_invalid_input_float_child_1():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 1.5,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == True
    assert result["baseAmount"] == 120.0
    assert result["childrenAmount"] == 20.0
    assert result["supplementAmount"] == 140.0

def test_invalid_input_family_type():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 1,
        "familyComposition": "married",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == False
    assert result["baseAmount"] == 0.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 0.0

def test_invalid_input_empty_family_type():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 1,
        "familyComposition": None,
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == False
    assert result["baseAmount"] == 0.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 0.0

# Test - Invalid states
def test_eligibility_invalid_single_no_child():
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

def test_eligibility_invalid_single_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 1,
        "familyComposition": "single",
        "familyUnitInPayForDecember": False
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == False
    assert result["baseAmount"] == 0.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 0.0

def test_eligibility_invalid_couple_1_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 1,
        "familyComposition": "couple,",
        "familyUnitInPayForDecember": False
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == False
    assert result["baseAmount"] == 0.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 0.0

def test_eligibility_invalid_couple_no_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 0,
        "familyComposition": "couple",
        "familyUnitInPayForDecember": False
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == False
    assert result["baseAmount"] == 0.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 0.0

# Test - Valid States
def test_eligibility_valid_single_no_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 0,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == True
    assert result["baseAmount"] == 60.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 60.0

def test_eligibility_valid_single_1_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 1,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == True
    assert result["baseAmount"] == 120.0
    assert result["childrenAmount"] == 20.0
    assert result["supplementAmount"] == 140.0

def test_eligibility_valid_single_2_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 2,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == True
    assert result["baseAmount"] == 120.0
    assert result["childrenAmount"] == 40.0
    assert result["supplementAmount"] == 160.0

def test_eligibility_valid_single_3_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 3,
        "familyComposition": "single",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == True
    assert result["baseAmount"] == 120.0
    assert result["childrenAmount"] == 60.0
    assert result["supplementAmount"] == 180.0


def test_eligibility_valid_couple_no_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 0,
        "familyComposition": "couple",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == True
    assert result["baseAmount"] == 120.0
    assert result["childrenAmount"] == 0.0
    assert result["supplementAmount"] == 120.0

def test_eligibility_valid_couple_1_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 1,
        "familyComposition": "couple",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == True
    assert result["baseAmount"] == 120.0
    assert result["childrenAmount"] == 20.0
    assert result["supplementAmount"] == 140.0

def test_eligibility_valid_couple_2_child():
    test_message = {
        "id": "test-1234",
        "numberOfChildren": 2,
        "familyComposition": "couple",
        "familyUnitInPayForDecember": True
        }
    result = rule_engine(json.dumps(test_message))
    assert result["isEligible"] == True
    assert result["baseAmount"] == 120.0
    assert result["childrenAmount"] == 40.0
    assert result["supplementAmount"] == 160.0