from cx_Freeze import setup, Executable

setup(
    name="ObsidianDocsSync",
    version="0.1",
    description="Sync Obsidian Vault with Google Docs / MS Word",
    executables=[Executable("main.py")]
)
