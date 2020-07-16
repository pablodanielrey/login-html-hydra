
from . import hydraModel, loginModel, usersModel
from .db import open_users_session, open_login_session

class LoginHydraModel():

    INTERNAL_DOMAINS = os.environ['INTERNAL_DOMAINS'].split(',')

    def __init__(self):
        pass

    """ TODO: modificar esto ya que ahroa si tenemos concepto de cuenta interna o externa en la entidad de los mails """
    def _is_internal_mail(mail):
        return mail.split('@')[1] in INTERNAL_DOMAINS

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

    def _generate_context(self, user):
        """
            Genera el contexto del token del usuario
        """
        context = {
            'sub':user.id,
            'given_name': user.firstname,
            'family_name': user.lastname,
            'preferred_username': _get_user_dni(user)
        }
        student_number = _get_user_student_number(user)
        if student_number:
            context['student_number'] = student_number

        mail_context = None
        mails = [m.email for m in user.mails if m.deleted is None and m.confirmed]
        internals_mail = [m for m in mails if _is_internal_mail(m)]
        """ esta lista debe ser determinista!!! asi que la ordeno por longitud por ejemplo para que sea determinista y después por el orden normal (para el caso de 2 mails de mismo largo) """
        internals_mail.sort(revese=False, key=len)
        internals_mails.sort(reverse=False)

        if len(internals_mail) > 0:
            mail_context = internals_mail[0]
        
        if not mail_context:
            externals_mails = [m for m in mails if not _is_internal_mail(m)]
            if len(externals_mails) > 0:
                mail_context = externals_mails[0]
    
        if mail_context:
            context['email'] = mail_context
            context['email_verified'] = True
        return context

    def login(self, username, password):
        with open_login_session() as lsession:
            uid, hash_ = loginModel.login(lsession, username, password, '', challenge)

        with open_users_session() as usession:
            usersModel.get_users(usession, [uid])