from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class Tokengenerator(PasswordResetTokenGenerator):
    def _Hash_value(self,new_user,timestap):

        return (
            six.text_type(new_user.pk)+six.text_type(timestap)+six.text_type(new_user.is_active)
        )
account_activation = Tokengenerator()