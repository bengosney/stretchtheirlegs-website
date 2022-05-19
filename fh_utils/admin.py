# Django


class statusAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status"] + list(self.list_display)
        self.list_filter = ["status"] + list(self.list_filter)


class datePeriodAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["show_from", "show_to"] + list(self.list_display)
        self.list_filter = ["show_from", "show_to"] + list(self.list_filter)


class dateAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status", "published"] + list(self.list_display)
        self.list_filter = ["status", "published"] + list(self.list_filter)


class dateRangeAdmin:
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        self.list_display = ["status", "published_from", "published_to"] + list(self.list_display)
        self.list_filter = ["status", "published_from", "published_to"] + list(self.list_filter)
