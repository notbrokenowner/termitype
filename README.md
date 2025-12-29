# Termitype

Terminal typing speed test application for the command line.

## Description

Termitype is a typing speed test application that runs directly in your terminal. It displays text to type, tracks your typing speed (WPM - words per minute), accuracy, and error count in real-time.

## Features

- 🎯 Real-time typing speed test
- 📊 WPM (words per minute) calculation
- ✅ Accuracy tracking
- 🎨 Color-coded correct/incorrect characters
- 🌍 Multi-language support via JSON files
- ⏱️ Timer and statistics
- 📁 Easy language management through JSON files

## Installation

1. Clone the repository or download the files
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic usage

```bash
python typing_test.py
```

This will use the default language (english) with 25 words.

### With parameters

```bash
# Test with a specific language
python typing_test.py -l english

# Test with 50 words
python typing_test.py -w 50

# Combination of parameters
python typing_test.py -l english -w 30

# List all available languages
python typing_test.py --list-languages
```

### Command line parameters

- `-l, --language` - Language name (e.g., `english`). Default: `english`
- `-w, --words` - Number of words in the test. Default: `25`
- `--list-languages` - List all available languages and exit

## Language Files

Languages are stored as JSON files in the `languages/` directory. Each language file should have the following structure:

```json
{
  "name": "english",
  "words": [
    "the",
    "be",
    "of",
    ...
  ]
}
```

### Language file fields

- `name` - Language name (used with `-l` parameter)
- `words` - Array of words for the typing test

### Adding a new language

1. Create a new JSON file in the `languages/` directory (e.g., `languages/russian.json`)
2. Add the language data following the structure above
3. Run `python typing_test.py --list-languages` to verify it's loaded
4. Use it with `python typing_test.py -l russian`

## Controls

- **Start typing** - Test begins automatically on first keystroke
- **Backspace** - Delete last character
- **Enter** - Finish test early
- **Ctrl+C** - Interrupt test

## Example Output

```
=== Termitype - Typing Speed Test ===
Press any key to start...

the be of and a to in he have it that for they I with as not on she at

WPM: 45.2 | Accuracy: 98.5% | Time: 12.3s
```

## Requirements

- Python 3.6+
- Windows, Linux, or macOS
- `colorama` library (installed automatically)

## License

GNU General Public License v3.0
