from ._identity import identity_str, identity_bytes, identity_mmap_str, identity_mmap_bytes
try:
    from ._lxml import html, xml
except ImportError:
    pass
from . import pickle, compressed_pickle
