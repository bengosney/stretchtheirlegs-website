class adminManagerAdmin:
    def get_queryset(self, request):
        try:
            qs = self.model.admin_objects.get_queryset()
        except AttributeError:
            qs = self.model._default_manager.get_queryset()

        if ordering := self.get_ordering(request):
            qs = qs.order_by(*ordering)
        if self.is_pagemodel:
            # If we're listing pages, exclude the root page
            qs = qs.exclude(depth=1)
        return qs


class statusAdmin(adminManagerAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status"] + list(self.list_display)
        self.list_filter = ["status"] + list(self.list_filter)


class datePeriodAdmin(adminManagerAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["show_from", "show_to"] + list(self.list_display)
        self.list_filter = ["show_from", "show_to"] + list(self.list_filter)


class dateAdmin(adminManagerAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status", "published"] + list(self.list_display)
        self.list_filter = ["status", "published"] + list(self.list_filter)


class dateRangeAdmin(adminManagerAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status", "published_from", "published_to"] + list(self.list_display)
        self.list_filter = ["status", "published_from", "published_to"] + list(self.list_filter)
