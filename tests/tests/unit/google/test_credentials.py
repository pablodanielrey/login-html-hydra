
import uuid
import logging

def test_change_credentials(google_sync_model):
    creds = str(uuid.uuid4()).replace('-','')
    model = google_sync_model
    r = model.sync_login('70000001',creds)
    print(creds)