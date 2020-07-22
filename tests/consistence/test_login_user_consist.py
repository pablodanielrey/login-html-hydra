

def test_login_user_consistence(prepare_environment):
    """
        testea que todas las credenciales tengan usuario asociado
    """
    import sys
    sys.path.append('../src/')

    from users.model.entities.User import User, Mail, MailTypes, IdentityNumber, IdentityNumberTypes
    from login.model.entities.Login import UserCredentials
    from login_html_hydra.models.db import open_users_session, open_login_session

    with open_login_session() as lsession:
        with open_users_session() as usession:
            for uc in lsession.query(UserCredentials).all():
                uid = uc.user_id
                assert usession.query(User).filter(User.id == uid).count() == 1


def test_user_login_consistence(prepare_environment):
    """
        testea que todos los usuarios tengan al menos unas credenciales asociadas
    """
    import sys
    sys.path.append('../src/')

    from users.model.entities.User import User, Mail, MailTypes, IdentityNumber, IdentityNumberTypes
    from login.model.entities.Login import UserCredentials
    from login_html_hydra.models.db import open_users_session, open_login_session

    with open_users_session() as usession:
        with open_login_session() as lsession:
            for u in usession.query(User.id).all():
                uid = u.id
                assert lsession.query(UserCredentials).filter(UserCredentials.user_id == uid).count() > 0