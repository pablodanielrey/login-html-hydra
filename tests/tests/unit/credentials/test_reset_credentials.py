

def test_get_reset_info(credentials_model_test):
    model = credentials_model_test
    model.generate_reset_info()

def test_reset_credentials(credentials_model_test):
    model = credentials_model_test
    model.reset_credentials()

def test_send_email_with_code(credentials_model):
    model = credentials_model