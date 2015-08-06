# **prompt**

This tool allows you to easily customize your terminal's prompt to display all sorts of useful information, including info about projects with version control. 

**prompt** replaces patterns enclosed in curly braces `{`, `}` with information about the current environment:
The pattern

    {user} at ({branch}) on [{repo}] $
    
becomes 

    rkargon at (master) on [prompt] $ _

Colors can also be inserted into the prompt, taking care of ANSI color codes for you:


    
## Installation
Download the repository, using:

    git clone https://github.com/rkargon/prompt.git

Then run  
    
    python setup.py install

## Using prompt
To test **prompt**, use the `prompt` command with a pattern of your choosing. 

## Documentation
### Syntax
### Possible Directives:
- `{user}`
- `{cwd}`
### Examples