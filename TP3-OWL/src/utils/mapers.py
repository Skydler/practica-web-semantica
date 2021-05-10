from models.model import Person, Video


def to_video(url):
    if url:
        return Video(
            url=url,
            schema_type='Video',
            name=None,
            description=None,
            thumbnail_url=None)


def to_person(person_names):
    return [
        Person(name=name, url=None, image=None, schema_type='Person')
        for name in person_names
    ]
