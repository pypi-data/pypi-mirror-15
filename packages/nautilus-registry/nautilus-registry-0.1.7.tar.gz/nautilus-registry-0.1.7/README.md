# nautilus-registry
A module to support an "impure" nautilus architecture, taking advantage of a service registry

## Installing
`nautilus_registry` can be installed from pip:

```bash
pip install nautilus_registry
```


## Connecting a service to consul
Currently, `nautilus_registry` only supports consul and does so through a
service mixin:

```python
import nautilus
from nautilus_registry import RegisterMixin

class MyService(RegisterMixin, nautilus.Service):
    # ...

```


This mixin registers the service with consul when the service starts and
handles the removal of the service from consul aswell.


## Referring to the registry in an API
Schemas that are executed from services with this mixin can access various utility functions through the context:

```python
class MyObjectType(graphene.ObjectType):

    field = Field(...)

    @graphene.with_content
    @graphene.resolve_only_args
    def resolve_field(self, context=None):
        # query the api for some data
        data = context.service.query_api(...)
```
