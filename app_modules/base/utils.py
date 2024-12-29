import os
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def get_encoded_id(id):
    return urlsafe_base64_encode(force_bytes(id))

def get_actions_buttons(update_url,delete_url,title,encoded_id):
    return f"""
        <a href='{update_url}' title='Edit' style='color:var(--primary-bg-color); cursor: pointer;'>
            <i class='fa fa-edit'></i>
        </a> 
        <label data-title='{title}' data-id='{encoded_id}' 
                style='color:var(--primary-bg-color); cursor: pointer;' title='Delete' 
                data-url='{delete_url}' class='text-danger delete-btn text-center'>
            <i class='fa fa-trash'></i>
        </label>
    """

def delete_image(image_path):
    """
    Deletes an image file from the filesystem.
    """
    try:
        if os.path.isfile(image_path):
            os.remove(image_path)
            print(f"Image at {image_path} deleted.")
        else:
            print(f"Image at {image_path} not found.")
    except Exception as e:
        print(f"An error occurred while deleting the image: {e}")

def normalize_email(email):
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        print('\033[91m'+'email: ' + '\033[92m', email)
        return email