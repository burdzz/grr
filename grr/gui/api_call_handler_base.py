#!/usr/bin/env python
"""The base class for ApiCallHandlers."""

from grr.lib import registry


class Error(Exception):
  pass


class ResourceNotFoundError(Error):
  """Raised when a resource could not be found."""


class ApiBinaryStream(object):
  """Object to be returned from streaming API methods."""

  def __init__(self, filename, content_generator=None, content_length=None):
    """ApiBinaryStream constructor.

    Args:
      filename: A file name to be used by the browser when user downloads the
          file.
      content_generator: A generator that yields byte chunks (of any size) to
          be streamed to the user.
      content_length: The length of the stream, if known upfront.

    Raises:
      ValueError: if content_generator is None.
    """
    self.filename = filename
    self.content_length = content_length

    if content_generator is None:
      raise ValueError("content_generator can't be None")
    self.content_generator = content_generator

  def GenerateContent(self):
    """Generates content of the stream.

    Yields:
      Byte chunks (of any size) to be streamed to the user.
    """

    for chunk in self.content_generator:
      yield chunk


class ApiCallHandler(object):
  """Baseclass for restful API renderers."""

  __metaclass__ = registry.MetaclassRegistry

  # RDFValue type used to handle API renderer arguments. This has to be
  # a class object.
  args_type = None

  # RDFValue type returned by the handler. This is only used by new handlers
  # that implement Handle() method. Legacy handlers don't have Handle()
  # implemented and return arbitrary data structures from Render() method.
  result_type = None

  # This is a maximum time in seconds the renderer is allowed to run. Renderers
  # exceeding this time are killed softly (i.e. the time is not a guaranteed
  # maximum, but will be used as a guide).
  max_execution_time = 60

  # If True, when converting response to JSON, strip type information from root
  # fields of the resulting proto.
  strip_json_root_fields_types = True

  # NOTE: Render() is deprecated in favor of Handle(). Main difference of
  # Render() and Handle() is that Handle() returns an RDFValue, while Render()
  # return arbitrary data structures.
  def Render(self, args, token=None):
    """Renders response as a plain python object."""
    raise NotImplementedError()

  def Handle(self, args, token=None):
    """Handles request and returns an RDFValue of result_type."""
    raise NotImplementedError()
