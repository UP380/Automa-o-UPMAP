import requests
import json

# Configurações do ClickUp
clickup_api_key = 'pk_60972141_HQNP13ADG96CMTETEOP5GSNJ4HVGKP0J'
team_id = '9007138778'  # Substitua pelo seu ID de equipe

# Autenticação no ClickUp
headers = {
    'Authorization': clickup_api_key,
}

# Função para obter todas as tarefas em uma lista
def get_all_tasks_in_list(list_id):
    task_response = requests.get(f'https://api.clickup.com/api/v2/list/{list_id}/task', headers=headers)
    task_data = task_response.json()
    return task_data

# Função recursiva para obter todas as listas em uma pasta
def get_all_lists_in_folder(folder_id):
    list_response = requests.get(f'https://api.clickup.com/api/v2/folder/{folder_id}/list', headers=headers)
    list_data = list_response.json()
    
    all_lists = []
    if 'lists' in list_data:
        for task_list in list_data['lists']:
            print('pegando uma list🤝')
            list_id = task_list['id']
            tasks = get_all_tasks_in_list(list_id)
            all_lists.append({
                'list_info': task_list,
                'tasks': tasks,
            })

    return all_lists

# Função recursiva para obter todas as pastas em um espaço
def get_all_folders_in_space(space_id):
    print('So pegando mais um space!')
    folder_response = requests.get(f'https://api.clickup.com/api/v2/space/{space_id}/folder', headers=headers)
    folder_data = folder_response.json()
    
    all_folders = []
    if 'folders' in folder_data:
        for folder in folder_data['folders']:
            folder_id = folder['id']
            lists = get_all_lists_in_folder(folder_id)
            all_folders.append({
                'folder_info': folder,
                'lists': lists,
            })
    print('passou aqui tambem ta tudo certo👍')
    return all_folders

# Função para obter todas as informações de todos os espaços, pastas e tarefas
def get_all_data_in_all_spaces():
    space_response = requests.get(f'https://api.clickup.com/api/v2/team/{team_id}/space', headers=headers)
    space_data = space_response.json()

    all_spaces = []
    for space in space_data['spaces']:
        print('Pegando mais um space😁')
        space_id = space['id']
        folders = get_all_folders_in_space(space_id)
        all_spaces.append({
            'space_info': space,
            'folders': folders,
        })

    return all_spaces

# Chame a função para obter todas as informações de todos os espaços
all_data = get_all_data_in_all_spaces()

# Salvar os dados em três arquivos JSON separados
with open('spaces.json', 'w', encoding='utf-8') as spaces_file:
    json.dump(all_data, spaces_file, ensure_ascii=False, indent=4)

# Criar listas separadas para espaços, pastas e tarefas
all_spaces = []
all_folders = []
all_tasks = []

for space_info in all_data:
    print('Setando spaces🌚')
    all_spaces.append(space_info['space_info'])
    for folder_info in space_info['folders']:
        print('Coletando folders✅')
        all_folders.append(folder_info['folder_info'])
        for list_info in folder_info['lists']:
            print('Setando o Json das lists📋')
            all_tasks.extend(list_info['tasks'])

# Salvar os dados de espaços, pastas e tarefas em arquivos JSON separados
#with open('all_spaces.json', 'w', encoding='utf-8') as all_spaces_file:
#    json.dump(all_spaces, all_spaces_file, ensure_ascii=False, indent=4)
#
#with open('all_folders.json', 'w', encoding='utf-8') as all_folders_file:
#    json.dump(all_folders, all_folders_file, ensure_ascii=False, indent=4)
#
#with open('all_tasks.json', 'w', encoding='utf-8') as all_tasks_file:
#    json.dump(all_tasks, all_tasks_file, ensure_ascii=False, indent=4)

print('Dados salvos em arquivos JSON separados: spaces.json, all_spaces.json, all_folders.json e all_tasks.json')
