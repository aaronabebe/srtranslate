import argparse
import dataclasses
from typing import List

from llama_cpp import Llama
from tqdm import tqdm


@dataclasses.dataclass
class SrtEntry:
    start: str
    end: str
    text: str


def get_translation(
    llm: Llama, start_lang: str, target_lang: str, srt_entry: SrtEntry
) -> SrtEntry:
    resp = llm(
        f"Q: Perfectly translate this from {start_lang} to {target_lang}. Leave out any notes or suggestions, only reply with the ideal translation: {srt_entry.text} \nA:",
        max_tokens=32,
        stop=["Q:", "\n"],
        echo=False,
    )

    srt_entry.text = resp["choices"][0]["text"]
    return srt_entry


def load_srt(file_path: str) -> List[SrtEntry]:
    entries = []
    with open(file_path, "r", encoding="utf-8") as file:
        entry_lines = file.read().strip().split("\n\n")
        for entry in entry_lines:
            lines = entry.split("\n")
            if len(lines) >= 3:
                _ = lines[0]  # Not used, but parsed to maintain structure
                time_range = lines[1]
                text = "\n".join(lines[2:])
                start, end = time_range.split(" --> ")
                entries.append(SrtEntry(start=start, end=end, text=text))
    return entries


def save_srt(entries: List[SrtEntry], file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        for i, entry in enumerate(entries, start=1):
            block = f"{i}\n{entry.start} --> {entry.end}\n{entry.text}\n"
            file.write(block + "\n")


def main(args: argparse.Namespace):
    llm = Llama.from_pretrained(
        repo_id=args.model,
        filename=args.model_file,
        verbose=False,
        chat_format="llama-2",
    )
    translated_srt = [
        get_translation(llm, args.source, args.target, srt)
        for srt in tqdm(load_srt(args.input))
    ]
    save_srt(translated_srt, args.output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="SRTranslate\n\nTranslate your .srt files into almost any language."
    )
    parser.add_argument(
        "--source",
        type=str,
        required=True,
        help="The initial language of your .srt file.",
    )
    parser.add_argument(
        "--target",
        type=str,
        required=True,
        help="The target language of your .srt file.",
    )
    parser.add_argument(
        "--input", type=str, required=True, help="Path to your .srt file."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="out.srt",
        help="Path to your new translated .srt file.",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="TheBloke/OpenHermes-2.5-Mistral-7B-GGUF",
        help="The model to use for translation.",
    )
    parser.add_argument(
        "--model_file",
        type=str,
        default="openhermes-2.5-mistral-7b.Q2_K.gguf",
        help="The quantized model file in GGUF format to load for translation.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
