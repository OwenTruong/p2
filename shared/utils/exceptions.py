class UnexpectedException(Exception):
  """Raised when an excpetion happens due to some bug or unexpected variable on the application's side."""
  pass

class DatabaseConnectionException(Exception):
  """Raised when the application cannot reach the PostgreSQL Database Instance."""
  pass

class NoFetchedResultException(Exception):
  """Raised when a fetchone query returns nothing."""

class UniqueRowException(Exception):
  """Raised when a row insertion fails due to unique constraint."""

class ActiveReservationException(Exception):
  """Raised when attempting to delete a listing that has an active reservation going on."""

class UserDoesNotOwnException(Exception):
  """Raised when a user tries to access a record/row they do not own."""