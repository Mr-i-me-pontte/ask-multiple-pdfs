#!/bin/bash

# Create a new Markdown file called directory_files.md
echo -e "# Directory Files\n" > directory_files.md

# Loop through each file in the current directory
for file in *; do
    # Exclude specific files from the list
    if [ "$file" != "create_directory_files_md.sh" ] && [ "$file" != "directory_files.md" ]; then
        # Check if the item is a file (not a directory)
        if [ -f "$file" ]; then
            # Get the filename without the path
            filename=$(basename "$file")

            # Get the file content
            fileContent=$(cat "$file")

            # Append a new section to the Markdown file
            echo -e "## $filename\n" >> directory_files.md
            echo -e "\`\`\`python\n$fileContent\n\`\`\`\n" >> directory_files.md
        fi
    fi
done

echo "Markdown file 'directory_files.md' has been created with sections for each file."
