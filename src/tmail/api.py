import requests

MAIL_ENDPOINT = "https://api.internal.temp-mail.io/api/v3/email/new"
INBOX_ENDPOINT = "https://api.internal.temp-mail.io/api/v3/email/{email}/messages"
ATTACHMENT_ENDPOINT = "https://api.internal.temp-mail.io/api/v3/attachment/{id}?download=1"


def get_random_email():
    """Generates a new random email address."""
    json_data = {"min_name_length": 10, "max_name_length": 10}
    response = requests.post(MAIL_ENDPOINT, json=json_data)
    response.raise_for_status()
    return response.json()["email"]


def fetch_messages(email):
    """Fetches messages for a given email address."""
    url = INBOX_ENDPOINT.format(email=email)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_attachment_url(att_id):
    """Returns the download URL for an attachment."""
    return ATTACHMENT_ENDPOINT.format(id=att_id)


def download_attachment(att_id, save_path):
    """Downloads an attachment to the given file path."""
    url = ATTACHMENT_ENDPOINT.format(id=att_id)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
