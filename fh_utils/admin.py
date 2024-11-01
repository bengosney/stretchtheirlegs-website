class StatusAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status", *self.list_display]
        self.list_filter = ["status", *list(self.list_filter)]


class DatePeriodAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["show_from", "show_to", *list(self.list_display)]
        self.list_filter = ["show_from", "show_to", *list(self.list_filter)]


class DateAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status", "published", *list(self.list_display)]
        self.list_filter = ["status", "published", *list(self.list_filter)]


class DateRangeAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status", "published_from", "published_to", *list(self.list_display)]
        self.list_filter = ["status", "published_from", "published_to", *list(self.list_filter)]
