import os
import random
import string
import yaml

def create_index():
    try:
        # Generate a random index ID
        index_id = random.choice(string.ascii_uppercase) + ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
        # Update config.yml with the new index ID
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
            config['INDEX_NAME'] = index_id
        with open('config.yml', 'w') as file:
            yaml.dump(config, file)
        print("Index Updated Successfully")
    except Exception as e:
        error_msg = f"Failed to update index name: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

def clear_data(data_folder):
    if os.path.exists(data_folder):
        for filename in os.listdir(data_folder):
            file_path = os.path.join(data_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))