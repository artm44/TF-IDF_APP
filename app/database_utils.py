from sqlalchemy import exc


# Декоратор для подтверждения выполнения операций CUD в БД
def commit_cud_operation(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except exc.SQLAlchemyError as ex:
            print(ex)
            return False
        return result

    return wrapper
