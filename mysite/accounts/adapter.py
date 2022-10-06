from allauth.account.adapter import DefaultAccountAdapter
import logging
logging.basicConfig(level=logging.INFO)


class MyAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
  
        from allauth.account.utils import user_email, user_field, user_username

        data = form.cleaned_data
        logging.info('*'*100)
        logging.info(data)
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("name")
        user.phone = data.get("phone")
        user.birth_date = data.get("birth_date")
        user.city = data.get("city")
        user.address = data.get("address")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user