# Fix the
 that was parsed literally as "\
" in fix_imports
import os

for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
            if "\
" in content and "import" in content:
                content = content.replace("\
", "
")
                with open(path, "w") as f:
                    f.write(content)
