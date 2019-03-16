from flask import url_for
from flask import current_app


class PaginationHelper:
    def __init__(self, request, **kwargs):
        self.request = request
        self.query = kwargs.get("query")
        self.resource_for_url = kwargs.get("resource_for_url")
        self.key_name = kwargs.get("key_name", "results")
        self.schema = kwargs.get("schema")
        self.results_per_page = current_app.config["POSTS_PER_PAGE"]
        self.page_argument_name = current_app.config["PAGINATION_PAGE_ARGUMENT_NAME"]
        self.per_page_argument_name = current_app.config["PAGINATION_PER_PAGE_ARGUMENT_NAME"]

    def paginate_query(self):
        # If no page number is specified, we assume the request wants page #1
        page_number = self.request.args.get(self.page_argument_name, 1, type=int)
        results_per_page = self.request.args.get(
            self.per_page_argument_name, current_app.config["POSTS_PER_PAGE"], type=int
        )
        paginated_objects = self.query.paginate(page_number, per_page=results_per_page, error_out=False)
        objects = paginated_objects.items
        if paginated_objects.has_prev:
            previous_page_url = url_for(self.resource_for_url, page=page_number - 1, _external=True)
        else:
            previous_page_url = None
        if paginated_objects.has_next:
            next_page_url = url_for(self.resource_for_url, page=page_number + 1, _external=True)
        else:
            next_page_url = None
        dumped_objects = self.schema.dump(objects, many=True).data
        return {
            self.key_name: dumped_objects,
            "previous": previous_page_url,
            "next": next_page_url,
            "count": paginated_objects.total,
            self.per_page_argument_name: results_per_page,
        }
