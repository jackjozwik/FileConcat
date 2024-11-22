# Claude File Concatenator

A streamlined Python utility that helps you work more effectively with Claude AI by managing your source code context. It concatenates your project files with clear separators, making it easy to feed relevant code to Claude while respecting your project's `.gitignore` rules.

## Key Features

- Concatenate files with clear separators that Claude understands
- Respect your project's `.gitignore` patterns
- Split modified files back to their original locations
- Filter specific file types to maintain focused context
- Process files quickly with minimal overhead

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install pathspec
```

## Usage

### Basic Operations

Concatenate your files:
```bash
python script.py --mode concat --input ./my-project --output combined.txt
```

Split files back into your project:
```bash
python script.py --mode split --input claude-modified.txt --output ./my-project
```

### Advanced Usage

Target specific file types:
```bash
python script.py --mode concat --input ./src --output frontend.txt --extensions .ts .tsx .js .jsx
```

Focus on specific features:
```bash
# Single feature
python script.py --mode concat --input ./src/features/auth --output auth.txt --extensions .ts .tsx

# Backend code
python script.py --mode concat --input ./src/backend --output backend.txt --extensions .rs .go
```

## Best Practices

### Managing Context

Keep your code context focused and relevant. Instead of feeding entire projects to Claude, target specific directories or features you need help with. This not only reduces token usage but also helps Claude provide more precise assistance.

### Token Efficiency

Avoid including build artifacts and dependencies in your concatenated files. The tool respects your `.gitignore` by default, but you can further optimize by:
- Targeting specific feature directories
- Filtering for relevant file extensions
- Excluding test and configuration files when unnecessary

### Working With Claude

When using your concatenated files with Claude:
1. Include clear prompts about what you want to analyze
2. Specify if you need explanations, modifications, or both
3. Use the split functionality to easily apply Claude's changes back to your project

## Technical Details

### File Handling
The tool processes files with UTF-8 encoding and adds clear file separators. It maintains your project's directory structure when splitting files and automatically skips binary files and ignored directories.

### Default Configuration

**Supported Extensions:**
- `.py` (Python)
- `.js`, `.jsx` (JavaScript)
- `.ts`, `.tsx` (TypeScript)
- `.css`, `.scss` (Stylesheets)
- `.html` (HTML)

**Default Ignores:**
When no `.gitignore` is present, the tool excludes common development artifacts and directories like:
- `.git/`
- `__pycache__/`
- `node_modules/`
- `.env`
- `venv/`
- IDE directories

## Contributing

Issues and enhancement requests are welcome. Feel free to contribute to make this tool even better.
