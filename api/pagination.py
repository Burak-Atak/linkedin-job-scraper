import types
from collections import OrderedDict
from itertools import chain

import six
from django.core.paginator import (
    InvalidPage,
)

from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class Pagination(PageNumberPagination):
    page_size_query_param = "limit"

    def paginate_queryset(self, queryset, request, view=None):
        page_size = self.get_page_size(request)
        if page_size:
            # check if queryset is ordered
            # if not, apply ordering with pk field to avoid UnorderedObjectListWarning
            ordered = getattr(queryset, 'ordered', None)
            if ordered is not None and not ordered:
                pk_field = getattr(queryset.model._meta, 'pk', None)
                if pk_field is not None:
                    # pk_field is an AutoField
                    queryset = queryset.order_by(pk_field.name)
            paginator = self.django_paginator_class(queryset, page_size)
            page_number = request.query_params.get(self.page_query_param, 1)
            if page_number in self.last_page_strings:
                page_number = paginator.num_pages

            try:
                self.page = paginator.page(page_number)
            except InvalidPage as exc:
                msg = self.invalid_page_message.format(
                    page_number=page_number, message=six.text_type(exc)
                )
                raise NotFound(msg)

            if paginator.num_pages > 1 and self.template is not None:
                # The browsable API should display pagination controls.
                self.display_page_controls = True

            self.request = request
            for page_item in self.page:
                yield page_item

    def get_paginated_response(self, data):
        def gen(first):
            yield first

        if isinstance(data, types.GeneratorType):
            try:
                first_record = next(data)
            except (StopIteration,):
                data = []
            else:
                data = chain(gen(first_record), data)
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
