__version__ = '0.5.6'

from model import BaseModel

from feature import Feature, JSONFeature, TextFeature, CompressedFeature, \
    PickleFeature

from extractor import Node, Graph, Aggregator, NotEnoughData

from bytestream import ByteStream, ByteStreamFeature

from data import \
    IdProvider, UuidProvider, UserSpecifiedIdProvider, StaticIdProvider, \
    KeyBuilder, StringDelimitedKeyBuilder, Database, FileSystemDatabase, \
    InMemoryDatabase

from datawriter import DataWriter

from database_iterator import DatabaseIterator

from encoder import IdentityEncoder

from decoder import Decoder

from lmdbstore import LmdbDatabase

from persistence import PersistenceSettings

try:
    from nmpy import StreamingNumpyDecoder, NumpyMetaData, NumpyFeature
except ImportError:
    pass
