import pytest
from django.contrib.auth import get_user_model


User = get_user_model()


class Test00UserRegistration:
    url_signup = '/api/users/'
    url_token = '/api/auth/token/login/'
    url_admin_create_user = '/api/v1/users/'

    @pytest.mark.django_db(transaction=True)
    def test_00_nodata_signup(self, client):
        request_type = 'POST'
        response = client.post(self.url_signup)

        assert response.status_code != 404, (
            f'Page `{self.url_signup}` not found.'
        )
        code = 400
        assert response.status_code == code, (
            f'Check, that in {request_type} request `{self.url_signup}`'
            f'without parameters user did not created and was retured code {code}'
        )
        response_json = response.json()
        empty_fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        ]
        for field in empty_fields:
            assert (field in response_json.keys()
                    and isinstance(response_json[field], list)), (
                f'Check, that in {request_type} request `{self.url_signup}`'
                f'without parameters response have a description, which fields'
                f'filled worng'
            )
    
    @pytest.mark.django_db(transaction=True)
    def test_00_invalid_data_signup(self, client):
        invalid_email = 'invalid_email'
        invalid_username = 'invalid_username@yamdb.fake'

        invalid_data = {
            'email': invalid_email,
            'username': invalid_username
        }
        request_type = 'POST'
        response = client.post(self.url_signup, data=invalid_data)

        assert response.status_code != 404, (
            f'Page `{self.url_signup}` not found.'
        )
        code = 400
        assert response.status_code == code, (
            f'Check that in {request_type} request `{self.url_signup}` '
            f'with wrond data user is not created and returned code {code}'
        )

        response_json = response.json()
        invalid_fields = ['email']
        for field in invalid_fields:
            assert (field in response_json.keys()
                    and isinstance(response_json[field], list)), (
                f'Check that in {request_type} request `{self.url_signup}`'
                f' with invadid data response have a description which fields '
                f'filled wrong'
            )

        valid_email = 'validemail@yamdb.fake'
        invalid_data = {
            'email': valid_email,
        }
        response = client.post(self.url_signup, data=invalid_data)
        assert response.status_code == code, (
            f'Check that in {request_type} request `{self.url_signup}` '
            f'without username it is impossible to create a user '
            f'and returned code {code}'
        )

    @pytest.mark.django_db(transaction=True)
    def test_00_valid_data_user_signup(self, client):

        valid_email = 'valid@yamdb.fake'
        valid_username = 'valid_username'
        valid_first_name = 'Validfirstname'
        valid_last_name = 'Validlastname'
        valid_password = 'Validpass1'

        valid_data = {
            'email': valid_email,
            'username': valid_username,
            'first_name': valid_first_name,
            'last_name': valid_last_name,
            'password': valid_password
        }
        request_type = 'POST'
        response = client.post(self.url_signup, data=valid_data)

        assert response.status_code != 404, (
            f'Page `{self.url_signup}` not found'
        )

        code = 200
        assert response.status_code == code, (
            f'Check that in {request_type} request `{self.url_signup}` '
            f'with valid data user is created and returned code {code}'
        )
       
        for key in ('email', 'username', 'first_name', 'last_name'):
            assert response.json()[key] == valid_data[key], (
                f'Check that in {request_type} request `{self.url_signup}` '
                f'with valid data user is created and returned valid data {code}'
            )

        new_user = User.objects.filter(email=valid_email)
        assert new_user.exists(), (
            f'Check that in {request_type} request `{self.url_signup}` '
            f'with valid data user is created and returned code {code}'
        )

        new_user.delete()


    @pytest.mark.django_db(transaction=True)
    def test_00_obtain_jwt_token_invalid_data(self, client):

        request_type = 'POST'
        response = client.post(self.url_token)
        assert response.status_code != 404, (
            f'Page `{self.url_token}` not found, check url in *urls.py*'
        )

        code = 400
        assert response.status_code == code, (
            f'Chech, that in POST request `{self.url_token}` '
            f'without parametrs куегкты {code}'
        )

        invalid_data = {
            'password': 12345
        }
        response = client.post(self.url_token, data=invalid_data)
        assert response.status_code == code, (
            f'Check, that in POST request `{self.url_token}` without email, '
            f'returned code {code}'
        )

        invalid_data = {
            'email': 'unexisting@email.mail',
            'password': 12345
        }
        response = client.post(self.url_token, data=invalid_data)
        code = 400
        assert response.status_code == code, (
            f'Check, that in POST request `{self.url_token}` with, '
            f'unexisting email returned {code}'
        )

        valid_email = 'valid@yamdb.fake'
        valid_username = 'valid_username'

        valid_data = {
            'email': valid_email,
            'username': valid_username
        }
        response = client.post(self.url_signup, data=valid_data)
        code = 200
        assert response.status_code == code, (
            f'Chech, that with {request_type} request `{self.url_signup}` '
            f' with valid data user is created and returned code {code}'
        )

        invalid_data = {
            'email': valid_username,
            'password': 12345
        }
        response = client.post(self.url_token, data=invalid_data)
        code = 400
        assert response.status_code == code, (
            f'Check, that witn POST request `{self.url_token}` with valid email , '
            f'but with invalid password returned code {code}'
        )

# TODO
    @pytest.mark.skip(reason='Not ready')
    @pytest.mark.django_db(transaction=True)
    def test_00_registration_me_username_restricted(self, client):
        valid_email = 'valid@yamdb.fake'
        invalid_username = 'me'
        request_type = 'POST'

        valid_data = {
            'email': valid_email,
            'username': invalid_username
        }
        response = client.post(self.url_signup, data=valid_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` '
            f'нельзя создать пользователя с username = "me" и возвращается статус {code}'
        )
    
    @pytest.mark.skip(reason='Not ready')
    @pytest.mark.django_db(transaction=True)
    def test_00_registration_same_email_restricted(self, client):
        valid_email_1 = 'test_duplicate_1@yamdb.fake'
        valid_email_2 = 'test_duplicate_2@yamdb.fake'
        valid_username_1 = 'valid_username_1'
        valid_username_2 = 'valid_username_2'
        request_type = 'POST'

        valid_data = {
            'email': valid_email_1,
            'username': valid_username_1
        }
        response = client.post(self.url_signup, data=valid_data)
        code = 200
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` '
            f'можно создать пользователя с валидными данными и возвращается статус {code}'
        )

        duplicate_email_data = {
            'email': valid_email_1,
            'username': valid_username_2
        }
        response = client.post(self.url_signup, data=duplicate_email_data)
        code = 400
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` нельзя создать '
            f'пользователя, email которого уже зарегистрирован и возвращается статус {code}'
        )
        duplicate_username_data = {
            'email': valid_email_2,
            'username': valid_username_1
        }
        response = client.post(self.url_signup, data=duplicate_username_data)
        assert response.status_code == code, (
            f'Проверьте, что при {request_type} запросе `{self.url_signup}` нельзя создать '
            f'пользователя, username которого уже зарегистрирован и возвращается статус {code}'
        )
