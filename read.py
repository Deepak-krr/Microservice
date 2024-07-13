# generate_readme.py

def generate_readme():
    # Fetch project information (e.g., docstrings, file names, etc.)
    project_name = "Microservice"
    description = "Creating a microservice application using Flask framework in python"
    author = "Deepak Kumar"
    email = "deepak.ce2k15@gmail.com"
    # Add more information as needed...

    # Generate README content
    readme_content = f"""
    # {project_name}

    {description}

    ## Installation

    ## Usage

    ## Contributing

    ## Authors

    {author} - {email}

    ## License
    """

    # Write content to README.md
    with open('README.md', 'w') as f:
        f.write(readme_content)

if __name__ == "__main__":
    generate_readme()
