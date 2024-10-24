from django.contrib import admin

from myApp.models import *

admin.site.register(custom_user)
admin.site.register(BasicInfoModel)
admin.site.register(skillModel)
admin.site.register(intermediate_skillModel)
admin.site.register(LanguageModel)
admin.site.register(intermediate_LanguageModel)
admin.site.register(experienceModel)
admin.site.register(intermediate_experienceModel)
admin.site.register(educationModel)
admin.site.register(intermediate_educationModel)
admin.site.register(interestModel)
admin.site.register(intermediate_interestModel)
admin.site.register(JobModel)
admin.site.register(jobApplyModel)


