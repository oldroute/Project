import re
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.conf.urls import url
from django.contrib import messages
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.http import urlquote
from django.utils.translation import ugettext as _
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.utils import quote, unquote
from django.db import router
from django.contrib.admin.utils import get_deleted_objects
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from .models import *


IS_POPUP_VAR = '_popup'
TO_FIELD_VAR = '_to_field'

HORIZONTAL, VERTICAL = 1, 2


class TopicInline(SortableInlineAdminMixin, admin.TabularInline):

    model = Topic
    extra = 0
    fields = ('order_key', 'title')
    show_change_link = True
    readonly_fields = ('title',)

    @property
    def template(self):
        return 'admin/training/topic/tabular.html'


class TaskItemInline(SortableInlineAdminMixin, admin.TabularInline):

    model = TaskItem
    extra = 0
    fields = ('order_key', 'task', 'show')
    raw_id_fields = ("task",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    raw_id_fields = ("author",)
    fields = ('show', 'title', 'author', 'content')
    inlines = (TaskItemInline,)

    def __init__(self, model, admin_site, course=None):
        super().__init__(model, admin_site)
        self._course = course

    def save_model(self, request, obj, form, change):
        obj.course = self._course or obj.course
        obj.save()

    def response_post_save_add(self, request, obj):
        opts = self.model._meta
        if self.has_change_permission(request, None):
            post_url = reverse('admin:training_course_change', args=[obj.course.id], current_app=self.admin_site.name)
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, post_url)
        else:
            post_url = reverse('admin:index',  current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    def response_post_save_change(self, request, obj):

        opts = self.model._meta

        if self.has_change_permission(request, None):
            post_url = reverse('admin:training_course_change', args=[obj.course.id], current_app=self.admin_site.name)
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, post_url)
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    def response_add(self, request, obj, post_url_continue=None):
        """
        Determines the HttpResponse for the add_view stage.
        """
        opts = obj._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)
        obj_url = reverse('admin:change_topic',  args=(self._course.id, quote(pk_value)), current_app=self.admin_site.name,)
        if self.has_change_permission(request, obj):
            obj_repr = format_html('<a href="{}">{}</a>', urlquote(obj_url), obj)
        else:
            obj_repr = force_text(obj)
        msg_dict = {'name': force_text(opts.verbose_name), 'obj': obj_repr}

        if "_continue" in request.POST or (
                # Redirecting after "Save as new".
                "_saveasnew" in request.POST and self.save_as_continue and
                self.has_change_permission(request, obj)
        ):
            msg = format_html(_('The {name} "{obj}" was added successfully. You may edit it again below.'), **msg_dict)
            self.message_user(request, msg, messages.SUCCESS)
            if post_url_continue is None:
                post_url_continue = obj_url
            post_url_continue = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': opts},
                post_url_continue
            )
            return HttpResponseRedirect(post_url_continue)

        elif "_addanother" in request.POST:
            msg = format_html(_('The {name} "{obj}" was added successfully. You may add another {name} below.'), **msg_dict)
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        else:
            msg = format_html(_('The {name} "{obj}" was added successfully.'), **msg_dict)
            self.message_user(request, msg, messages.SUCCESS)
            return self.response_post_save_add(request, obj)

    def response_change(self, request, obj):

        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        msg_dict = {'name': force_text(opts.verbose_name), 'obj': format_html('<a href="{}">{}</a>', urlquote(request.path), obj),}
        if "_continue" in request.POST:
            msg = format_html(_('The {name} "{obj}" was changed successfully. You may edit it again below.'), **msg_dict)
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        elif "_saveasnew" in request.POST:
            msg = format_html(_('The {name} "{obj}" was added successfully. You may edit it again below.'), **msg_dict)
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse('admin:%s_%s_change' % (opts.app_label, opts.model_name), args=(pk_value,), current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        elif "_addanother" in request.POST:
            msg = format_html(_('The {name} "{obj}" was changed successfully. You may add another {name} below.'), **msg_dict)
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse('admin:add_topic', kwargs={'course_pk': obj.course.id}, current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        else:
            msg = format_html(_('The {name} "{obj}" was changed successfully.'), **msg_dict)
            self.message_user(request, msg, messages.SUCCESS)
            return self.response_post_save_change(request, obj)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.update({
            'course': self._course,
            'author': request.user,
            'order_key': Topic.objects.filter(course=self._course).count() + 1
        })
        return initial

    def response_delete(self, request, obj_display, obj_id, course_id):

        opts = self.model._meta

        self.message_user(request, _('The %(name)s "%(obj)s" was deleted successfully.') % {
            'name': force_text(opts.verbose_name),
            'obj': force_text(obj_display),
        }, messages.SUCCESS,)

        if self.has_change_permission(request, None):
            post_url = reverse('admin:training_course_change', args=[course_id], current_app=self.admin_site.name)
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, post_url)
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    def _delete_view(self, request, object_id, extra_context):

        opts = self.model._meta
        app_label = opts.app_label

        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField("The field %s cannot be referenced." % to_field)

        obj = self.get_object(request, unquote(object_id), to_field)

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            return self._get_obj_does_not_exist_redirect(request, opts, object_id)

        using = router.db_for_write(self.model)

        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.
        (deleted_objects, model_count, perms_needed, protected) = get_deleted_objects(
            [obj], opts, request.user, self.admin_site, using)

        if request.POST and not protected:  # The user has confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_text(obj)
            attr = str(to_field) if to_field else opts.pk.attname
            course_id = obj.course.id
            obj_id = obj.serializable_value(attr)
            self.log_deletion(request, obj, obj_display)
            self.delete_model(request, obj)

            return self.response_delete(request, obj_display, obj_id, course_id)

        object_name = force_text(opts.verbose_name)

        if perms_needed or protected:
            title = _("Cannot delete %(name)s") % {"name": object_name}
        else:
            title = _("Are you sure?")

        context = dict(
            self.admin_site.each_context(request),
            title=title,
            object_name=object_name,
            object=obj,
            deleted_objects=deleted_objects,
            model_count=dict(model_count).items(),
            perms_lacking=perms_needed,
            protected=protected,
            opts=opts,
            app_label=app_label,
            preserved_filters=self.get_preserved_filters(request),
            is_popup=(IS_POPUP_VAR in request.POST or
                      IS_POPUP_VAR in request.GET),
            to_field=to_field,
        )
        context.update(extra_context or {})

        return self.render_delete_form(request, context)


@admin.register(Course)
class CourseAdmin(SortableAdminMixin, admin.ModelAdmin):

    model = Course
    list_display = ('order_key', 'title', 'author', 'show')
    list_display_links = ('title',)
    fields = ('show', 'title', 'slug', 'lang', 'author', 'content')
    prepopulated_fields = {'slug': ['title']}
    inlines = [TopicInline]
    raw_id_fields = ("author",)

    def set_instance(self, request):
        object_id = re.search(r'\d+', request.META['PATH_INFO']).group(0)
        self.instance = self.model.objects.get(pk=object_id)

    def get_inline_instances(self, request, obj=None):
        inline_instances = super().get_inline_instances(request, obj)
        if not obj:
            for inline in inline_instances:
                if inline.__class__ == TopicInline:
                    inline_instances.remove(inline)
        return inline_instances

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.set_instance(request)
        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_object_with_change_permissions(self, request, model, obj_pk):
        obj = get_object_or_404(model, pk=obj_pk)
        if not self.has_change_permission(request, obj):
            raise PermissionDenied
        return obj

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial.update({
            'author': request.user,
            'order_key': Course.objects.all().count() + 1
        })
        return initial

    def add_topic(self, request, course_pk):
        course = self.get_object_with_change_permissions(request, Course, course_pk)
        topic_admin = TopicAdmin(Topic, self.admin_site, course)
        return topic_admin.add_view(request, extra_context={'course': course})

    def change_topic(self, request, course_pk, topic_pk):
        course = self.get_object_with_change_permissions(request, Course, course_pk)
        topic_admin = TopicAdmin(Topic, self.admin_site, course)
        return topic_admin.change_view(request, object_id=topic_pk, extra_context={'course': course})

    def get_urls(self):
        return [
            url(r'^(?P<course_pk>[0-9]+)/topics/add/$', self.admin_site.admin_view(self.add_topic), name='add_topic'),
            url(r'^(?P<course_pk>[0-9]+)/topics/(?P<topic_pk>[0-9]+)/change/$', self.admin_site.admin_view(self.change_topic), name='change_topic'),
        ] + super().get_urls()


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    model = Solution
    raw_id_fields = ('user',)