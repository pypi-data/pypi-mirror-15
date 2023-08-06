from channels.generic import websockets
from channels_api.settings import api_settings

from rest_framework.exceptions import ValidationError

from .mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    ListModelMixin, DeleteModelMixin, SerializerMixin


class ModelConsumerBase(SerializerMixin, websockets.JsonWebsocketConsumer):
    """consumer class based on an individual model."""

    available_methods = ('create', 'retrieve', 'list', 'update', 'delete')
    model = None
    queryset = None
    lookup_field = 'pk'

    @classmethod
    def channel_names(cls):
        """Used by router class to determine what channels to listen to."""
        return [cls.get_channel_name(m) for m in cls.available_methods if m in dir(cls)]

    @classmethod
    def get_channel_name(cls, method):
        """Helper method to format the name of the channel based on method."""
        model_name = cls.model.__name__
        return "{}.{}".format(model_name, method).lower()

    def dispatch(self, message, **kwargs):
        try:
            self.send(self.format_response(data=super().dispatch(message, **kwargs), message=message))
        except ValidationError as ex:
            self.send(self.format_response(error=ex, message=message))

    def filter_queryset(self, queryset):
        """Override this method to handle filtering."""
        return queryset

    def format_response(self, **kwargs):
        return api_settings.DEFAULT_FORMATTER_CLASS(**kwargs)()

    def get_params(self):
        return api_settings.DEFAULT_PARSER_CLASS(self.message)()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(**{self.lookup_field: self.get_params()["id"]})

    def get_queryset(self):
        assert self.queryset is not None, (
            "'%s' should either include a `queryset` attribute, "
            "or override the `get_queryset()` method."
            % self.__class__.__name__
        )
        return self.queryset.all()

    @property
    def method_mapping(self):
        """Used by get_handler method to figure out what method to run."""
        mapping = {}
        for method in self.available_methods:
            m = getattr(self, method)
            if m:
                mapping[self.get_channel_name(method)] = m.__name__
        return mapping


class ReadOnlyModelConsumer(RetrieveModelMixin, ListModelMixin, ModelConsumerBase):
    pass


class ModelConsumer(CreateModelMixin, RetrieveModelMixin,
                    ListModelMixin, UpdateModelMixin, DeleteModelMixin,
                    ModelConsumerBase):
    pass
