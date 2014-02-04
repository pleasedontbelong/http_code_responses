from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.contrib.messages import api as messages_api
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import curry



class SuccessURLRedirectDetailMixin(object):
    """
    Inspired on SuccessURLRedirectListMixin mixin on ``braces``.
    It's used basically with the create and edit CBV
    and it will redirect to the detail view of the element.
    """
    success_detail_url = None
    success_detail_kwarg = None
    success_detail_attribute = None

    def get_success_url(self):
        # Return the reversed success url.
        if None in (self.success_detail_url, self.success_detail_kwarg, self.success_detail_attribute):
            raise ImproperlyConfigured(
                "%(cls)s is missing a class setting "
                "to reverse and redirect. Define "
                "%(cls)s.success_detail_url, success_detail_kwarg and success_detail_attribute"
                "or override %(cls)s.get_success_url()"
                "." % {"cls": self.__class__.__name__})
        return reverse(self.success_detail_url, kwargs={
            self.success_detail_kwarg: getattr(self.object, self.success_detail_attribute)
        })


class MessageWrapper(object):
    """Wrap the django.contrib.messages.api module to automatically pass a given
    request object as the first parameter of function calls.
    """
    def __init__(self, request):
        self.request = request

    def __getattr__(self, attr):
        """Retrieve the function in the messages api and curry it with the
        instance's request.
        """
        fn = getattr(messages_api, attr)
        return curry(fn, self.request)


class MessageMixin(object):
    """Add a `messages` attribute on the view instance that wraps
    `django.contrib .messages`, automatically passing the current request object.
    """
    def dispatch(self, request, *args, **kwargs):
        self.messages = MessageWrapper(request)
        return super(MessageMixin, self).dispatch(request, *args, **kwargs)


class FormMessageMixin(MessageMixin):
    """Add contrib.messages support in views that use FormMixin."""
    form_valid_message = _("Your information has been saved successfully.")
    form_invalid_message = _("Please correct the errors in the form then re-submit.")

    def form_valid(self, form):
        response = super(FormMessageMixin, self).form_valid(form)
        if self.form_valid_message:
            self.messages.success(self.form_valid_message)
        return response

    def form_invalid(self, form):
        response = super(FormMessageMixin, self).form_invalid(form)
        if self.form_invalid_message:
            self.messages.error(self.form_invalid_message)
        return response


class DeleteMessageMixin(MessageMixin):
    """Provide message support to generic.DeleteView."""

    @property
    def delete_message(self):
        msg = _("The %(object_name)s has been deleted.")
        return msg % {'object_name': self.model._meta.verbose_name}

    def delete(self, request, *args, **kwargs):
        response = super(DeleteMessageMixin, self).delete(request, *args, **kwargs)
        self.messages.success(self.delete_message)
        return response


class _NoChangeInstance(object):
    """A proxy for object instances to make safe operations within an
    OnChangeMixin.on_change() callback.
    """

    def __init__(self, instance):
        self.__instance = instance

    def __repr__(self):
        return u'<%s for %r>' % (self.__class__.__name__, self.__instance)

    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, val):
        if attr.endswith('__instance'):
            # _NoChangeInstance__instance
            self.__dict__[attr] = val
        else:
            setattr(self.__instance, attr, val)

    def save(self, *args, **kw):
        kw['_signal'] = False
        return self.__instance.save(*args, **kw)

    def update(self, *args, **kw):
        kw['_signal'] = False
        return self.__instance.update(*args, **kw)


_on_change_callbacks = {}


class OnChangeMixin(object):
    """Mixin for a Model that allows you to observe attribute changes.

    Register change observers with::

        class YourModel(amo.models.OnChangeMixin,
                        amo.models.ModelBase):
            # ...
            pass

        YourModel.on_change(callback)

    """

    def __init__(self, *args, **kw):
        super(OnChangeMixin, self).__init__(*args, **kw)
        self._initial_attr = dict(self.__dict__)

    @classmethod
    def on_change(cls, callback):
        """Register a function to call on save or update to respond to changes.

        For example::

            def watch_status(old_attr={}, new_attr={},
                             instance=None, sender=None, **kw):
                if old_attr.get('status') != new_attr.get('status'):
                    # ...
                    new_instance.save(_signal=False)
            TheModel.on_change(watch_status)

        .. note::

            Any call to instance.save() or instance.update() within a callback
            will not trigger any change handlers.

        """
        _on_change_callbacks.setdefault(cls, []).append(callback)
        return callback

    def _send_changes(self, old_attr, new_attr_kw):
        new_attr = old_attr.copy()
        new_attr.update(new_attr_kw)
        for cb in _on_change_callbacks[self.__class__]:
            cb(old_attr=old_attr, new_attr=new_attr,
               instance=_NoChangeInstance(self), sender=self.__class__)

    def save(self, *args, **kw):
        """
        Save changes to the model instance.

        If _signal=False is in `kw` the on_change() callbacks won't be called.
        """
        signal = kw.pop('_signal', True)
        result = super(OnChangeMixin, self).save(*args, **kw)
        if signal and self.__class__ in _on_change_callbacks:
            self._send_changes(self._initial_attr, dict(self.__dict__))
        return result

    def update(self, **kw):
        """
        Shortcut for doing an UPDATE on this object.

        If _signal=False is in ``kw`` the post_save signal won't be sent.
        """
        signal = kw.pop('_signal', True)
        old_attr = dict(self.__dict__)
        result = super(OnChangeMixin, self).update(**kw)
        if signal and self.__class__ in _on_change_callbacks:
            self._send_changes(old_attr, kw)
        return result