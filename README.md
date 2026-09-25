# Hunt the Wumpus – Web Edition

A web adaptation of the classic game *Hunt the Wumpus* (as it existed on the TI-99/4A), built with **Python**, **Flask** and **Jinja2**. This was developed as a course project for *Technologie Internet 2*.

## The Game

You are lost in a maze of interconnected caves. Somewhere in it lives the Wumpus, a voracious creature. Your only weapon is a bow with a single magical arrow, which can follow the corridors to reach the next cave.

**Goal:** find the Wumpus and kill it with your arrow. If you miss, the arrow is lost and so is the game.

### Dangers and clues

| Element | What happens | Clue |
| --- | --- | --- |
| **Wumpus** | You are devoured if you enter its cave. | Its remains are visible up to two caves away (red discs in the original game). Corridors do not count in the distance. |
| **Slime pits** | You fall in and die. There are 2 on the board. | The adjacent caves are covered with moss (shown in green in the original game). |
| **Giant bats** | The second time you enter a bat's cave, it carries you to a random cave, then picks a new cave for itself. Bats never drop you in the Wumpus's lair or in a slime pit. | – |

You only know the cave you are currently in, so you have to explore the maze cave by cave. Once you have located the Wumpus, move to an adjacent cave, shoot, and choose the direction of the arrow.

### Difficulty levels

The board is 8×6 caves with 2 slime pits. The number of corridors is drawn at random within limits that depend on the level, and every cave is always reachable.

| Level | Bats | Caves (average) | Corridors |
| --- | --- | --- | --- |
| Easy | 1 | 32 | 10 (between 8 and 14) |
| Medium | 2 | 24 | 18 |
| Hard | 2 | 16 | 26 |

### Optional modes

- **Blindfold:** only the cave you are standing in is displayed.
- **Express:** corridors are crossed automatically up to the destination cave.

## Features

- Playable Hunt the Wumpus in the browser
- Three difficulty levels with a randomly generated maze
- Account creation form
- Player statistics (wins, killed by the Wumpus, fallen in a slime pit)
- Leaderboard stored in a database
- Fully customable icon for your account with a selection of colors

## Tech Stack

- **Python** with the **Flask** web framework
- **Jinja2** templates, using a base template for the shared page layout
- **PostgreSQL** (via `psycopg`) for accounts, statistics and ranking
- **HTML** and **CSS**: the game board is built with a table and `div`s using CSS classes and background images, with no inline `style` attributes
- **JavaScript**, limited to animations and sound. It never makes direct server calls (no `fetch` or `XMLHttpRequest`): page requests go through links and forms only.

## Getting Started

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the dependencies:

   ```bash
   pip install flask psycopg
   ```

3. Configure the database connection (host, database name, user, password) in the application settings, then create the required tables.

4. Run the application:

   ```bash
   flask run
   ```

5. Open `http://127.0.0.1:5000` in your browser.

The project is also designed to run on a Unix web server, which is case-sensitive, so file names and paths must match exactly.

## Author

Nolan Mertens, Antoine V

## Credits

Based on the original *Hunt the Wumpus*.
Project assignment by *D.Moreaux*.