import pytest
#from pytest_xprocess import getrootdir

def validate_json_data(data):
    assert "id" in data, "missing 'id' key"
    assert "name" in data, "missing 'name' key"
    assert "email" in data, "missing 'email' key"
    assert isinstance(data["id"], int), "'id' should be an integer"
    # A built-in function that checks if an object (data["id"]) is of a specific type (int)
    assert isinstance(data["name"], str), "'name' should be a string"
    assert isinstance(data["email"], str), "'email' should be a string"

def test_validate_json_data():
    #test valid data
    valid_data = {
        "id": 1,
        "name": "john Doe",
        "email": "john.do@example.com"
    }

    validate_json_data(valid_data)

    #test missing 'id' key
    missing_id_data = {
        "name": "john Doe",
        "email": "john.do@example.com"
    }

    with pytest.raises(AssertionError, match="missing 'id' key"):
        validate_json_data(missing_id_data)


    # test missing 'name' key
    missing_name_data = {
        "id" : 1,
        "email" : "john.doe@example.com"
    }
    with pytest.raises(AssertionError, match="missing 'name' key"):
        validate_json_data(missing_name_data)

    # Test missing 'email' key
    missing_email_data = {
        "id": 1,
        "name": "John Doe"
    }
    with pytest.raises(AssertionError, match="Missing 'email' key"):
        validate_json_data(missing_email_data)

    #Test 'id' is not an integer
    invalid_id_data = {
        "id": "1",
        "name": "John Doe",
        "email": "john.doe@example.com"
    }
    with pytest.raises(AssertionError, match="'id' should be an integer"):
        validate_json_data(invalid_id_data)

    # Test 'name' is not a string
    invalid_name_data = {
        "id": 1,
        "name": 123,
        "email": "john.doe@example.com"
    }
    with pytest.raises(AssertionError, match="'name' should be a string"):
        validate_json_data(invalid_name_data)

    # Test 'email' is not a string
    invalid_email_data = {
        "id": 1,
        "name": "John Doe",
        "email": 123
    }
    with pytest.raises(AssertionError, match="'email' should be a string"):
        validate_json_data(invalid_email_data)

if __name__ == '__main__':
    pytest.main()





    
    