from datetime import datetime

from sqlalchemy_easy_softdelete.hook import IgnoredTable
from sqlalchemy_easy_softdelete.mixin import generate_soft_delete_mixin_class


class SoftDeleteMixin(generate_soft_delete_mixin_class(ignored_tables=[IgnoredTable(table_schema="public", name="roles"),]
)):
    """
    Mixin para soft delete
    https://pypi.org/project/sqlalchemy-easy-softdelete/
    """
    deleted_at: datetime