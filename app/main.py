"""Render expects `app.main:app`, so re-export the root FastAPI app instance."""

from main import app  # noqa: F401

__all__ = ["app"]
