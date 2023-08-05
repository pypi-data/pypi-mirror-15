# Screenshot

![Screenshot of latexsnapshots](https://raw.githubusercontent.com/sirrice/latexsnapshots/master/latexsnapshots/static/screenshot.png)

# Usage

* Create a config file (below)
* Generate snapshots of your latex document.  The code currently creates a snapshot every time
  the Levenshtein distance between the `*.tex` documents is greater than 4000.  In the future, this can be
  configurable

        latexsnapshots latex

  * Note that `latexsnapshots` will create a sqlite database file based on your config file contents.  The path is relative to your current directory.
* Run the server to see thumbnails of your snapshots

        latexsnapshots server


# Create a config file

Create a python file called `config.py` in your current directory.  `latexsnapshots` will look in your current
directory to import this file.

        # where to store the data, no need to change this
        dburi = "sqlite:///latex2.db"

        # absolute path to the git_repo for your paper
        git_repo = "/tmp/animated"

        # what name for the paper?
        paper_name = "infovis16_approx"

        # the latex document directory (within the git repo)
        latex_dir = "docs/infovis16_approx"

        def make_cmds(dstpath):
          """
          @param dstpath Where the generated latex file should be moved to
          @return a list of commands to run to generate the latex file and move it to dstpath
          """
          cmds = [
            "cd /tmp/animated/docs/infovis16_approx",
            "latexrun main",
            "cp latex.out/main.pdf %s" % dstpath
          ]
          return cmds

