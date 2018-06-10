import inspect


def get_context_manager(*args):
    """
    Insert base_conext into with_metadata
    """
    def with_metadata(context):
        """
        Update context by view metadata needed to render several things properly
        """
        currentframe = inspect.currentframe()
        outerframe = inspect.getouterframes(currentframe, 1)

        # get the name of function which called this one
        caller_name = outerframe[1][3]
        # get the name of function which called this one
        caller_app = outerframe[1][1].replace("\\", "/").split('/')[-2]

        for app_specific_data in args:
            context.update(app_specific_data)

        context['metadata_active_view'] = caller_name
        context['metadata_active_app'] = caller_app
        return context
    return with_metadata
