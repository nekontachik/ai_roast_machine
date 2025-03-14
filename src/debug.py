"""Debug utilities for development and troubleshooting."""
import sys
import traceback
import time
import logging
from functools import wraps
from typing import Any, Callable, Dict, Optional, TypeVar, cast

logger = logging.getLogger(__name__)

F = TypeVar('F', bound=Callable[..., Any])

def debug_trace(func: F) -> F:
    """Decorator to trace function calls with parameters and return values.
    
    Args:
        func: Function to trace
        
    Returns:
        Wrapped function with tracing
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name = func.__name__
        logger.debug(
            f"Entering {func_name}",
            extra={
                'args': args,
                'kwargs': kwargs,
                'caller': traceback.extract_stack()[-2].name
            }
        )
        try:
            result = func(*args, **kwargs)
            logger.debug(
                f"Exiting {func_name}",
                extra={'result': result}
            )
            return result
        except Exception as e:
            logger.error(
                f"Error in {func_name}",
                extra={
                    'error': str(e),
                    'traceback': traceback.format_exc()
                }
            )
            raise
    return cast(F, wrapper)

def measure_time(func: F) -> F:
    """Decorator to measure function execution time.
    
    Args:
        func: Function to measure
        
    Returns:
        Wrapped function with timing
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end = time.perf_counter()
            logger.debug(
                f"{func.__name__} execution time",
                extra={'duration_seconds': end - start}
            )
    return cast(F, wrapper)

def memory_usage(func: F) -> F:
    """Decorator to track memory usage of a function.
    
    Args:
        func: Function to track
        
    Returns:
        Wrapped function with memory tracking
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        import psutil
        process = psutil.Process()
        
        mem_before = process.memory_info().rss
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            mem_after = process.memory_info().rss
            mem_diff = mem_after - mem_before
            logger.debug(
                f"{func.__name__} memory usage",
                extra={
                    'memory_before_bytes': mem_before,
                    'memory_after_bytes': mem_after,
                    'memory_diff_bytes': mem_diff
                }
            )
    return cast(F, wrapper)

def set_trace() -> None:
    """Drop into pdb debugger."""
    import pdb
    pdb.set_trace() 