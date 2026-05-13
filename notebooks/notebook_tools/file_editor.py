from pathlib import Path

import ipywidgets as widgets
from IPython.display import display


def edit(filename, height="350px", width="100%"):
    """
    Inline optional file editor for Jupyter notebooks.

    Usage in notebook:
        edit("my_file.txt")
    """

    path = Path(filename)

    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")

    editor = widgets.Textarea(
        value=path.read_text(),
        layout=widgets.Layout(width=width, height=height),
    )

    save_button = widgets.Button(
        description="Save changes",
        button_style="success",
        tooltip="Write changes back to the file",
    )

    reload_button = widgets.Button(
        description="Reload",
        tooltip="Reload the file from disk",
    )

    close_button = widgets.Button(
        description="Close",
        tooltip="Hide this editor",
    )

    status = widgets.Output()

    box = widgets.VBox([
        widgets.HTML(
            f"<b>Optional:</b> edit <code>{path}</code>. "
            "If no changes are needed, continue to the next cell."
        ),
        editor,
        widgets.HBox([save_button, reload_button, close_button]),
        status,
    ])

    def save_file(_):
        path.write_text(editor.value)
        with status:
            status.clear_output()
            print(f"Saved: {path}")

    def reload_file(_):
        editor.value = path.read_text()
        with status:
            status.clear_output()
            print(f"Reloaded: {path}")

    def close_editor(_):
        box.children = []

    save_button.on_click(save_file)
    reload_button.on_click(reload_file)
    close_button.on_click(close_editor)

    display(box)