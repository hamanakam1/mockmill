"""Offline CRM file-mapping foundations; no API clients or live write authority."""
from .offline import ADAPTERS, build_adapter, export_adapter
__all__=['ADAPTERS','build_adapter','export_adapter']
