from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.helpers import PageButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import BlogPage


class ArticleButtonHelper(PageButtonHelper):
    def my_button(self, url=None):
        return {
            'url': url,
            'label': _('Frontend version'),
            'classname': 'button button-small button-secondary',
            'title': _('Frontend version'),
        }

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None,
                            classnames_exclude=None):
        btns = super().get_buttons_for_obj(
            obj, exclude=exclude, classnames_add=classnames_add, classnames_exclude=classnames_exclude)
        btns.append(self.my_button(url=obj.url))
        return btns


class PostsAdmin(ModelAdmin):
    model = BlogPage
    button_helper_class = ArticleButtonHelper
    menu_label = _('Blog Posts')  # ditch this to use verbose_name_plural from model
    menu_icon = 'edit'  # change as required
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    add_to_settings_menu = False  # or True to add your model to the Settings sub-menu
    exclude_from_explorer = False  # or True to exclude pages of this type from Wagtail's explorer view
    list_display = ('title', 'date', 'live')
    list_filter = ('date', )
    search_fields = ('title', 'body')
    ordering = ['-date']
    list_per_page = 20


modeladmin_register(PostsAdmin)
