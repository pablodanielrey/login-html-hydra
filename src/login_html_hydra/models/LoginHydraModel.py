import logging
import inject

from login.model.LoginModel import LoginModel
from users.model.UsersModel import UsersModel

from .HydraApi import HydraApi
from . import User, Mail, IdentityNumberTypes, MailTypes
from .db import open_users_session, open_login_session

class LoginHydraModel():

    @inject.autoparams()
    def __init__(self, hydraApi: HydraApi, loginModel: LoginModel, usersModel: UsersModel):
        self.hydraApi = hydraApi
        self.loginModel = loginModel
        self.usersModel = usersModel

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

    def _generate_context(self, user:User):
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
        """
            acepta o deniega el challenge de hydra.
            solo retorna una exception cuando algo no funciona.
            en el caso de usuario inválido se retorna un 200 con un redirect a un error.
        """

        logging.debug(f'username: {username} - challenge: {challenge} inicio de logueo')
        data = self.get_login_challenge(challenge)
        assert data['skip'] is False

        with open_login_session() as lsession:
            login, hash_ = self.loginModel.login(lsession, username, password, '', challenge)
            if login:
                uid = login.user_id1
                with open_users_session() as usession:
                    users = self.usersModel.get_users(usession, [uid])
                    user = users[0]
                    context = self._generate_context(user)
                    data = self.hydraApi.accept_login_challenge(challenge=challenge, uid=uid, data=context, remember=False)
                    redirect = data['redirect_to']
                    return redirect
            else:
                data = self.hydraApi.deny_login_challenge(challenge=challenge, device_id=None, error='Credenciales incorrectas')
                redirect = data['redirect_to']
                return redirect


    def accept_login_challenge(self, challenge, uid):
        data = self.hydraApi.accept_login_challenge(challenge, uid)
        redirect = data['redirect_to']
        return redirect
    
    def get_login_challenge(self, challenge):
        data = self.hydraApi.get_login_challenge(challenge)
        return data

    def check_and_accept_consent_challenge(self, challenge):
        """
            https://www.ory.sh/hydra/docs/reference/api/#get-consent-request-information
        """
        data = self.hydraApi.get_consent_challenge(challenge)
        logging.debug(f'consent: {data}')
        scopes = data['requested_scope']
        context = data['context'] 
        redirect = self.hydraApi.accept_consent_challenge(challenge=challenge, scopes=scopes, context=context, remember=False)
        return redirect['redirect_to']
