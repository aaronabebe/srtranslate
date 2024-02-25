# srtranslate

`srtranslate` is a Python-based tool designed to automate the translation of subtitles. 
Leveraging LLM translation via `llama_cpp_python`, it offers high-quality translations across multiple languages.

---

## Features

- **Automatic Translation**: Support for multiple languages.
- **Customizable Translation Engines**: Integrates with various LLMs.
- **Format Preservation**: Maintains the original subtitle format, ensuring timing and text formatting are kept intact.
- **CLI Support**: Easy-to-use command-line interface for quick translations and script integrations.

## Installation

Clone this repo.

```bash
pip install
```

## Usage

Translate a subtitle file from English to French:

```bash
srtranslate translate --input /path/to/input.srt --output /path/to/output.srt --source en --target fr
```

## License

`srtranslate` is released under the MIT License. See [LICENSE](LICENSE) for details.

