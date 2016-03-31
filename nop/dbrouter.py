class NopRouter(object):
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'nop':
            return db == 'nop'
        return None
