import requests

BASE = 'http://127.0.0.1:8080/api/v2/users'


def print_response(label, resp):
    print(f'\n=== {label} ===')
    print(f'Статус: {resp.status_code}')
    try:
        print(f'Тело:  {resp.json()}')
    except Exception:
        print(f'Тело:  {resp.text}')


# GET все пользователи (корректный)
print_response(
    'GET все пользователи',
    requests.get(BASE)
)

# GET один пользователь (корректный)
print_response(
    'GET пользователь id=1',
    requests.get(f'{BASE}/1')
)

# GET несуществующий пользователь (ошибка 404)
print_response(
    'GET пользователь id=9999 — ожидаем 404',
    requests.get(f'{BASE}/9999')
)

# POST создать нового пользователя (корректный)
new_user = {
    'surname': 'Bean',
    'name': 'Sean',
    'age': 40,
    'position': 'pilot',
    'speciality': 'navigator',
    'address': 'Mars base 2',
    'email': 'bean@mars.org',
    'city_from': 'Sheffield',
}
post_resp = requests.post(BASE, json=new_user)
print_response('POST создать пользователя', post_resp)

# сохраним id созданного пользователя для delete
new_id = post_resp.json().get('id') if post_resp.ok else None

# POST с пустым телом (ошибка 400)
print_response(
    'POST пустой запрос — ожидаем 400',
    requests.post(BASE, json={})
)

# POST дублирующийся email (ошибка)
print_response(
    'POST дублирующийся email — ожидаем ошибку',
    requests.post(BASE, json={**new_user, 'surname': 'Clone'})
)

# DELETE созданного пользователя (корректный)
if new_id:
    print_response(
        f'DELETE пользователь id={new_id}',
        requests.delete(f'{BASE}/{new_id}')
    )
    # проверяем, что действительно удалён
    print_response(
        f'GET после DELETE id={new_id} — ожидаем 404',
        requests.get(f'{BASE}/{new_id}')
    )

#DELETE несуществующего пользователя (ошибка 404)
print_response(
    'DELETE пользователь id=9999 — ожидаем 404',
    requests.delete(f'{BASE}/9999')
)