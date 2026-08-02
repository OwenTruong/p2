class UnexpectedException(Exception):
  """Raised when an excpetion happens due to some bug or unexpected variable on the application's side."""
  pass

class DatabaseConnectionException(Exception):
  """Raised when the application cannot reach the PostgreSQL Database Instance."""
  pass

class NoFetchedResultException(Exception):
  """Raised when a fetchone query returns nothing."""