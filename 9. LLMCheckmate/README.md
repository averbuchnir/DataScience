# LLMCheckmate

A chess engine that pits Large Language Models (LLMs) against each other in chess games. This project allows GPT and Gemini models to play chess by providing them with board positions, legal moves, and move history, then extracting their moves from natural language responses.

## Features

- 🤖 **Multi-Model Support**: Play games between GPT and Gemini models across different tiers
- 🏆 **Tournament System**: Automatic tournaments across Fast, Medium, and High tiers
- 🎯 **Move History Context**: Models receive full game history for better decision-making
- 📊 **Comprehensive Game Logging**: Detailed JSON logging with metadata, timestamps, and move analysis
- 🖼️ **Visualization**: Generates board images and animated GIFs of games
- ♟️ **Chess Engine**: Uses `python-chess` for move validation and game state management
- 🔄 **Retry Logic**: Automatic retry mechanism for illegal moves (up to 3 attempts per move)

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

### Running a Tournament

Simply run the main script:

```bash
python main.py
```

The script will:
1. Run tournaments across all tiers (Fast, Medium, High)
2. For each tier, randomly assign GPT and Gemini to white/black
3. Play games between the two models
4. Save board images for each move
5. Generate comprehensive JSON logs of each game
6. Create animated GIFs of each game
7. Display tournament summaries with win statistics

### Output Structure

The game generates outputs organized by tier in the `Log/` directory:

```
Log/
├── Fast/
│   └── game_001/
│       ├── board_001.png
│       ├── board_002.png
│       ├── game_log_YYYYMMDD_HHMMSS.json
│       └── game_YYYYMMDD_HHMMSS.gif
├── Medium/
│   └── game_001/
│       └── ...
└── High/
    └── game_001/
        └── ...
```

Each game folder contains:
- **Board Images**: `board_001.png`, `board_002.png`, ... (one per move)
- **Game Log**: `game_log_YYYYMMDD_HHMMSS.json` (complete game data with metadata)
- **Animated GIF**: `game_YYYYMMDD_HHMMSS.gif` (visualization of the game)

### Game Log Format

Each game log is a comprehensive JSON object containing:

**Game Metadata:**
- `tier`: Tournament tier (Fast, Medium, High)
- `game_number`: Game number in the tournament
- `white_model`: Model playing white ("gpt" or "gemini")
- `black_model`: Model playing black ("gpt" or "gemini")
- `white_model_name`: Specific model name for white (e.g., "gpt-5-nano")
- `black_model_name`: Specific model name for black (e.g., "gemini-2.0-flash-lite")
- `initial_fen`: Starting board position
- `game_start_time`: ISO timestamp of game start
- `game_end_time`: ISO timestamp of game end
- `result`: Game result ("1-0", "0-1", "1/2-1/2", or "*")
- `winning_model`: Winning model or "draw"
- `total_plies`: Total number of moves played
- `game_over`: Boolean indicating if game ended
- `final_fen`: Final board position

**Move Information (in `moves` array):**
- `ply`: Move number
- `side`: "white" or "black"
- `model`: "gpt" or "gemini"
- `model_name`: Specific model name used
- `fen_before`: Board state before the move
- `fen_after`: Board state after the move
- `uci`: The move in UCI notation
- `raw_move`: Raw response from the model
- `legal`: Whether the move was successfully applied
- `status`: "OK" or "ILLEGAL MOVE"
- `timestamp`: Time of the move (HH:MM:SS.mmm format)
- `legal_moves_count`: Number of legal moves available
- `attempts`: Number of attempts made for this move

## How It Works

1. **Tournament Initialization**: Iterates through all tiers (Fast, Medium, High)
2. **Game Setup**: For each game:
   - Randomly assigns GPT and Gemini to white/black
   - Creates game folder structure
   - Initializes comprehensive game log
3. **Move Generation**: For each turn:
   - Gets the current FEN position
   - Retrieves legal moves
   - Builds a prompt with FEN, move history, and legal moves
   - Sends prompt to the appropriate LLM (GPT or Gemini) based on tier
   - Extracts UCI move from the response using pattern matching
4. **Move Validation**: Validates the move and retries if illegal (up to 3 attempts)
5. **Logging**: Records detailed move information including timestamps, attempts, and status
6. **State Update**: Applies the move and updates the game state
7. **Visualization**: After game completion, saves board images and generates GIFs
8. **Tournament Summary**: Displays win statistics across all tiers

## Model Configuration

### Tier System

The project uses a tier-based system with different models for each tier:

- **Fast Tier**: 
  - GPT: `gpt-5-nano`
  - Gemini: `gemini-2.0-flash-lite`
- **Medium Tier**: 
  - GPT: `gpt-5-mini`
  - Gemini: `gemini-3-flash-preview`
- **High Tier**: 
  - GPT: `gpt-5.2`
  - Gemini: `gemini-3-pro-preview`

### Changing Models

To modify the models used in each tier, edit `src/models/get_model_names.py`:

```python
Model_Names = {
    "Fast": {
        "gpt": "your-gpt-model",
        "gemini": "your-gemini-model"
    },
    "Medium": {
        "gpt": "your-gpt-model",
        "gemini": "your-gemini-model"
    },
    "High": {
        "gpt": "your-gpt-model",
        "gemini": "your-gemini-model"
    }
}
```

### Model Settings

Models use default API settings without custom configuration parameters (temperature, top_p, etc.) to ensure compatibility across all tiers and model versions.

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

## Configuration

### Game Settings

In `main.py`, you can configure:
- `number_of_games`: Number of games to play per tier (default: 1)
- `max_plies`: Maximum number of plies per game to avoid infinite games (default: 3)
- `max_retries`: Number of retry attempts for illegal moves (default: 3)

## Limitations

- Maximum plies per game is configurable (default: 3, can be increased in `main.py`)
- Up to 3 retry attempts for illegal moves per move
- Board images require internet connection (uses chessvision.ai API)
- Rate limiting may apply depending on your API quotas
- Models use default API settings (no custom temperature or sampling parameters)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license here]

## Acknowledgments

- Uses [python-chess](https://github.com/niklasf/python-chess) for chess logic
- Board images generated via [chessvision.ai FEN2Image API](https://fen2image.chessvision.ai/)
