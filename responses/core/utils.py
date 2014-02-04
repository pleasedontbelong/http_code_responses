from django.db.models.query import QuerySet

from celery import group


def chop_queryset(queryset, size=10000, values_list=None):
    """generator that split the given :arg queryset: in chunks of :arg size:
    elements. :arg queryset: may be any iterable. in this case,
    :arg values_list: is ignored.

    If :arg values_list: is not None (the default), queryset.values_list()
    is applied.

    If :arg values_list: has a single element, the returned list is flattend.

    Note: this function executes the queryset.
    """
    # apply values_list
    if isinstance(queryset, QuerySet) and values_list:
        if len(values_list) == 1:
            kwargs = {'flat': True}
        else:
            kwargs = {}
        queryset = queryset.values_list(*values_list, **kwargs)
    # split the queryset
    try:
        total = queryset.count()
    except (TypeError, AttributeError):
        total = len(queryset)
    cycles = 0
    while total > 0:
        offset = cycles * size
        if total < size:
            size = total
        cycles += 1
        total -= size
        yield queryset[offset:offset + size]


def chop_and_apply(queryset, task, size=10000, values_list=None, async=True):
    """Apply the Celery :arg task: (as a subtask) to each chunks of the
    :arg queryset:. The :arg queryset: is chopped using :function chop_queryset:
    :arg size: and :arg values_list: are passed as is.
    """
    job = group(task.subtask([chunk]) for chunk in
                chop_queryset(queryset, size, values_list))
    if async:
        result = job.apply_async()
    else:
        result = job.apply()
    return result
