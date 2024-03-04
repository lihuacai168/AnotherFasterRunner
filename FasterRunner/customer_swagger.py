from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        if hasattr(self.view, 'swagger_tag'):
            return [self.view.swagger_tag]
        return super().get_tags(operation_keys)
