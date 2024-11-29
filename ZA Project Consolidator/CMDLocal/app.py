import argparse
import requests
import os


def get_file_info(filename, content):
    """Collects file information from content."""
    try:
        lines = content.splitlines()
        size = len(content.encode("utf-8"))
        num_lines = len(lines)
        return {"name": filename, "size": size, "lines": num_lines, "content": content}
    except Exception as e:
        return {"error": str(e)}


def process_github_repo(repo_url):
    """Processes the GitHub repository and consolidates file content."""
    try:
        parts = repo_url.strip("/").split("/")[-2:]
        username, repo_name = parts[0], parts[1]

        api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
        response = requests.get(api_url)
        response.raise_for_status()

        contents = response.json()

        consolidated_content = ""
        for item in contents:
            if item["type"] == "file":
                file_url = item["download_url"]
                file_response = requests.get(file_url)
                file_response.raise_for_status()
                file_content = file_response.text

                info = get_file_info(item["name"], file_content)

                if "error" in info:
                    consolidated_content += (
                        f"Error reading {item['name']}: {info['error']}\n"
                    )
                else:
                    consolidated_content += "=" * 72 + "\n"
                    consolidated_content += f"Name: {info['name']}\n"
                    consolidated_content += f"Size: {info['size']} bytes\n"
                    consolidated_content += f"Lines: {info['lines']}\n"
                    consolidated_content += "\nContent:\n"
                    consolidated_content += info["content"] + "\n"

        return consolidated_content

    except requests.exceptions.RequestException as e:
        return f"Error fetching data from GitHub: {e}"
    except Exception as e:
        return f"An error occurred: {e}"


def process_local_folder(folder_path):
    """Processes a local folder and consolidates file content."""
    consolidated_content = ""
    try:
        for root, _, files in os.walk(folder_path):
            for file in files:
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    info = get_file_info(file, content)

                    if "error" in info:
                        consolidated_content += (
                            f"Error reading {filepath}: {info['error']}\n"
                        )
                    else:
                        consolidated_content += "=" * 14 + "\n"
                        consolidated_content += f"Name: {info['name']}\n"
                        consolidated_content += (
                            f"Location: {filepath}\n"  # Use full path here
                        )
                        consolidated_content += f"Size: {info['size']} bytes\n"
                        consolidated_content += f"Lines: {info['lines']}\n"
                        consolidated_content += "\nContent:\n"
                        consolidated_content += info["content"] + "\n"

                except Exception as e:
                    consolidated_content += f"Error reading {filepath}: {e}\n"

        return consolidated_content

    except Exception as e:
        return f"An error occurred: {e}"


def main():
    """Parses command-line arguments and performs consolidation."""
    parser = argparse.ArgumentParser(
        description="Consolidate project files from GitHub or a local folder."
    )
    parser.add_argument("source", help="GitHub URL or local folder path")
    parser.add_argument("-o", "--output", help="Output file path (optional)")

    args = parser.parse_args()

    if args.source.startswith("http"):
        consolidated_content = process_github_repo(args.source)
    else:
        consolidated_content = process_local_folder(args.source)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as outfile:
                outfile.write(consolidated_content)
            print(f"Consolidated content written to {args.output}")
        except Exception as e:
            print(f"Error writing to file: {e}")
    else:
        print(consolidated_content)


if __name__ == "__main__":
    main()
