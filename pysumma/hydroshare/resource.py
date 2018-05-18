

class ResourceMetadata (object):
    def __init__(self, system_meta, science_meta):

        self.__dict__.update(science_meta)
        self.__dict__.update(system_meta)

    @property
    def url(self):
        return self.resource_url

    @property
    def abstract(self):
        return self.description

    @property
    def keywords(self):
        return [s['value'] for s in self.subjects]
