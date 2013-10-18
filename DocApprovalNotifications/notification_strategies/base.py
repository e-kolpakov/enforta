from django.db.models.loading import get_model


class BaseStrategy(object):
    def _get_entity_model(self, entity):
        app_label, model_name = entity.split(".")
        return get_model(app_label, model_name, seed_cache=False)

    def _get_entity(self, entity, entity_id):
        model = self._get_entity_model(entity)
        return model.objects.get(pk=entity_id)

    def _get_event_entity(self, event):
        return self._get_entity(event.entity, event.entity_id)

    def execute(self, event):
        raise NotImplementedError("Execute called on strategy class")