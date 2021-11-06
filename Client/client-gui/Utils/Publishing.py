class Publish:

    def __init__(self, rq, name, list_of_files, **_):
        self.TYPE = "PUBLISH"
        self.rq = rq
        self.name = name
        self.list_of_files = list_of_files

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        NAME:\t{self.name}
        LIST OF FILES:\t{self.list_of_files}
        """


class Published:

    def __init__(self, rq, **_):
        self.TYPE = "PUBLISHED"
        self.rq = rq

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        """


class PublishDenied:

    def __init__(self, rq, reason, **_):
        self.TYPE = "PUBLISH-DENIED"
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        REASON:\t{self.reason}
        """


class Remove:

    def __init__(self, rq, name, list_of_files_to_remove, **_):
        self.TYPE = "REMOVE"
        self.rq = rq
        self.name = name
        self.list_of_files_to_remove = list_of_files_to_remove

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        NAME:\t{self.name}
        LIST OF FILES TO REMOVE:\t{self.list_of_files_to_remove}
        """


class Removed:

    def __init__(self, rq, **_):
        self.TYPE = "REMOVED"
        self.rq = rq

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t\t{self.rq}
        """


class RemoveDenied:

    def __init__(self, rq, reason, **_):
        self.TYPE = "REMOVE-DENIED"
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        REASON:\t{self.reason}
        """
