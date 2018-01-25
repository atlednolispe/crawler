class Head:
    @staticmethod
    def format(request_heads):
        """
        Format chrome request headers to headers lib of requests needed.
        """
        headers = {}
        head_lists = request_heads.strip().split('\n')[:-1]
        for head in head_lists:
            item = head.split(': ')
            key, value = item[0], item[-1]
            headers[key] = value
        return headers
