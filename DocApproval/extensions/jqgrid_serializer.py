class JqgridSerializer():
    def __init__(self, *args, **kwargs):
        super(JqgridSerializer, self).__init__(*args, **kwargs)

    def serialize_queryset(self, entities, page_size):
        rows_count = len(entities)
        total_pages = floor(rows_count / page_size) + 1
        result = {
            "totalpages": total_pages,
            "totalrows": rows_count
        }
