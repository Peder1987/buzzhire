from configurations_seddonym import StandardConfiguration
import os


class ProjectConfiguration(StandardConfiguration):
#     BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#     STATICFILES_DIRS = (
#         os.path.join(BASE_DIR, "static"),
#     )

    PROJECT_NAME = 'buzzhire'
    INSTALLED_APPS = StandardConfiguration.INSTALLED_APPS + (
        # Apps lower down the list should import from apps higher up the list,
        # and not the other way around
        'django.contrib.humanize',
        # 'sorl.thumbnail',
        # 'dbbackup',
    )

    # TEMPLATE_CONTEXT_PROCESSORS += (
    #     'apps.main.context_processors.main',
    # )
