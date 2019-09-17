from apps.product.models import Category


class Utils:

    @staticmethod
    def create_category(parent_category, name):
        category = Category()
        category.name = name
        category.parent = parent_category
        if parent_category:
            category.level = parent_category.level + 1
        else:
            category.level = 1

        category.sort = 0
        category.is_delete = False
        category.is_enable = True
        category.delete_time = None
        category.save()
        return category
