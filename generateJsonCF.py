import requests
import json

# Configurações do ClickUp
clickup_api_key = 'api_key'
team_id = 'teams_id'  # Substitua pelo seu ID de equipe

# Autenticação no ClickUp
headers = {
    'Authorization': clickup_api_key,
}

# Função para obter todas as tarefas em uma lista
def get_all_tasks_in_list(list_id):
    task_response = requests.get(f'https://api.clickup.com/api/v2/list/{list_id}/task', headers=headers)
    task_data = task_response.json()
    return task_data

# Função para obter os campos (fields) de uma lista
def get_fields_in_list(list_id):
    field_response = requests.get(f'https://api.clickup.com/api/v2/list/{list_id}/field', headers=headers)
    field_data = field_response.json()
    return field_data

# Função modificada para obter todas as listas em uma pasta e coletar os campos
def get_all_lists_in_folder(folder_id):
    list_response = requests.get(f'https://api.clickup.com/api/v2/folder/{folder_id}/list', headers=headers)
    list_data = list_response.json()
    
    all_lists = []
    all_fields = []  # Lista para armazenar os campos de todas as listas
    if 'lists' in list_data:
        for task_list in list_data['lists']:
            print('Pegando uma lista')
            list_id = task_list['id']
            tasks = get_all_tasks_in_list(list_id)
            fields = get_fields_in_list(list_id)  # Coleta os dados dos campos
            all_fields.append({'list_id': list_id, 'fields': fields})  # Armazena os campos com o ID da lista correspondente
            all_lists.append({
                'list_info': task_list,
                'tasks': tasks,
            })

    return all_lists, all_fields  # Retorna as listas e os campos coletados

# Função recursiva para obter todas as pastas em um espaço
def get_all_folders_in_space(space_id):
    print('Só pegando mais um espaço!')
    folder_response = requests.get(f'https://api.clickup.com/api/v2/space/{space_id}/folder', headers=headers)
    folder_data = folder_response.json()
    
    all_folders = []
    all_fields = []  # Lista para armazenar os campos de todas as listas em todas as pastas
    if 'folders' in folder_data:
        for folder in folder_data['folders']:
            folder_id = folder['id']
            lists, fields = get_all_lists_in_folder(folder_id)  # Modificado para receber também os campos
            all_folders.append({
                'folder_info': folder,
                'lists': lists,
            })
            all_fields.extend(fields)  # Adiciona os campos desta pasta à lista geral de campos
    return all_folders, all_fields

# Função para obter todas as informações de todos os espaços, pastas e tarefas, agora incluindo campos
def get_all_data_in_all_spaces():
    space_response = requests.get(f'https://api.clickup.com/api/v2/team/{team_id}/space', headers=headers)
    space_data = space_response.json()

    all_spaces = []
    all_fields = []  # Lista para armazenar todos os campos de todas as listas em todos os espaços
    for space in space_data['spaces']:
        print('Pegando mais um espaço')
        space_id = space['id']
        folders, fields = get_all_folders_in_space(space_id)  # Modificado para receber também os campos
        all_spaces.append({
            'space_info': space,
            'folders': folders,
        })
        all_fields.extend(fields)  # Adiciona os campos deste espaço à lista geral de campos

    return all_spaces, all_fields

# Chamada principal para obter todas as informações de todos os espaços
all_data, all_fields = get_all_data_in_all_spaces()

# Salvar os dados em arquivos JSON separados
with open('spaces.json', 'w', encoding='utf-8') as spaces_file:
    json.dump(all_data, spaces_file, ensure_ascii=False, indent=4)

# Salvar os dados dos campos em um novo arquivo JSON
with open('all_fields.json', 'w', encoding='utf-8') as fields_file:
    json.dump(all_fields, fields_file, ensure_ascii=False, indent=4)

print('Dados salvos em arquivos JSON separados: spaces.json e all_fields.json')