import requests

BASE = 'http://127.0.0.1:8080/api/v2/jobs'


def print_response(label, resp):
    print(f'\n=== {label} ===')
    print(f'Статус: {resp.status_code}')
    try:
        print(f'Тело:  {resp.json()}')
    except Exception:
        print(f'Тело:  {resp.text}')


# GET все работы (корректный)
print_response('GET все работы', requests.get(BASE))

# GET одна работа (корректный)
print_response('GET работа id=1', requests.get(f'{BASE}/1'))

# GET несуществующая работа (ошибка 404)
print_response('GET работа id=9999 - ожидаем 404', requests.get(f'{BASE}/9999'))

# POST создать работу (корректный)
new_job = {
    'job': 'Atmospheric pressure monitoring',
    'work_size': 10,
    'collaborators': '2, 3',
    'team_leader': 1,
    'is_finished': False,
}
post_resp = requests.post(BASE, json=new_job)
print_response('POST создать работу', post_resp)
new_id = post_resp.json().get('id') if post_resp.ok else None

# POST без обязательного поля job (ошибка 400)
print_response('POST без поля job - ожидаем 400', requests.post(BASE, json={'work_size': 5, 'team_leader': 1}))

# POST с пустым телом (ошибка 400)
print_response('POST пустой запрос - ожидаем 400', requests.post(BASE, json={}))

# PUT обновить работу (корректный)
if new_id:
    print_response(
        f'PUT обновить работу id={new_id}', requests.put(f'{BASE}/{new_id}', json={'is_finished': True, 'work_size': 20})
    )
    # проверяем что изменения применились
    print_response(f'GET после PUT id={new_id}', requests.get(f'{BASE}/{new_id}'))

# PUT несуществующей работы (ошибка 404)
print_response('PUT работа id=9999 - ожидаем 404', requests.put(f'{BASE}/9999', json={'is_finished': True}))

# DELETE созданной работы (корректный)
if new_id:
    print_response(f'DELETE работа id={new_id}', requests.delete(f'{BASE}/{new_id}'))
    # проверяем что удалена
    print_response(f'GET после DELETE id={new_id} - ожидаем 404', requests.get(f'{BASE}/{new_id}'))

# DELETE несуществующей работы (ошибка 404)
print_response('DELETE работа id=9999 - ожидаем 404', requests.delete(f'{BASE}/9999'))
