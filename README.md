# **prompt**

This tool allows you to easily customize your terminal's prompt to display all sorts of useful information, including info about projects with version control (currently supports git and mercurial). 

**prompt** replaces patterns enclosed in curly braces `{`, `}` with information about the current environment:
The pattern

    {user} at ({branch}) on [{repo}] $
    
becomes 

    rkargon at (master) on [prompt] $ _

Colors can also be inserted into the prompt, taking care of ANSI color codes for you:

    {host}:{cwd} {col|red}{user}{col|reset}$
    
## Installation
Download the repository, using:

    git clone https://github.com/rkargon/prompt.git

Then run  
    
    python setup.py install

## Using prompt
To test **prompt**, use the `prompt` command with a pattern of your choosing. 
`prompt "They call me the '{repo} {branch}'!"` , for instance, will print out `They call me the 'prompt master'!`

To actually modify your terminal prompt, you will need to edit the `PS1` environment variable in your terminal. Add the following code to your `~/.bash_profile`:

    # run prompt, and pipe errors to /dev/null
	prompt_ps1() {
	    prompt "{ [{col|blue}{branch}{col|reset}{col|red}{status}{col|reset}]}$" 2> /dev/null
	}
	
	PS1='$(prompt_ps1)'

This will set your prompt variable at startup to use **prompt**. Use the `source` command to refresh your terminal and see these changes. 

## Documentation

### Syntax
Patterns are enclosed with braces, like `{this}`. Attributes can be added to a pattern, by appending pipes: `{pattern|arg1|arg2|arg3}`.  If the text in the braces is not a valid pattern, it is simply returned unchanged. For instance, `{some text}` would return `some text`.  This allows you to nest patterns. Why would you want to do this? Some patterns are not always valid, depending on the state of your environment. For instance, `{branch}` doesn't make much sense when you're not in a repository. When a pattern fails, all the enclosing patterns will return an empty string. Thus, the pattern `{user}{on {branch}}$ ` can produce either `rkargon on master$ `, or `rkargon$ `,  depending on the situation. 

### Possible Directives:
- `{col|colargs...}` Changes the output's color and style using any number of  `colargs`. `colargs` can be the following:
	- colors: black, red, green, yellow, blue, magenta, cyan, or white
	- background colors, by append 'bg_' to a color name
	- style keywords, including bold, italic, underline, or bold_off, italic_off, etc. to disable styles.
	- ANSI color codes for custom background/foreground, of the form `/[34]8;(?:2;\d+;\d+;\d+|5;\d+)/`
	- fg_reset, bg_reset, and reset to reset foreground color, background color, or reset all text styles, respectively. 
- `{cwd}` Displays the current working directory. Use `|short` to get only the directory name and not the full path.
- `{date}` Displays the current date and time.
- `{host}` Displays the current host machine.
- `{user}` Displays the current user. 
- `{virtualenv}` Displays the current virtualenv (If virtualenv is not enabled, no text is returned.) Usually not necessary, as virtualenv adds its own prefix to the prompt string.
- `{branch}` Displays the current version-control repository's branch.
- `{repo}` Displays the name of this repository's local root directory. Use `|short` to get only the directory name and not the full path.
- `{status}` If the current repository contains tracked changes, "!" is displayed. For untracked changes, "?" is displayed. Otherwise, no output is displayed.

### Examples
1. A simple prompt that shows the current branch, as well as whether or not there are uncommitted changes:
`{host}:{cwd} {user}{ [{repo}/{branch}{status}]}$ ` becomes
`raphbox:prompt rkargon [prompt/master!]$ _`
