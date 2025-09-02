import typer
from typer.testing import CliRunner


def test_auto_envvar_prefix_with_and_without_underscore():
    """Test that auto_envvar_prefix supports both underscore and non-underscore formats."""
    app = typer.Typer()

    @app.command(context_settings={"auto_envvar_prefix": "MYAPP"})
    def main(
        name: str = typer.Option("World", help="Name to greet"),
        debug: bool = typer.Option(False, help="Enable debug mode")
    ):
        """Test command for auto envvar prefix behavior."""
        print(f"Hello {name}! Debug: {debug}")

    runner = CliRunner()

    # Test help shows both formats
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "MYAPP_NAME, MYAPPNAME" in result.output
    # The debug option might be on a different line due to formatting
    assert "MYAPP_DEBUG" in result.output
    assert "MYAPPDEBUG" in result.output

    # Test underscore version works
    result = runner.invoke(app, [], env={"MYAPP_NAME": "Alice", "MYAPP_DEBUG": "true"})
    assert result.exit_code == 0
    assert "Hello Alice! Debug: True" in result.output

    # Test non-underscore version works
    result = runner.invoke(app, [], env={"MYAPPNAME": "Bob", "MYAPPDEBUG": "true"})
    assert result.exit_code == 0
    assert "Hello Bob! Debug: True" in result.output

    # Test underscore version takes precedence
    result = runner.invoke(app, [], env={
        "MYAPP_NAME": "Alice", "MYAPPNAME": "Bob",
        "MYAPP_DEBUG": "true", "MYAPPDEBUG": "false"
    })
    assert result.exit_code == 0
    assert "Hello Alice! Debug: True" in result.output

    # Test only non-underscore set
    result = runner.invoke(app, [], env={"MYAPPNAME": "Charlie"})
    assert result.exit_code == 0
    assert "Hello Charlie! Debug: False" in result.output