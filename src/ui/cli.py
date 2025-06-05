"""CLI User Interface for LLM Fixpoints Explorer."""

class CLIUserInterface:
    """Command-line interface for interacting with users."""

    def get_story_cornerstones(self) -> dict[str, str]:
        """Get the corner stones of a story from the user and return as dictionary."""
        print("\nPlease provide the corner stones of your story:")
        cornerstones = {}

        # Title
        title = input("Title: ")
        if title:
            cornerstones["title"] = title

        # Main characters
        characters = input("Main characters (comma-separated): ")
        if characters:
            cornerstones["characters"] = characters

        # Setting
        setting = input("Setting: ")
        if setting:
            cornerstones["setting"] = setting

        # Plot points
        plot_points = input("Plot points (comma-separated): ")
        if plot_points:
            cornerstones["plot_points"] = plot_points

        # Theme
        theme = input("Theme: ")
        if theme:
            cornerstones["theme"] = theme

        return cornerstones

    def display_story(self, story: str):
        """Display a story to the user."""
        print("\nHere's your story:")
        print("-" * 40)
        print(story)
        print("-" * 40)

    def get_retell_count(self) -> int:
        """Get the number of retellings from the user."""
        while True:
            try:
                count = input("How many times should the story be retold? (default: 5): ")
                if not count:
                    return 5
                return int(count)
            except ValueError:
                print("Please enter a valid number.")