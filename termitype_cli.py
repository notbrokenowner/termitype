import sys
import time
import random
import os
import json
from typing import List, Tuple, Dict, Optional
from pathlib import Path

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = ''
        RED = ''
        YELLOW = ''
        CYAN = ''
        WHITE = ''
    class Style:
        RESET_ALL = ''
        BRIGHT = ''

class Language:
    def __init__(self, name: str, words: List[str]):
        self.name = name
        self.words = words


class LanguageLoader:
    def __init__(self, languages_dir: str = "languages"):
        self.languages_dir = Path(languages_dir)
        self.languages: Dict[str, Language] = {}
        self._load_languages()
    
    def _load_languages(self):
        if not self.languages_dir.exists():
            print(f"{Fore.YELLOW}Warning: Languages directory '{self.languages_dir}' not found!")
            return
        
        for json_file in self.languages_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                language = Language(
                    name=data.get("name", json_file.stem),
                    words=data.get("words", [])
                )
                
                self.languages[language.name] = language
            except Exception as e:
                print(f"{Fore.RED}Error loading language from {json_file}: {e}")
    
    def get_language(self, name: str) -> Optional[Language]:
        return self.languages.get(name)
    
    def list_languages(self) -> List[str]:
        return list(self.languages.keys())
    
    def get_default_language(self) -> Optional[Language]:
        return self.languages.get("english")


class TypingTest:
    def __init__(self, language: Language, words_count: int = 25):
        self.language = language
        self.words_count = words_count
        self.text = self._generate_text()
        self.user_input = []
        self.start_time = None
        self.end_time = None
        
    def _generate_text(self) -> List[str]:
        return random.sample(self.language.words, min(self.words_count, len(self.language.words)))
    
    def _get_char_status(self, char_idx: int) -> Tuple[str, bool]:
        if char_idx >= len(self.user_input):
            return ' ', False
        
        text_str = ' '.join(self.text)
        if char_idx >= len(text_str):
            return ' ', False
            
        user_char = self.user_input[char_idx]
        correct_char = text_str[char_idx]
        
        return user_char, user_char == correct_char
    
    def _display_text(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        text_str = ' '.join(self.text)
        display_lines = []
        
        line_length = 80
        for i in range(0, len(text_str), line_length):
            line = text_str[i:i + line_length]
            display_lines.append((i, line))
        
        for start_idx, line in display_lines:
            for i, char in enumerate(line):
                char_idx = start_idx + i
                user_char, is_correct = self._get_char_status(char_idx)
                
                if char_idx < len(self.user_input):
                    if is_correct:
                        print(Fore.GREEN + char, end='')
                    else:
                        print(Fore.RED + char, end='')
                elif char_idx == len(self.user_input):
                    print(Fore.CYAN + Style.BRIGHT + char, end='')
                else:
                    print(Fore.WHITE + char, end='')
            print()
        
        print()
        
        if self.start_time:
            elapsed = time.time() - self.start_time
            if elapsed > 0:
                typed_chars = len(self.user_input)
                correct_chars = sum(1 for i in range(min(typed_chars, len(text_str))) 
                                  if i < len(self.user_input) and 
                                  self.user_input[i] == text_str[i])
                accuracy = (correct_chars / typed_chars * 100) if typed_chars > 0 else 0
                wpm = (correct_chars / 5) / (elapsed / 60) if elapsed > 0 else 0
                
                print(f"{Fore.YELLOW}WPM: {wpm:.1f} | {Fore.CYAN}Accuracy: {accuracy:.1f}% | "
                      f"{Fore.WHITE}Time: {elapsed:.1f}s")
    
    def _get_input_char(self) -> str:
        if os.name == 'nt':
            import msvcrt
            while True:
                if msvcrt.kbhit():
                    char = msvcrt.getch()
                    if char == b'\r':
                        return '\n'
                    elif char == b'\x08':
                        return '\b'
                    elif char == b'\xe0':
                        msvcrt.getch()
                        continue
                    else:
                        try:
                            try:
                                return char.decode('utf-8')
                            except UnicodeDecodeError:
                                import locale
                                encoding = locale.getpreferredencoding()
                                return char.decode(encoding, errors='ignore')
                        except:
                            return ''
        else:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                char = sys.stdin.read(1)
                return char
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def run(self):
        print(f"{Fore.CYAN}{Style.BRIGHT}=== Termitype - Typing Speed Test ==={Style.RESET_ALL}")
        print(f"{Fore.WHITE}Press any key to start...")
        print()
        
        self._get_input_char()
        self.start_time = time.time()
        
        text_str = ' '.join(self.text)
        
        while True:
            self._display_text()
            
            if len(self.user_input) >= len(text_str):
                self.end_time = time.time()
                break
            
            char = self._get_input_char()
            
            if char == '\n' or char == '\r':
                self.end_time = time.time()
                break
            elif char == '\b' or (char and ord(char) == 127):
                if self.user_input:
                    self.user_input.pop()
            elif char and char.isprintable():
                self.user_input.append(char)
        
        self._show_results()
    
    def _show_results(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        text_str = ' '.join(self.text)
        user_str = ''.join(self.user_input)
        
        elapsed = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        typed_chars = len(self.user_input)
        correct_chars = 0
        errors = 0
        
        for i in range(min(typed_chars, len(text_str))):
            if i < len(self.user_input):
                if self.user_input[i] == text_str[i]:
                    correct_chars += 1
                else:
                    errors += 1
        
        accuracy = (correct_chars / typed_chars * 100) if typed_chars > 0 else 0
        wpm = (correct_chars / 5) / (elapsed / 60) if elapsed > 0 else 0
        
        print(f"{Fore.CYAN}{Style.BRIGHT}=== Results ==={Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Speed (WPM): {Fore.WHITE}{wpm:.1f}")
        print(f"{Fore.YELLOW}Accuracy: {Fore.WHITE}{accuracy:.1f}%")
        print(f"{Fore.YELLOW}Errors: {Fore.WHITE}{errors}")
        print(f"{Fore.YELLOW}Time: {Fore.WHITE}{elapsed:.2f} seconds")
        print(f"{Fore.YELLOW}Characters: {Fore.WHITE}{typed_chars}/{len(text_str)}")
        print()
        
        print(f"{Fore.CYAN}Your input:{Style.RESET_ALL}")
        for i, char in enumerate(user_str[:len(text_str)]):
            if i < len(text_str):
                if char == text_str[i]:
                    print(Fore.GREEN + char, end='')
                else:
                    print(Fore.RED + char, end='')
            else:
                print(Fore.RED + char, end='')
        print()
        
        print(f"\n{Fore.CYAN}Correct text:{Style.RESET_ALL}")
        print(text_str)
        print()


def main():
    import argparse
    
    loader = LanguageLoader()
    available_languages = loader.list_languages()
    
    if not available_languages:
        print(f"{Fore.RED}Error: No languages found in 'languages' directory!")
        print(f"{Fore.YELLOW}Please create language JSON files in the 'languages' folder.")
        sys.exit(1)
    
    default_lang = loader.get_default_language()
    if not default_lang:
        default_lang = loader.get_language(available_languages[0])
    
    parser = argparse.ArgumentParser(
        description='Termitype - Terminal typing speed test',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Available languages: {', '.join(available_languages)}"
    )
    parser.add_argument('-l', '--language', type=str, default=default_lang.name if default_lang else available_languages[0],
                       help=f'Language name (default: {default_lang.name if default_lang else available_languages[0]})')
    parser.add_argument('-w', '--words', type=int, default=25,
                       help='Number of words in the test (default: 25)')
    parser.add_argument('--list-languages', action='store_true',
                       help='List all available languages and exit')
    
    args = parser.parse_args()
    
    if args.list_languages:
        print(f"{Fore.CYAN}Available languages:{Style.RESET_ALL}")
        for lang_name in available_languages:
            lang = loader.get_language(lang_name)
            if lang:
                print(f"  {Fore.YELLOW}{lang_name}{Style.RESET_ALL} - {len(lang.words)} words")
        sys.exit(0)
    
    language = loader.get_language(args.language)
    if not language:
        print(f"{Fore.RED}Error: Language '{args.language}' not found!")
        print(f"{Fore.YELLOW}Available languages: {', '.join(available_languages)}")
        print(f"{Fore.YELLOW}Use --list-languages to see all available languages.")
        sys.exit(1)
    
    try:
        test = TypingTest(language=language, words_count=args.words)
        test.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Test interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
