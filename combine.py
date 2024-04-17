import os
import re

def read_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file {filepath}: {e}")
        return None

def resolve_includes(content, base_path):
    # Regular expression to match include and use statements
    include_pattern = re.compile(r'^\s*(include|use) <([^>]+)>', re.MULTILINE)

    def include_replacer(match):
        directive, filename = match.groups()
        included_path = os.path.join(base_path, filename)
        included_content = read_file(included_path)
        if included_content:
            return resolve_includes(included_content, os.path.dirname(included_path))
        else:
            return f"// Error: File not found {included_path}"

    return re.sub(include_pattern, include_replacer, content)

def process_file(filepath):
    base_path = os.path.dirname(filepath)
    content = read_file(filepath)
    if content is not None:
        return resolve_includes(content, base_path)
    return ""

def main():
    root_dir = '/workspaces/KeyV2'  # Change this to the path of your project directory
    combined_content = ''
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.scad'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}...")
                combined_content += process_file(file_path)

    if combined_content:
        with open('combined.scad', 'w') as out_file:
            out_file.write(combined_content)
            print("combined.scad has been written successfully.")
    else:
        print("No content was combined. Please check the input paths and files.")

if __name__ == "__main__":
    main()
