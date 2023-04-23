from helpers.CONSTS import BASE_API_URL

from requests import get, post, put, delete


class CustomNews:
    pass


CREATED_NEWS = None
CREATED_USER_ID = None

test_news = CustomNews()
test_news.title = "Title test"
test_news.content = "Content testContent testContent testContent testContent testContent testContent test"
test_news.is_private = False

test_news2 = CustomNews()
test_news2.title = "Title test1"
test_news2.content = "Content testContent testContent testContent testContent testContent testContent test1"
test_news2.is_private = True


class TestNews:
    def test_get_all_news(self):
        all_news_json = get(f"{BASE_API_URL}/news").json()
        all_news = all_news_json["news"]
        assert isinstance(all_news, list)
        # self.assertIsInstance(all_news, list)

    def test_create_news_right(self):
        global CREATED_USER_ID, CREATED_NEWS
        CREATED_USER_ID = post(f"{BASE_API_URL}/users",
                               json={
                                   "name": "test",
                                   "about": "test",
                                   "email": "test1321434@test.test",
                                   "hashed_password": "123456",
                                   "password_again": "123456"
                               }).json()['user']['id']

        created_news_json = post(f"{BASE_API_URL}/news",
                                 json={'title': test_news.title,
                                       'content': test_news.content,
                                       'user_id': CREATED_USER_ID,
                                       'is_private': test_news.is_private}).json()
        created_news = CustomNews()
        created_news.id = created_news_json["news"]["id"]
        created_news.title = created_news_json["news"]["title"]
        created_news.content = created_news_json["news"]["content"]
        created_news.user_id = created_news_json["news"]["user"]["id"]
        created_news.created_date = created_news_json["news"]["created_date"]
        created_news.is_private = created_news_json["news"]["is_private"]
        assert created_news.title == test_news.title
        assert created_news.content == test_news.content
        assert created_news.user_id == CREATED_USER_ID
        assert created_news.is_private == test_news.is_private
        # self.assertEqual(created_news.title, test_news.title)
        # self.assertEqual(created_news.content, test_news.content)
        # self.assertEqual(created_news.user_id, CREATED_USER_ID)
        # self.assertEqual(created_news.is_private, test_news.is_private)
        CREATED_NEWS = created_news

    def test_create_news_bad_user_id(self):
        request = post(f"{BASE_API_URL}/news",
                       json={'title': 'Заголовок',
                             'content': 'Текст новости',
                             'user_id': -1,
                             'is_private': False})
        assert request.status_code == 404
        # self.assertEqual(request.status_code, 404)

    def test_get_news_right(self):
        news_json = get(f"{BASE_API_URL}/news/{CREATED_NEWS.id}").json()
        news = CustomNews()
        news.id = news_json["news"]["id"]
        news.title = news_json["news"]["title"]
        news.content = news_json["news"]["content"]
        news.user_id = news_json["news"]["user"]["id"]
        assert news.id == CREATED_NEWS.id
        assert news.title == CREATED_NEWS.title
        assert news.content == CREATED_NEWS.content
        assert news.user_id == CREATED_NEWS.user_id

    def test_get_news_bad_wrong_news_id(self):
        response = get(f"{BASE_API_URL}/news/-1")
        assert response.status_code == 404

    def test_edit_news_right(self):
        global CREATED_NEWS
        edited_news_json = put(f"{BASE_API_URL}/news/{CREATED_NEWS.id}",
                               json={'title': test_news2.title,
                                     'content': test_news2.content,
                                     'user_id': CREATED_USER_ID,
                                     'is_private': test_news2.is_private}).json()
        edited_news = CustomNews()
        edited_news.id = edited_news_json["news"]["id"]
        edited_news.title = edited_news_json["news"]["title"]
        edited_news.content = edited_news_json["news"]["content"]
        edited_news.user_id = edited_news_json["news"]["user"]["id"]
        edited_news.created_date = edited_news_json["news"]["created_date"]
        edited_news.is_private = edited_news_json["news"]["is_private"]
        assert edited_news.id == CREATED_NEWS.id
        assert edited_news.title == test_news2.title
        assert edited_news.content == test_news2.content
        assert edited_news.user_id == CREATED_USER_ID
        assert edited_news.is_private == test_news2.is_private
        # self.assertEqual(edited_news.id, CREATED_NEWS.id)
        # self.assertEqual(edited_news.title, test_news2.title)
        # self.assertEqual(edited_news.content, test_news2.content)
        # self.assertEqual(edited_news.user_id, CREATED_USER_ID)
        # self.assertEqual(edited_news.is_private, test_news2.is_private)
        CREATED_NEWS = edited_news

    def test_edit_news_bad_wrong_news_id(self):
        request = put(f"{BASE_API_URL}/news/-1",
                      json={'title': test_news2.title,
                            'content': test_news2.content,
                            'user_id': CREATED_USER_ID,
                            'is_private': test_news2.is_private})
        assert request.status_code == 404
        # self.assertEqual(request.status_code, 404)

    def test_edit_news_bad_wrong_user_id(self):
        request = put(f"{BASE_API_URL}/news/{CREATED_NEWS.id}",
                      json={'title': test_news2.title,
                            'content': test_news2.content,
                            'user_id': -1,
                            'is_private': test_news2.is_private})
        assert request.status_code == 404
        # self.assertEqual(request.status_code, 404)

    def test_edit_news_bad_user_has_no_permissions(self):
        second_test_user_id = post(f"{BASE_API_URL}/users",
                                   json={
                                       "name": "test",
                                       "about": "test",
                                       "email": "test1765465433456@test.test",
                                       "hashed_password": "123456",
                                       "password_again": "123456"
                                   }).json()['user']['id']
        request = put(f"{BASE_API_URL}/news/{CREATED_NEWS.id}",
                      json={'title': test_news2.title,
                            'content': test_news2.content,
                            'user_id': second_test_user_id,
                            'is_private': test_news2.is_private})
        assert request.status_code == 403
        # self.assertEqual(request.status_code, 403)
        temp = delete(f"{BASE_API_URL}/users/{second_test_user_id}").json()['id']
        assert second_test_user_id == temp
        # self.assertEqual(second_test_user_id, temp)

    def test_delete_news_bad_news_id(self):
        request = delete(f"{BASE_API_URL}/news/-1?is_authenticated=True&user_id={CREATED_USER_ID}")
        assert request.status_code == 404
        # self.assertEqual(request.status_code, 404)

    def test_delete_news_bad_user_id(self):
        request = delete(f"{BASE_API_URL}/news/{CREATED_NEWS.id}?is_authenticated=True&user_id=-1")
        assert request.status_code == 404
        # self.assertEqual(request.status_code, 404)

    def test_delete_news_bad_user_has_no_permissions(self):
        second_test_user_id = post(f"{BASE_API_URL}/users",
                                   json={
                                       "name": "test",
                                       "about": "test",
                                       "email": "test1765465433456@test.test",
                                       "hashed_password": "123456",
                                       "password_again": "123456"
                                   }).json()['user']['id']
        request = delete(f"{BASE_API_URL}/news/{CREATED_NEWS.id}?is_authenticated=True&user_id={second_test_user_id}")
        assert request.status_code == 403
        # self.assertEqual(request.status_code, 403)
        temp = delete(f"{BASE_API_URL}/users/{second_test_user_id}").json()['id']
        assert second_test_user_id == temp
        # self.assertEqual(second_test_user_id, temp)

    def test_delete_news_right(self):
        global CREATED_NEWS, CREATED_USER_ID
        query = f"?is_authenticated=True&user_id={CREATED_USER_ID}"
        deleted_news_id_json = delete(f"{BASE_API_URL}/news/{CREATED_NEWS.id}" + query).json()
        deleted_news_id = deleted_news_id_json['id']
        assert deleted_news_id == CREATED_NEWS.id
        # self.assertEqual(deleted_news_id, CREATED_NEWS.id)
        CREATED_NEWS = None
        temp = delete(f"{BASE_API_URL}/users/{CREATED_USER_ID}").json()['id']
        assert CREATED_USER_ID == temp
        # self.assertEqual(CREATED_USER_ID, temp)
        CREATED_USER_ID = None


def test():
    news_tests = TestNews()
    news_tests.test_get_all_news()
    news_tests.test_create_news_right()
    news_tests.test_create_news_bad_user_id()
    news_tests.test_get_news_right()
    news_tests.test_get_news_bad_wrong_news_id()
    news_tests.test_edit_news_right()
    news_tests.test_edit_news_bad_user_has_no_permissions()
    news_tests.test_edit_news_bad_wrong_news_id()
    news_tests.test_edit_news_bad_wrong_user_id()
    news_tests.test_delete_news_bad_news_id()
    news_tests.test_delete_news_bad_user_has_no_permissions()
    news_tests.test_delete_news_bad_user_id()
    news_tests.test_delete_news_right()


if __name__ == '__main__':
    test()
