# What?

Point `latexsnapshots` to your git repo, and it will go through the commits and identify those that change your tex files in a significant way,
and regenerate the pdf files.  It will also take thumbnails of those pdfs, and show them in a web UI.

Install it

        pip install latexsnapshots

# Screenshot

![Screenshot of latexsnapshots](https://raw.githubusercontent.com/sirrice/latexsnapshots/master/latexsnapshots/static/screenshot.png)

## Live Demo

See the output of the `export` command here [http://www.eugenewu.net/latexsnapshots/html/](http://www.eugenewu.net/latexsnapshots/html/)

# Usage

* Create a config file (below)
* Generate snapshots of your latex document.  The code currently creates a snapshot every time
  the Levenshtein distance between the `*.tex` documents is greater than a configurable distancte,
  and when it's been more than X hours since the last snapshotted commit.

        latexsnapshots latex

  * Note that `latexsnapshots` will create a sqlite database file based on your config file to store metadata about the snapshots.  
    The `dburi` path is relative to your current directory.
* Run the server to see thumbnails of your snapshots.  You can run this while `latexsnapshots latex` is running

        latexsnapshots server

* Export everything into a folder for deployment as static website: [See example](http://eugenewu.net/latexsnapshots/html/)

        mkdir outputdir
        latexsnapshots export -o outputdir

        # see the website
        cd outputdir/
        python -m SimpleHTTMServer 8000

        # go to localhost:8000/html


# Create a config file

Create a python file called [config.py](config.py) in your current directory.  `latexsnapshots` will look in your current
directory to import this file.

        ###########################################
        #
        #    Required
        #
        ##########################################


        # absolute path to the git_repo
        # Make sure things are committed!  
        # We will need to checkout many commit points as part of the rollback procedure.
        git_repo = "/tmp/animated"

        # what name for the paper?
        paper_name = "infovis16_approx"

        # the latex document directory (within the git repo)
        latex_dir = "docs/infovis16_approx"

        # A function that returns shell commands for compiling the latex doc and 
        # copying it to the destination location
        def make_cmds(dstpath):
          """
          @param dstpath Where the generated latex file should be moved to
          @return a list of shell commands to run to generate the latex file and move it to dstpath
          """
          cmds = [
            "cd /tmp/animated/docs/infovis16_approx",
            "latexrun main",
            "cp latex.out/main.pdf %s" % dstpath
          ]
          return cmds


        ###########################################
        #
        #    Optional
        #
        ##########################################

        # minimum edit distance of tex files to take a snapshot (4000 is pretty conservative)
        min_edit_distance = 1000

        # Don't create a snapshot if the previous one was within X hours of this commit
        min_hours_gap = 12

        # where to store the data, no need to change this
        dburi = "sqlite:///latex2.db"

