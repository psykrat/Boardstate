# MTG Board State Manager

The MTG Board State Manager is a Python application developed using the `tkinter` library to manage and visualize the board state for the Magic: The Gathering card game. In games of MTG, especially with multiple players in Commander, it can become challenging to track every player's board state, remember creature stats, and discern power levels, especially from a distance. This application addresses this challenge by providing a clear, organized, and readable display of the entire board state on a large screen. Now, players can focus more on their strategies and less on trying to remember board details.

## Features

- **Canvas Splitting**: The canvas is split into four quadrants to organize the creatures.
- **Adding Creatures**: Users can add creatures by clicking on the "+" buttons located at each corner of the screen.
- **Dragging Creatures**: Creatures can be dragged and moved to a different position on the board.
- **Context Menu**: Right-clicking on a creature displays a context menu, allowing users to:
  - Modify the creature's value.
  - Modify the creature's description.
  - Delete the creature from the board.
  
## Benefits

- **Clarity**: Provides a clear visual representation of the board state, reducing confusion.
- **Accessibility**: Ensures all players can easily see creature stats, even from afar.
- **Efficiency**: Reduces the time spent asking about or trying to remember specific creature details.
- **Engagement**: Allows players to focus more on gameplay and strategy, enhancing the gaming experience.

## Usage

1. Run the code in your Python environment.
2. A window titled "MTG Board State" will appear.
3. Use the "+" buttons in the corners to add creatures.
4. Enter the creature's value (in the format `x/x`) and description when prompted.
5. Drag and drop creatures to move them.
6. Right-click on a creature to access the context menu for additional actions.

## Requirements

- Python 3.x
- `tkinter` library (standard with most Python installations)

## Code Structure

- **CreatureDialog**: A dialog class to input creature details.
- **MTGBoardState**: The main class handling the GUI and its functionalities.
  - `setup_window()`: Sets up the main window properties.
  - `setup_canvas()`: Sets up the canvas and divides it into quadrants.
  - `setup_buttons()`: Places "+" buttons on the screen for adding creatures.
  - `add_creature()`: Adds a creature to the specified quadrant.
  - `validate_input()`: Validates the creature's value input.
  - `display_creature()`: Displays the creature's value and description on the canvas.
  - `show_context_menu()`: Shows the context menu for a creature.
  - Dragging functionalities: `start_drag()`, `dragging()`, and `end_drag()`.

---

Made with ❤️ for MTG enthusiasts looking for a clearer, more efficient gameplay experience.
