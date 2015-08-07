# **prompt**

This tool allows you to easily customize your terminal's prompt to display all sorts of useful information, including info about projects with version control (currently supports git and mercurial). 

**prompt** replaces patterns enclosed in curly braces `{`, `}` with information about the current environment:
The pattern

    {user} at ({branch}) on [{repo}] $
    
becomes 

    rkargon at (master) on [prompt] $ _

Colors can also be inserted into the prompt, taking care of ANSI color codes for you:

    {host}:{cwd} {col:red}{user}{col:reset}$
    
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
	    prompt "{ [{col:blue}{branch}{col:reset}{col:red}{status}{col:reset}]}$" 2> /dev/null
	}
	
	PS1='$(prompt_ps1)'

This will set your prompt variable at startup to use **prompt**. Use the `source` command to refresh your terminal and see these changes. 

## Documentation

### Syntax
Patterns are enclosed with braces, like `{this}`. Attributes can be added to a pattern, by appending colons: `{pattern:arg1:arg2:arg3}`.  If the text in the braces is not a valid pattern, it is simply returned unchanged. For instance, `{some text}` would return `some text`.  This allows you to nest patterns. Why would you want to do this? Some patterns are not always valid, depending on the state of your environment. For instance, `{branch}` doesn't make much sense when you're not in a repository. When a pattern fails, all the enclosing patterns will return an empty string. Thus, the pattern `{user}{on {branch}}$ ` can produce either `rkargon on master$ `, or `rkargon$ `,  depending on the situation. 

### Possible Directives:
- `{col:colname}` Changes the output's color to the color 'colname'. Options are black, red, green, yellow, blue, magenta, cyan, white, and 'reset', which returns the terminal to its default color. 
- `{cwd}` Displays the current working directory. 
- `{date}` Displays the current date and time.
- `{host}` Displays the current host machine.
- `{user}` Displays the current user. 
- `{branch}` Displays the current version-control repository's branch.
- `{repo}` Displays the name of this repository's local root directory. 
- `{status}` If the current repository contains uncommited changed, `!` is displayed. Otherwise, this pattern produces no output. 

### Examples
1. A simple prompt that shows the current branch, as well as whether or not there are uncommitted changes:
`{host}:{cwd} {user}{ [{repo}/{branch}{status}]}$ ` becomes
`raphbox:prompt rkargon [prompt/master!]$ _`
