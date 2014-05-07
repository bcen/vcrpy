from serializers import compat
from vcr.request import Request

"""
Just a general note on the serialization philosophy here:
I prefer cassettes to be human-readable if possible.  Yaml serializes
bytestrings to !!binary, which isn't readable, so I would like to serialize to
strings and from strings, which yaml will encode as utf-8 automatically.
All the internal HTTP stuff expects bytestrings, so this whole serialization
process feels backwards.

Serializing: bytestring -> string (yaml persists to utf-8)
Deserializing: string (yaml converts from utf-8) -> bytestring
"""


def deserialize(cassette_string, serializer):
    data = serializer.deserialize(cassette_string)
    requests = [Request._from_dict(r['request']) for r in data]
    responses = [r['response'] for r in data]
    responses = [compat.convert_to_bytes(r['response']) for r in data]
    return requests, responses


def serialize(cassette_dict, serializer):
    data = ([{
        'request': request._to_dict(),
        'response': compat.convert_to_unicode(response),
    } for request, response in zip(
        cassette_dict['requests'],
        cassette_dict['responses'],
    )])
    return serializer.serialize(data)
