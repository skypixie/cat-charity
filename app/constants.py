# MODELS
MIN_PROJ_NAME_LENGTH = 5
MAX_PROJ_NAME_LENGTH = 100
MIN_PROJ_DESC_LENGTH = 10

# ERROR MESSAGES
ERR_MSG_DUPLICATE_PROJECT = 'Проект с таким именем уже существует!'
ERR_MSG_CANT_FIND_PROJECT = 'Проекта с таким id не существует!'
ERR_MSG_CLOSED_PROJECT = 'Закрытый проект нельзя редактировать!'
ERR_MSG_CANT_LOWER_AMOUNT = (
    'Нелья установить значение '
    'full_amount меньше уже вложенной суммы.'
)
ERR_MSG_CANT_DELETE_PROJECT = (
    'В проект были внесены средства, не подлежит удалению!'
)

# ERROR CODES
ERR_CODE_DUPLICATE_PROJECT = 400
ERR_CODE_CANT_FIND_PROJECT = 404
ERR_CODE_CLOSED_PROJECT = 400
ERR_CODE_CANT_LOWER_AMOUNT = 400
ERR_CODE_CANT_DELETE_PROJECT = 400
