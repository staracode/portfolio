import argparse
import os
import re
import textwrap
import time

import ollama

KNOWN_FILE_EXTENSIONS: tuple[str, ...] = ('.png', '.jpg', '.jpeg', '.webp')
DEFAULT_IMAGE_DIR="./images"
MODEL = "qwen2.5vl:7b"  # Run "ollama list" to get a list of models that we know about.
PROMPT = "Describe this image in 3-10 words suitable for a filename. Only provide a description, no punctuation."

def sanitize_filename(input_filename: str):
    # Spaces become underscores. Hyphens are allowed. Anything non-obviously-alphanumeric becomes an underscore.
    # A couple of special behaviors: changes "%" to "percent".
    # Doesn't change the case. Trims leading/trailing whitespace.
    # So e.g. "  Snake5%ç ç " becomes "Snake5Percent__"
    input_filename = input_filename.strip().replace("%", "percent").replace("$", "dollar")
    input_filename = input_filename.strip().replace("%", "percent")
    # Replace anything else "weird" with a suitable simple character. Don't care about upper/lower case.
    return re.sub(r"[^-A-Za-z0-9._]", "_", input_filename)

def rename_images(img_dir: str):
    if not os.path.exists(img_dir):
        raise IOError(f"Can't find the input image directory `{img_dir}`! Maybe it doesn't exist?")

    n_renamed: int = 0
    n_failed: int = 0
    n_skipped: int = 0
    for filename in os.listdir(img_dir):
        if not filename.lower().endswith(KNOWN_FILE_EXTENSIONS):
            print(f"Skipping this file of a type that we don't know what to do with: {filename}")
            continue # Skip it!

        image_path = os.path.join(img_dir, filename)
        
        print(f"Processing {filename}... (note: NOT reading recursively yet)")
        
        try:
            llm_start_time = time.perf_counter()
            response = ollama.chat(
                model=MODEL,
                messages=[{
                    'role': 'user',
                    'content': PROMPT,
                    'images': [image_path]
                }]
            )
            llm_end_time = time.perf_counter()
            
            original_description = response['message']['content']
            clean_desc = sanitize_filename(original_description)
            
            file_extension = os.path.splitext(filename)[1].lower()  # e.g. ".jpg" or whatever. Includes the dot, notably.
            new_filename = f"{clean_desc}{file_extension}"
            new_path: str = os.path.join(img_dir, new_filename)
            
            # If there's a name collision, try incrementing a counter. Blow up if we need more than 1000 of these
            counter = 1
            while os.path.exists(new_path):
                new_path = os.path.join(img_dir, f"{clean_desc}_{counter}{file_extension}")
                counter += 1
                if counter > 1000:
                    raise IOError(f"How are we STILL getting name collisions? Check {new_path}.")

            # os.rename(image_path, new_path) # Dangerous!
            print(textwrap.dedent(
                f"""
                Ollama thought for {llm_end_time - llm_start_time:.1f} seconds, and wants to perform this renaming:
                {filename} --> {os.path.basename(new_path)}
                Ollama had this to say: <<<{original_description}>>>
                """))
            n_renamed += 1

        except Exception as e:
            print(textwrap.dedent(
                f"""
                Error processing {filename}: {e}.
                Is ollama running already? If not, try running `ollama serve` and make sure you have the expected model (`${MODEL}`)
                """))
            n_failed += 1

    return n_renamed, n_failed, n_skipped

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A renamer.")
    parser.add_argument("--in_dir", type=str, default="", help="The input directory. Will be read, but NOT recursively.")
    args = parser.parse_args()

    input_dir = DEFAULT_IMAGE_DIR if (args.in_dir == "") else args.in_dir

    overall_start_time = time.perf_counter()
    n_good, n_bad, n_skipped = rename_images(input_dir)
    overall_end_time = time.perf_counter()

    elapsed = overall_end_time - overall_start_time
    print(f"""\
          Successfully renamed {n_good} file(s) in {elapsed:.1f} seconds.
          Skipped {n_skipped} that didn't seem like valid image files based on the filename.
          (Failed to rename {n_bad} file(s)).
          """)



