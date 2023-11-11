from django.apps import AppConfig


class DbGeneralModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    #注意name 属性应该是包含子应用路径的字符串。确保它正确指向你的子应用。
    name = 'utils.db_general_models'
