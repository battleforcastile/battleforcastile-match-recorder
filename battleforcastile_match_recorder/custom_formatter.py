import logging

# Custom formatter returns a structure, than a string
class CustomFormatter(logging.Formatter):
    def format(self, record):
        log_msg = super(CustomFormatter, self).format(record)
        return {
            'msg': log_msg,
            'args': record.args,
        }