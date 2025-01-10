import subprocess
import os

def convert_notebook_to_html(notebook_name):
    """
    Converts a Jupyter Notebook to an HTML file, excluding the input cells (code), 
    and saves it in a 'reports' folder located at the same level as the notebook folder.

    Parameters:
        notebook_folder (str): Path to the folder containing the notebook.
        notebook_name (str): Name of the notebook file to convert (e.g., 'example_notebook.ipynb').
    """
    try:
        # Construct the full path to the notebook
        relative_directory = os.path.join(os.path.dirname(__file__), '../notebooks')
        notebook_path = os.path.join(relative_directory, notebook_name)
        print(notebook_path)

        # Define the output folder ('reports' is at the same level as 'notebooks')
        reports_folder = os.path.join(os.path.dirname(__file__), '../reports')
        print(reports_folder)

        # Ensure the 'reports' folder exists
        os.makedirs(reports_folder, exist_ok=True)

        # Construct the output HTML path
        output_path = os.path.join(reports_folder, f"{os.path.splitext(notebook_name)[0]}.html")

        # Run the nbconvert command
        subprocess.run([
            'jupyter', 'nbconvert', '--to', 'html', '--execute', '--no-input', 
            '--output', output_path, notebook_path
        ], check=True)

        print(f"Notebook converted and saved as HTML: {output_path}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred during nbconvert: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
notebook_name = 'pato_meteo.ipynb'

convert_notebook_to_html( notebook_name)