import sys

# Add the current directory to the path, so we can import the compiler.
sys.path.insert(0, ".")

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


class CustomHook(BuildHookInterface):
    """A custom build hook for hydrogram."""

    def initialize(self, version, build_data):
        """Initialize the hook."""
        if self.target_name not in ["wheel", "install"]:
            return

        from compiler.api.compiler import start as compile_api
        from compiler.errors.compiler import start as compile_errors

        compile_api()
        compile_errors()
