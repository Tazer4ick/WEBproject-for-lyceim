from helpers.CONSTS import BASE_API_URL

from requests import get, post, delete, put


class CustomUser:
    pass


CREATED_USER = None
test_user = CustomUser()
test_user.name = "test_user_name"
test_user.email = "test@test.test"
test_user.about = "little about story"

test_user2 = CustomUser()
test_user2.name = "test_user_name1"
test_user2.email = "test1@test.test"
test_user2.about = "little about story1"


class TestUsers:
    def test_get_all_users(self):
        all_users_json = get(f"{BASE_API_URL}/users").json()
        all_users = all_users_json["users"]
        assert isinstance(all_users, list)
        # self.assertIsInstance(all_users, list)

    def test_create_user_right(self):
        global CREATED_USER
        created_user_json = post(f"{BASE_API_URL}/users",
                                 json={
                                     "name": test_user.name,
                                     "about": test_user.about,
                                     "email": test_user.email,
                                     "hashed_password": "123456",
                                     "password_again": "123456"
                                 }).json()
        created_user = CustomUser()
        created_user.id = created_user_json["user"]["id"]
        created_user.name = created_user_json["user"]["name"]
        created_user.about = created_user_json["user"]["about"]
        created_user.email = created_user_json["user"]["email"]
        assert created_user.name == test_user.name
        assert created_user.about == test_user.about
        assert created_user.email == test_user.email
        # self.assertEqual(created_user.name, test_user.name)
        # self.assertEqual(created_user.about, test_user.about)
        # self.assertEqual(created_user.email, test_user.email)
        CREATED_USER = created_user

    def test_create_user_bad_same_email(self):
        request = post(f"{BASE_API_URL}/users",
                       json={
                           "name": test_user.name,
                           "about": test_user.about,
                           "email": test_user.email,
                           "hashed_password": "123456",
                           "password_again": "123456"
                       })
        assert request.status_code == 400
        # self.assertEqual(request.status_code, 400)

    def test_create_user_bad_different_passwords(self):
        request = post(f"{BASE_API_URL}/users",
                       json={
                           "name": test_user.name,
                           "about": test_user.about,
                           "email": "test" + test_user.email,
                           "hashed_password": "123456",
                           "password_again": "123"
                       })
        assert request.status_code == 409
        # self.assertEqual(request.status_code, 409)

    def test_get_one_user_right(self):
        user_json = get(f"{BASE_API_URL}/users/{CREATED_USER.id}").json()
        user = CustomUser()
        user.id = user_json["user"]["id"]
        user.name = user_json["user"]["name"]
        user.about = user_json["user"]["about"]
        user.email = user_json["user"]["email"]
        assert user.id == CREATED_USER.id
        assert user.name == CREATED_USER.name
        assert user.about == CREATED_USER.about
        assert user.email == CREATED_USER.email
        # self.assertEqual(user.id, CREATED_USER.id)
        # self.assertEqual(user.name, CREATED_USER.name)
        # self.assertEqual(user.about, CREATED_USER.about)
        # self.assertEqual(user.email, CREATED_USER.email)

    def test_get_one_user_bad_wrong_user_id(self):
        response = get(f"{BASE_API_URL}/users/-1")
        assert response.status_code == 404
        # self.assertEqual(response.status_code, 404)

    def test_edit_user_right(self):
        global CREATED_USER
        edited_user_json = put(f"{BASE_API_URL}/users/{CREATED_USER.id}",
                               json={
                                   "name": test_user2.name,
                                   "about": test_user2.about,
                                   "email": test_user2.email,
                                   "hashed_password": "1234567",
                                   "password_again": "1234567"
                               }).json()
        edited_user = CustomUser()
        edited_user.id = edited_user_json["user"]["id"]
        edited_user.name = edited_user_json["user"]["name"]
        edited_user.about = edited_user_json["user"]["about"]
        edited_user.email = edited_user_json["user"]["email"]
        assert edited_user.id == CREATED_USER.id
        assert edited_user.name == test_user2.name
        assert edited_user.about == test_user2.about
        assert edited_user.email == test_user2.email
        # self.assertEqual(edited_user.id, CREATED_USER.id)
        # self.assertEqual(edited_user.name, test_user2.name)
        # self.assertEqual(edited_user.about, test_user2.about)
        # self.assertEqual(edited_user.email, test_user2.email)
        CREATED_USER = edited_user

    def test_edit_user_bad_wrong_user_id(self):
        request = put(f"{BASE_API_URL}/users/-1",
                      json={
                          "name": test_user2.name,
                          "about": test_user2.about,
                          "email": test_user2.email,
                          "hashed_password": "1234567",
                          "password_again": "1234567"
                      })
        assert request.status_code == 404
        # self.assertEqual(request.status_code, 404)

    def test_edit_user_bad_different_passwords(self):
        request = put(f"{BASE_API_URL}/users/{CREATED_USER.id}",
                      json={
                          "name": test_user2.name,
                          "about": test_user2.about,
                          "email": test_user2.email,
                          "hashed_password": "1234567",
                          "password_again": "123"
                      })
        assert request.status_code == 409
        # self.assertEqual(request.status_code, 409)

    def test_delete_user_right(self):
        global CREATED_USER
        deleted_user_id_json = delete(f"{BASE_API_URL}/users/{CREATED_USER.id}").json()
        deleted_user_id = deleted_user_id_json["id"]
        assert deleted_user_id == CREATED_USER.id
        # self.assertEqual(deleted_user_id, CREATED_USER.id)
        CREATED_USER = None

    def test_delete_user_bad_wrong_user_id(self):
        request = delete(f"{BASE_API_URL}/users/-1")
        assert request.status_code == 404
        # self.assertEqual(request.status_code, 404)


def test():
    users_test = TestUsers()
    users_test.test_get_all_users()
    users_test.test_create_user_right()
    users_test.test_create_user_bad_same_email()
    users_test.test_create_user_bad_different_passwords()
    users_test.test_get_one_user_right()
    users_test.test_get_one_user_bad_wrong_user_id()
    users_test.test_edit_user_right()
    users_test.test_edit_user_bad_different_passwords()
    users_test.test_edit_user_bad_wrong_user_id()
    users_test.test_delete_user_right()
    users_test.test_delete_user_bad_wrong_user_id()


if __name__ == '__main__':
    test()
