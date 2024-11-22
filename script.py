import os
from pathlib import Path
import argparse
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

def load_gitignore(directory: str) -> PathSpec:
    """
    Load .gitignore patterns from the directory
    """
    gitignore_path = Path(directory) / '.gitignore'
    patterns = []
    
    if gitignore_path.exists():
        try:
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                patterns = [line.strip() for line in f if line.strip() 
                          and not line.startswith('#')]
        except Exception as e:
            print(f"Warning: Error reading .gitignore: {str(e)}")
    
    # Add default patterns if no .gitignore exists
    if not patterns:
        patterns = [
            '.git/', '__pycache__/', 'node_modules/',
            '*.pyc', '*.pyo', '*.pyd', '.Python',
            '.env', '.venv/', 'env/', 'venv/',
            '.idea/', '.vscode/'
        ]
    
    return PathSpec.from_lines(GitWildMatchPattern, patterns)

def should_process_file(path: Path, base_dir: Path, gitignore_spec: PathSpec) -> bool:
    """
    Check if file should be processed based on .gitignore rules
    """
    # Get relative path for gitignore matching
    relative_path = str(path.relative_to(base_dir))
    
    # Skip hidden files and gitignore matches
    return not (path.name.startswith('.') or gitignore_spec.match_file(relative_path))

def concatenate_directory(
    directory: str,
    output_file: str = None,
    allowed_extensions: list = None
) -> str:
    """
    Concatenate all files in a directory and its subdirectories with file separators.
    Respects .gitignore rules.
    
    Args:
        directory: Source directory path
        output_file: Optional output file path
        allowed_extensions: List of file extensions to include (e.g. ['.py', '.js'])
    
    Returns:
        Concatenated content as string
    """
    if allowed_extensions is None:
        allowed_extensions = ['.py', '.js', '.ts', '.jsx', '.tsx', '.css', '.scss', '.html']
        
    concatenated = []
    directory_path = Path(directory)
    gitignore_spec = load_gitignore(directory)
    
    # Walk through directory
    for root, _, files in os.walk(directory_path):
        root_path = Path(root)
        
        # Skip if the directory itself is ignored
        if not should_process_file(root_path, directory_path, gitignore_spec):
            continue
            
        for file in sorted(files):
            file_path = root_path / file
            
            # Apply gitignore rules and extension filter
            if not should_process_file(file_path, directory_path, gitignore_spec):
                continue
                
            # Skip files with unwanted extensions
            if allowed_extensions and file_path.suffix not in allowed_extensions:
                continue
                
            # Get relative path from base directory
            relative_path = file_path.relative_to(directory_path)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Add file separator and content
                concatenated.extend([
                    f"\n// File: {relative_path}\n",
                    content,
                    "\n"
                ])
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                
    final_content = "".join(concatenated)
    
    # Write to output file if specified
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(final_content)
            print(f"Output written to {output_file}")
        except Exception as e:
            print(f"Error writing output file: {str(e)}")
            
    return final_content

def split_concatenated_file(input_file: str, output_dir: str):
    """
    Split a concatenated file back into individual files
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading input file: {str(e)}")
        return
        
    # Split content by file separator
    files = content.split("\n// File: ")
    
    # Skip empty first element
    if files[0].strip() == "":
        files = files[1:]
        
    for file_content in files:
        # Split into filename and content
        try:
            file_path, content = file_content.split("\n", 1)
        except ValueError:
            continue
            
        # Create full output path
        output_path = Path(output_dir) / file_path
        
        # Create directories if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content.rstrip())
            print(f"Written: {output_path}")
        except Exception as e:
            print(f"Error writing {output_path}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Concatenate or split directory files for Claude')
    parser.add_argument('--mode', choices=['concat', 'split'], required=True,
                      help='Operation mode: concat or split')
    parser.add_argument('--input', required=True,
                      help='Input directory for concat mode, input file for split mode')
    parser.add_argument('--output', required=True,
                      help='Output file for concat mode, output directory for split mode')
    parser.add_argument('--extensions', nargs='*', default=None,
                      help='Allowed file extensions')
    
    args = parser.parse_args()
    
    if args.mode == 'concat':
        concatenate_directory(args.input, args.output, args.extensions)
    else:
        split_concatenated_file(args.input, args.output)

if __name__ == "__main__":
    main()