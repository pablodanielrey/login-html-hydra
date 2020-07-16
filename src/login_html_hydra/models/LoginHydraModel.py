
from . import hydraModel, loginModel, usersModel, User, Mail, IdentityNumberTypes, MailTypes
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

    def login(self, username, password):
        with open_login_session() as lsession:
            uid, hash_ = loginModel.login(lsession, username, password, '', challenge)

        with open_users_session() as usession:
            usersModel.get_users(usession, [uid])