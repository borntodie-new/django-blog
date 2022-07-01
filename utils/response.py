class Response(object):
    def __init__(self, code='200', message='操作成功', data=None, **kwargs):
        d = {
            'code': code,
            'message': message
        }
        d.update(kwargs)
        if data:
            d['data'] = data
        self.data = d

    def set_code_and_message(self, data=tuple):
        self.data['code'] = data[0]
        self.data['message'] = data[1]
