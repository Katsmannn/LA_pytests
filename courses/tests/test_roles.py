import pytest
from http import HTTPStatus

from api.models import UserRole, User


class TestRoleAPI:
    '''
    Тестирование эндпоинта присвоения ролей пользователю
    /users/{user.id}/role/.

    Поддерживаемые методы: GET, POST, DELETE.
    При присвоении пользователю роли main user, пользователю должны назначаться
    адимистративные права в Django для работы в админке.
    '''

    @pytest.mark.django_db(transaction=True)
    def test_user_roles_url(self, client, user):
        '''
        Тестирование доступности эндпоинта /users/{user.id}/role/.
        '''
        response = client.get(f'/users/{user.id}/role/')

        assert response.status_code == HTTPStatus.OK, (
            'Эндпоинт /users/{user.id}/role/ недоступен.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_get_user_roles(self, client, user, user_admin_teacher_role):
        '''
        Тестирование метода GET. Получение ролей пользователя.
        '''
        response = client.get(f'/users/{user.id}/role/')

        test_data = response.json()
        assert type(test_data) == list, (
            'Ответ должен содержать список ролей (list).'
        )

        assert len(test_data) == UserRole.objects.filter(user=user.id).count()

        assert 'id' in test_data[0], (
            'В ответе отсутствует поле id.'
        )

        assert 'role' in test_data[0], (
            'В ответе отсутствует поле role.'
        )

        assert 'user' in test_data[0], (
            'В ответе отсутствует поле user.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_create_user_roles(self, client, user,
                               role_main_admin, role_teacher):
        '''
        Тестирование метода POST. Создание ролей пользователя.
        '''
        user_role_data_1 = {'role': role_teacher}
        user_role_admin_data = {'role': role_main_admin}
        user_role_incorrect_data = {'role', 'incorrect role'}

        client.post(f'/users/{user.id}/role/', data=user_role_data_1)
        user_roles = UserRole.objects.filter(user=user)
        assert user_roles.count() == 1, (
            'Проверьте, что метод POST добавляет запись в базу.'
        )

        assert user_roles[0].role == user_role_data_1['role'], (
            'Проверьте, что метод POST добавляет в базу запись с'
            + 'верными аттрибутами.'
        )

        try:
            client.post(f'/users/{user.id}/role/', data=user_role_data_1)
        except Exception:
            pass
        assert UserRole.objects.filter(user=user).count() == 1, (
            'Роли пользователя не могут дублироваться.'
        )

        client.post(f'/users/{user.id}/role/', data=user_role_admin_data)
        assert user_roles.count() == 2, (
            'У пользователя может быть несколько ролей.'
        )

        try:
            client.post(
                f'/users/{user.id}/role/', data=user_role_incorrect_data
            )
        except Exception:
            pass
        assert UserRole.objects.filter(user=user).count() == 2, (
            'Пользователю может быть присвоена роль только из списка ролей.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_delete_user_roles(self, client, user, user_admin_teacher_role):
        '''
        Тестирование метода DELETE. Удаление ролей пользователя.
        '''
        response = client.get(f'/users/{user.id}/role/')
        role_id = response.json()[0]['id']
        client.delete(f'/users/{user.id}/role/{role_id}/')

        assert UserRole.objects.count() == 1, (
            'Проверьте, что метод DELETE удаляет роль из таблицы UserRole.'
        )

        assert not UserRole.objects.filter(user=user, id=role_id).exists(), (
            'Проверьте, что метод DELETE удаляет из таблицы UserRole.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_admin_user_roles(self, client, user,
                              role_main_admin,
                              role_teacher):
        '''
        Тестирование предоставления прав superuser пользователю
        с ролью main admin.
        '''
        user_role_data_1 = {'role': role_teacher}
        user_role_admin_data = {'role': role_main_admin}

        client.post(f'/users/{user.id}/role/', data=user_role_data_1)
        assert not User.objects.get(id=user.id).is_superuser, (
            'Пользователь без роли main admin, не должен быть superuser.'
        )

        client.post(f'/users/{user.id}/role/', data=user_role_admin_data)
        assert User.objects.get(id=user.id).is_superuser, (
            'При добалении пользователю роли main admin,'
            + 'is_superuser долже устанавливаться в True.'
        )

        response = client.get(f'/users/{user.id}/role/')
        role_id = [
            role['id'] for role in response.json() if role[
                'role'
            ] == role_main_admin
        ][0]
        client.delete(f'/users/{user.id}/role/{role_id}/')
        assert not User.objects.get(id=user.id).is_superuser, (
            'При удалении у пользователя роли main admin,'
            + 'is_superuser должен устанавливаться в False.'
        )
