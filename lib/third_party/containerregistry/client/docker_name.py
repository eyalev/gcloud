"""This package defines Tag a way of representing an image uri."""


class BadNameException(Exception):
  """Exceptions when a bad docker name is supplied."""


_REPOSITORY_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789_-./'
_TAG_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789_-.ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# These have the form: sha256:<hex string>
_DIGEST_CHARS = 'sh:0123456789abcdef'


def _check_element(name, element, characters, min_len, max_len):
  """Checks a given named element matches character and length restrictions.

  Args:
    name: str, the name of the element being validated
    element: str, the actual element being checked
    characters: str, acceptable characters for this element, or None
    min_len: int, minimum element length, or None
    max_len: int, maximum element length, or None

  Raises:
    BadNameException: one of the restrictions was not met.
  """
  length = len(element)
  if min_len and length < min_len:
    raise BadNameException('Invalid %s: %s, must be at least %s characters'
                           % (name, element, min_len))

  if max_len and length > max_len:
    raise BadNameException('Invalid %s: %s, must be at most %s characters'
                           % (name, element, max_len))

  if element.strip(characters):
    raise BadNameException('Invalid %s: %s, acceptable characters include: %s'
                           % (name, element, characters))


def _check_repository(repository):
  _check_element('repository', repository, _REPOSITORY_CHARS, 4, 255)


def _check_tag(tag):
  _check_element('tag', tag, _TAG_CHARS, 1, 127)


def _check_digest(digest):
  _check_element('digest', digest, _DIGEST_CHARS, 7 + 64, 7 + 64)


class Repository(object):
  """Stores a docker repository name in a structured form."""

  def __init__(self, name):
    if not name:
      raise BadNameException('A Docker image name must be specified')

    parts = name.split('/', 1)
    if len(parts) != 2:
      raise self._validation_exception(name)
    self._registry = parts[0]

    self._repository = parts[1]
    _check_repository(self._repository)

  def _validation_exception(self, name):
    return BadNameException('Docker image name must have the form: '
                            'registry/repository, saw: %s' % name)

  @property
  def registry(self):
    return self._registry

  @property
  def repository(self):
    return self._repository

  def __str__(self):
    return '{registry}/{repository}'.format(
        registry=self.registry, repository=self.repository)


class Tag(Repository):
  """Stores a docker repository tag in a structured form."""

  def __init__(self, name):
    parts = name.split(':')
    if len(parts) != 2:
      raise self._validation_exception(name)

    self._tag = parts[1]
    _check_tag(self._tag)
    super(Tag, self).__init__(parts[0])

  def _validation_exception(self, name):
    return BadNameException('Docker image name must be fully qualified (e.g.'
                            'registry/repository:tag) saw: %s' % name)

  @property
  def tag(self):
    return self._tag

  def __str__(self):
    return '{base}:{tag}'.format(base=super(Tag, self).__str__(), tag=self.tag)


class Digest(Repository):
  """Stores a docker repository digest in a structured form."""

  def __init__(self, name):
    parts = name.split('@')
    if len(parts) != 2:
      raise self._validation_exception(name)

    self._digest = parts[1]
    _check_digest(self._digest)
    super(Digest, self).__init__(parts[0])

  def _validation_exception(self, name):
    return BadNameException('Docker image name must be fully qualified (e.g.'
                            'registry/repository@digest) saw: %s' % name)

  @property
  def digest(self):
    return self._digest

  def __str__(self):
    return '{base}@{digest}'.format(base=super(Digest, self).__str__(),
                                    digest=self.digest)
