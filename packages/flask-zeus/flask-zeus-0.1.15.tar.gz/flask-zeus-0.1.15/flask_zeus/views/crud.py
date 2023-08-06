from flask import (request, url_for, flash, redirect)
from flask_login import (login_required, current_user)
from .base import BaseView


class BaseFormView(BaseView):
    form = None
    csrf_enabled = False
    success_message = None
    methods = ['GET', 'POST']
    decorators = [login_required]

    def get_form(self, obj=None, **kwargs):
        """ 获取 wtforms 表单"""
        if not self.form:
            raise AttributeError('需要设置form值')

        form = self.form(obj=obj, csrf_enabled=self.csrf_enabled)

        for k, v in kwargs.items():
            if form.has_field(k):
                form.field.data = v

        return form

    def get_next_url(self, **kwargs):
        """ 获取跳转链接 """
        return request.args.get('next') or url_for(request.endpoint, **kwargs)


class CreateView(BaseFormView):

    def dispatch_request(self, **kwargs):
        form = self.get_form(**kwargs)

        if form.validate_on_submit():

            item = self.model()

            for k, v in form.data.iteritems():
                setattr(item, k, v)

            if self.model.has_property('user_id'):
                item.user_id = current_user.id

            item.save()
            self.append_context('item', item)

            if self.success_message:
                flash(self.success_message, category='success')

            return redirect(self.get_next_url(**kwargs))

        self.append_context('form', form)
        return self.render(**self.context)


class UpdateView(BaseFormView):

    def dispatch_request(self, **kwargs):

        stmt = self.get_query(**kwargs)
        item = stmt.first_or_404()

        form = self.get_form(obj=item, **kwargs)

        if form.validate_on_submit():

            for k, v in form.data.iteritems():
                setattr(item, k, v)

            if self.model.has_property('user_id'):
                item.user_id = current_user.id

            item.save()
            self.append_context('item', item)

            if self.success_message:
                flash(self.success_message, category='success')

            return redirect(self.get_next_url(**kwargs))

        self.append_context('form', form)
        return self.render(**self.context)