# LLMCheckmate

A chess engine that pits Large Language Models (LLMs) against each other in chess games. This project allows GPT and Gemini models to play chess by providing them with board positions, legal moves, and move history, then extracting their moves from natural language responses.

## Features

- 🤖 **Multi-Model Support**: Play games between GPT and Gemini models
- 🎯 **Move History Context**: Models receive full game history for better decision-making
- 📊 **Game Logging**: Automatic JSON logging of all game moves and states
- 🖼️ **Visualization**: Generates board images and animated GIFs of games
- ♟️ **Chess Engine**: Uses `python-chess` for move validation and game state management
- 🔄 **Retry Logic**: Automatic retry mechanism for illegal moves

## Project Structure

```
LLMCheckmate/
├── main.py                 # Main game loop
├── main_test.py           # Test script
├── requirements.txt       # Python dependencies
├── src/
│   ├── engine/           # Chess engine wrapper
│   │   ├── game_state.py # Game state management
│   │   └── __init__.py
│   ├── models/           # LLM integration
│   │   ├── gpt.py        # OpenAI GPT integration
│   │   ├── gemini.py     # Google Gemini integration
│   │   ├── prompts.py    # Prompt building
│   │   └── __init__.py
│   └── FEN_to_Image/     # Board visualization
│       ├── FEN_Imager.py # FEN to image conversion
│       └── __init__.py
└── Log/                  # Generated game logs and images
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd LLMCheckmate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Usage

### Running a Game

Simply run the main script:

```bash
python main.py
```

The script will:
1. Randomly assign GPT and Gemini to white/black
2. Play a game between the two models
3. Save board images for each move
4. Generate a JSON log of the game
5. Create an animated GIF of the game

### Output

The game generates several outputs in the `Log/` directory:

- **Board Images**: `board_001.png`, `board_002.png`, ... (one per move)
- **Game Log**: `game_log_YYYYMMDD_HHMMSS.json` (complete game data)
- **Animated GIF**: `game_YYYYMMDD_HHMMSS.gif` (visualization of the game)

### Game Log Format

Each game log contains:
- `ply`: Move number
- `side`: "white" or "black"
- `model`: "gpt" or "gemini"
- `uci`: The move in UCI notation
- `fen_before`: Board state before the move
- `fen_after`: Board state after the move
- `legal_moves`: List of legal moves at that position
- `raw_move`: Raw response from the model
- `ok`: Whether the move was successfully applied

## How It Works

1. **Game Initialization**: Creates a new chess game using `python-chess`
2. **Move Generation**: For each turn:
   - Gets the current FEN position
   - Retrieves legal moves
   - Builds a prompt with FEN, move history, and legal moves
   - Sends prompt to the appropriate LLM (GPT or Gemini)
   - Extracts UCI move from the response
3. **Move Validation**: Validates the move and retries if illegal (up to 3 attempts)
4. **State Update**: Applies the move and updates the game state
5. **Visualization**: Saves board images and generates GIFs

## Model Configuration

### GPT Models

Default model: `gpt-5-mini-2025-08-07`

To change the model, edit `src/models/gpt.py`:
```python
def get_move_gpt(fen, side, legal_moves=None, move_history=None, model="your-model-name"):
```

### Gemini Models

Default model: `gemini-3-pro-preview`

To change the model, edit `src/models/gemini.py`:
```python
def get_move_gemini(fen, side, legal_moves=None, move_history=None, model="your-model-name"):
```

## Prompt Structure

The prompt sent to models includes:
- Current side to move (White/Black)
- Current board position (FEN notation)
- Previous moves in the game (UCI notation)
- List of legal moves
- Instructions for output format

Example prompt:
```
You are playing chess as White.
Current board position (FEN): rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1
Previous moves in this game (UCI notation):
e2e4

Task: Choose ONE legal move.
...
```

## Dependencies

- `openai`: OpenAI API client for GPT models
- `google-genai`: Google Gemini API client
- `python-chess`: Chess engine and move validation
- `python-dotenv`: Environment variable management
- `requests`: HTTP requests for FEN-to-image API
- `Pillow`: Image processing for GIF generation

## API Keys

You'll need API keys from:
- **OpenAI**: Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Google**: Get your key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Limitations

- Maximum 100 plies per game (configurable in `main.py`)
- Up to 3 retry attempts for illegal moves
- Board images require internet connection (uses chessvision.ai API)
- Rate limiting may apply depending on your API quotas

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Acknowledgments

- Uses [python-chess](https://github.com/niklasf/python-chess) for chess logic
- Board images generated via [chessvision.ai FEN2Image API](https://fen2image.chessvision.ai/)
