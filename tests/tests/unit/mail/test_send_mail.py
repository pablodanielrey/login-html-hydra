

def test_send_code_mail(mails_model,generate_data):
    config = generate_data
    responses = mails_model.send_code(config['code'],config['user'],config['tos'])
    for r in responses:
        print(r)
    