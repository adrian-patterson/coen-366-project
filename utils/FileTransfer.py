class Download:
    def __init__(self, rq, file_name):
        self.rq = rq
        self.file_name = file_name

    def __str__(self):
        return f"""
    DOWNLOAD
        RQ:\t{self.rq}
        FILE NAME:\t{self.file_name}
        """


class File:
    def __init__(self, rq, file_name, chunk, text):
        self.rq = rq
        self.file_name = file_name
        self.chunk = chunk
        self.text = text

    def __str__(self):
        return f"""
    FILE
        RQ:\t{self.rq}
        FILE NAME:\t{self.file_name}
        CHUNK:\t{self.chunk}
        TEXT:\t{self.text}
        """


class FileEnd:
    def __init__(self, rq, file_name, chunk, text):
        self.rq = rq
        self.file_name = file_name
        self.chunk = chunk
        self.text = text

    def __str__(self):
        return f"""
    FILE END
        RQ:\t{self.rq}
        FILE NAME:\t{self.file_name}
        CHUNK:\t{self.chunk}
        TEXT:\t{self.text}
        """


class DownloadError:
    def __init__(self, rq, reason):
        self.rq = rq
        self.reason = reason

    def __str__(self):
        return f"""
    DOWNLOAD ERROR
        RQ:\t{self.rq}
        REASON:\t{self.reason}
        """
