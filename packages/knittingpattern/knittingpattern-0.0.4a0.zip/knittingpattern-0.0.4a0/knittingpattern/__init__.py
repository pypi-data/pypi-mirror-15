from .KnittingContext import KnittingContext

__version__ = '0.0.4a'

knitting_context = KnittingContext()

load_from_object = knitting_context.load.object
load_from_string = knitting_context.load.string
load_from_file = knitting_context.load.file
load_from_path = knitting_context.load.path
load_from_url = knitting_context.load.url
load_from_relative_file = knitting_context.load.relative_file

__all__ = [
        "KnittingContext", "knitting_context", "load_from_object",
        "load_from_string", "load_from_file", "load_from_path",
        "load_from_url", "load_from_relative_file"
    ]
