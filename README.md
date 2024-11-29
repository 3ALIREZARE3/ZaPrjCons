## Project Consolidator

This project provides three different tools to help you consolidate code files from either a local folder or a GitHub repository into a single text file with detailed information about each file (name, location, size, number of lines, and content). This is particularly useful for analyzing codebases, sharing code snapshots, or providing context to language models.

### Versions

1. **GUI Application (using tkinter)**

   - **Description:** A user-friendly desktop application with a graphical interface that allows you to browse and select a local folder to consolidate. The output is saved to a `consolidated_project.txt` file in the same directory as the script.
   - **How to Use:**
     1. Run the Python script (`project_consolidator.py`).
     2. Click "Browse Folder" to select the project directory.
     3. Click "Consolidate Project".
     4. The consolidated content will be saved in `consolidated_project.txt`.
   - **Strengths:** Easy to use for users who prefer a visual interface.

2. **Flask Web Application**

   - **Description:** A web-based tool that allows you to consolidate code files from a GitHub repository by providing its URL. The consolidated content is downloaded as a text file through the browser.
   - **How to Use:**
     1. Run the Flask app (`github_consolidator.py`).
     2. Open your browser and go to `http://127.0.0.1:5000/`.
     3. Enter the GitHub repository URL in the input field.
     4. Click "Consolidate".
     5. The browser will download `consolidated_project.txt`.
   - **Strengths:** Accessible from any device with a web browser, convenient for remote repositories.

3. **Command-Line Tool**

   - **Description:** A command-line utility that can consolidate code from either a local folder path or a GitHub repository URL. The output can be printed to the console or saved to a specified file.
   - **How to Use:**
     - **GitHub Repository:** `python consolidate.py <GitHub URL> [-o <output_file>]`
     - **Local Folder:** `python consolidate.py <folder_path> [-o <output_file>]`
     - If `-o` is not specified, the output is printed to the console.
   - **Strengths:** Flexible and scriptable, suitable for integration into workflows and automation. Can be converted to a standalone executable using PyInstaller for easy distribution.

### Features

- **Detailed File Information:** Each file's name, location (path or tree structure), size (in bytes), and number of lines are included.
- **Separated Content:** Content of each file is clearly separated by a line of equal signs (`==========`).
- **Error Handling:** Basic error handling for file read issues and GitHub API requests.
- **Cross-Platform:** Python code ensures compatibility across different operating systems.

### Getting Started

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   ```
2. **Choose a Version:** Navigate to the directory of the version you want to use (e.g., `gui`, `web`, `cmd`).
3. **Install Dependencies:**
   - For the web app, install Flask and Requests: `pip install Flask requests`
   - For the GUI and CMD versions, only standard Python libraries are needed.
4. **Run the Application:** Follow the specific instructions for the chosen version as described above.

### Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.
