class ProjectDbRouter(object):
    """A router to control all database operations on models in
    the myapp application

    """

    def db_for_read(self, model, **hints):
        """Suggest the database that should be used for read operations
        for objects of type model.

        """
        if model._meta.app_label == "elmotor":
            return "elmotor"
        if model._meta.app_label == "epikur":
            return "epikur"    
        if model._meta.app_label == "computers":
            return "computers"    

        return None

    def db_for_write(self, model, **hints):
        """Suggest the database that should be used for writes of objects
        of type Model.

        """
        if model._meta.app_label == "elmotor":
            return "elmotor"
        if model._meta.app_label == "epikur":
            return "epikur"    
        if model._meta.app_label == "computers":
            return "computers"    

        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Deny any relation if a model in elmotor is involved"""
        if obj1._meta.app_label == "elmotor" or \
                obj2._meta.app_label == "elmotor":
            return False
        if obj1._meta.app_label == "epikur" or \
                obj2._meta.app_label == "epikur":
            return False
        if obj1._meta.app_label == "computers" or \
                obj2._meta.app_label == "computers":
            return False
        return None

    def allow_syncdb(self, db, model):
        """Deny sync db for the elmotor models"""
        if model._meta.app_label == "elmotor":
            return False
        if db == "elmotor":
            return False
        if model._meta.app_label == "epikur":
            return False
        if db == "epikur":
            return False    
        if model._meta.app_label == "computers":
            return False
        if db == "computers":
            return False        
        return None