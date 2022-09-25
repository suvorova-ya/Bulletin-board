from django.apps import AppConfig



class ProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project'
    verbose_name = 'Доска объвлений'

    def ready(self):
        import project.signals


