from flask import Flask, request, Response
import requests
import os
import tempfile

app = Flask(__name__)


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
        # Extract username and repo name from URL
        parts = repo_url.strip("/").split("/")[-2:]
        username, repo_name = parts[0], parts[1]

        # Fetch repo contents from GitHub API
        api_url = f"https://api.github.com/repos/{username}/{repo_name}/contents"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

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


@app.route("/", methods=["GET", "POST"])
def index():
    """Handles the web form and processing."""
    if request.method == "POST":
        repo_url = request.form.get("repo_url")
        if repo_url:
            consolidated_text = process_github_repo(repo_url)
            return Response(
                consolidated_text,
                mimetype="text/plain",
                headers={
                    "Content-disposition": "attachment; filename=consolidated_project.txt"
                },
            )
        else:
            return "Please provide a GitHub repository URL."

    return """
        <form method="post">
            <label for="repo_url">GitHub Repository URL:</label><br>
            <input type="text" id="repo_url" name="repo_url" size="50"><br><br>
            <input type="submit" value="Consolidate">
        </form>
    """


if __name__ == "__main__":
    app.run(debug=True)
