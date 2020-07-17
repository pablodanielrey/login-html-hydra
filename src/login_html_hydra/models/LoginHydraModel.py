import logging

from .models import hydraApi, loginModel, usersModel
from . import User, Mail, IdentityNumberTypes, MailTypes
from .db import open_users_session, open_login_session

class LoginHydraModel():

    def __init__(self):
        pass

    def _get_user_dni(self, user:User):
        for i in user.identity_numbers:
            if i.type == IdentityNumberTypes.DNI:
                return i.number
        return ''

    def _get_user_student_number(self, user:User):
        for i in user.identity_numbers:
            if i.type == IdentityNumberTypes.STUDENT:
                return i.number
        return None    

    def _get_internal_mail(self, user:User):
        """
            Obtengo el primer correo institucional confirmado
            Si tiene mas de 1 correo es alfabéticamente ordenado
        """
        mails = [m.email for m in user.mails if m.deleted is None and m.confirmed and m.type == MailTypes.INSTITUTIONAL]
        mails.sort(reverse=False)
        if len(mails) > 0:
            return mails[0]
        return None

    def _get_external_mail(self, user:User):
        """
            Retorna el primer correo externo confirmado.
            Si tiene mas de 1 correco confirmado entonces es ordenado alfabéticamente.
        """
        mails = [m.email for m in user.mails if m.deleted is None and m.confirmed]
        mails.sort(reverse=False)
        if len(mails) > 0:
            return mails[0]

    def _generate_context(self, user):
        """
            Genera el contexto del token del usuario
        """
        context = {
            'sub':user.id,
            'given_name': user.firstname,
            'family_name': user.lastname,
            'preferred_username': self._get_user_dni(user)
        }
        student_number = self._get_user_student_number(user)
        if student_number:
            context['student_number'] = student_number

        mail = self._get_internal_mail(user)
        if not mail:
            mail = self._get_external_mail(user)
        
        if mail:
            context['email'] = mail
            context['email_verified'] = True
        return context

    def login(self, challenge, username, password):
        logging.debug(f'username: {username} - challenge: {challenge} inicio de logueo')
        valid, skip, redirect = self.check_login_challenge(challenge)

        if not valid:
            logging.error(f'username: {username} - challenge : {challenge} no válido')
            return False, None

        assert skip is False
        assert redirect is None

        with open_login_session() as lsession:
            uid, hash_ = loginModel.login(lsession, username, password, '', challenge)
            if not uid:
                with open_users_session() as usession:
                    users = usersModel.get_users(usession, [uid])
                    assert len(users) > 0
                    user = users[0]
                    context = self._generate_context(user)
                    status, data = hydraModel.accept_login_challenge(challenge=challenge, uid=uid, data=context, remember=False)
                    if status != 200:
                        return False, None
                    redirect = data['redirect_to']
                    return redirect
            else:
                status, data = hydraModel.deny_login_challenge(challenge, None, 'Credenciales incorrectas')
                if status != 200:
                    return False, None
                redirect = data['redirect_to']
                return redirect


    def accept_login_challenge(self, challenge):
        status, data = hydraApi.accept_login_challenge(challenge)
        redirect = data['redirect_url']
        return redirect
    

    def check_login_challenge(self, challenge):
        valid, skip = hydraApi.get_login_challenge(challenge)
        if valid:
            if skip:
                status, data = hydraApi.accept_login_challenge(challenge)
                redirect = data['redirect_url']
                return True, True, redirect
            else:
                return True, False, None
        else:
            return False, False, None

    def check_and_accept_consent_challenge(self, challenge):
        """
            https://www.ory.sh/hydra/docs/reference/api/#get-consent-request-information
        """
        status, data = hydraModel.get_consent_challenge(challenge)
        if status != 200:
            return False, None

        scopes = data['requested_scope']
        context = data['context'] 
        status, redirect = hydraModel.accept_consent_challenge(challenge=challenge, scopes=scopes, context=context, remember=False)
        if status != 200:
            return False, None

        return True, redirect

loginHydraModel = LoginHydraModel()