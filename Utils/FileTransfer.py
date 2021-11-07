class Download:

    def __init__(self, rq, file_name, **_):
        self.TYPE = "DOWNLOAD"
        self.rq = rq
        self.file_name = file_name

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        FILE NAME:\t{self.file_name}
        """


class File:

    def __init__(self, rq, file_name, chunk, text, **_):
        self.TYPE = "FILE"
        self.rq = rq
        self.file_name = file_name
        self.chunk = chunk
        self.text = text

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        FILE NAME:\t{self.file_name}
        CHUNK:\t{self.chunk}
        TEXT:\t{self.text}
        """


class FileEnd:

    def __init__(self, rq, file_name, chunk, text, **_):
        self.TYPE = "FILE-END"
        self.rq = rq
        self.file_name = file_name
        self.chunk = chunk
        self.text = text

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        FILE NAME:\t{self.file_name}
        CHUNK:\t{self.chunk}
        TEXT:\t{self.text}
        """


class DownloadError:

    def __init__(self, rq, reason, **_):
        self.TYPE = "DOWNLOAD-ERROR"
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    {self.TYPE}
        RQ:\t{self.rq}
        REASON:\t{self.reason}
        """
