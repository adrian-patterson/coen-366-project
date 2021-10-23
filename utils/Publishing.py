class Publish:
    def __init__(self, rq, name, list_of_files):
        self.rq = rq
        self.name = name
        self.list_of_files = list_of_files

    def __str__(self):
        return f"""
    PUBLISH
        RQ:\t\t{self.rq}
        NAME:\t{self.name}
        LIST OF FILES:\t{self.list_of_files}
        """


class Published:
    def __init__(self, rq):
        self.rq = rq

    def __str__(self):
        return f"""
    PUBLISHED
        RQ:\t\t{self.rq}
        """


class PublishDenied:
    def __init__(self, rq, reason):
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    PUBLISH DENIED
        RQ:\t\t{self.rq}
        REASON:\t{self.reason}
        """


class Remove:
    def __init__(self, rq, name, list_of_files_to_remove):
        self.rq = rq
        self.name = name
        self.list_of_files_to_remove = list_of_files_to_remove

    def __str__(self):
        return f"""
    REMOVE
        RQ:\t\t{self.rq}
        NAME:\t{self.name}
        LIST OF FILES TO REMOVE:\t{self.list_of_files_to_remove}
        """


class Removed:
    def __init__(self, rq):
        self.rq = rq

    def __str__(self):
        return f"""
    REMOVED
        RQ:\t\t{self.rq}
        """


class RemoveDenied:
    def __init__(self, rq, reason):
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    REMOVE DENIED
        RQ:\t\t{self.rq}
        REASON:\t{self.reason}
        """
