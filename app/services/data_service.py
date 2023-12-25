from app.exceptions.custom_exceptions import CustomException

# In-memory data store (replace this with a database in a real-world scenario)
data_store = {"example_key": "example_value"}
data_store_new = {"example_ttt": "example_zzz"}

def get_data():
    return data_store

def get_data_new():
    return data_store

def update_data(update_value):
    try:
        if "example_key" not in data_store:
            raise CustomException("Key not found in data store", status_code=404)

        # Update the data
        data_store["example_key"] = update_value
        return data_store
    except Exception as e:
        raise CustomException(str(e))