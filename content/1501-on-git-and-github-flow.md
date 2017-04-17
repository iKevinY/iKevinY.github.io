Title: On Git and GitHub Flow
Date: 2015-01-01

Recently, I have been making an added effort to seek out and contribute to open source projects on GitHub. The motivation behind this was largely the [24 Pull Requests](http://24pullrequests.com) project, which encourages developers to submit one pull request for each day in December leading up to Christmas. The prospect of being a new contributor to a large, open source project can be daunting, especially to the novice programmer, so this little bit of extrinsic motivation was a nudge in the right direction.

In learning how to properly make use of Git and GitHub, I've referenced a multitude of different resources. With 2015 having just arrived, I'm sure many people have "contribute to more open source projects" on their list of New Year's resolutions as well, so hopefully this article serves as a useful starting point.

## Finding a Project

Choosing a project is left as an exercise to the reader. However, here are my suggestions:

- Look to see if any software you use on a regular basis is open source. Given your familiarity with the software, you will likely be able to identify (and hack on) some bugs or additional features.

- Check out [trending GitHub repositories](https://github.com/trending) for languages that you're familiar with or ones that you're interested in learning, and pick one that seems friendly towards new contributors (most projects on GitHub are) and well-maintained. This technique is useful as you'll be browsing across projects that your fellow open source developers have also deemed interesting.

Remember that even if you can't contribute directly to the codebase due to lack of experience or being overwhelmed by the scale of the project, open source projects appreciate all sorts of contributions. While not as "prestigious", documentation and unit tests are areas that inevitability need to be addressed, and are a good way to become familiar with the project.

## Getting Started

The first step to using Git is installing it. You can do that from Git's [download page](http://git-scm.com/downloads), or through a package manager like Homebrew. My suggestion is to learn Git from the command line, and to avoid using other Git clients; the command line is universal, so being familiar with it to start with will be beneficial in the long run.

That being said, I do have [GitHub for Mac](https://mac.github.com) installed and I use it fairly frequently for selectively choosing specific parts of a file to commit, which is fairly cumbersome to do from the command line. Also, I find looking through the changes that have been made is much easier with the GitHub application compared to using `git diff`.

## Overview

Git tracks content modifications. It does so primarily through the use of commits. Commits can be thought of as snapshots in the development process, and contain authorship and timestamp information among other pieces of metadata. By committing frequently, it becomes trivial to rollback to an old commit if something goes disastrously (or if your simply don't like the changes you made). Because of this, Git (and any other version control system) is extremely powerful, even for projects that aren't collaborative in nature.

There is a convention behind the formatting of commit messages that should be followed, given the collaborative nature of open source projects. The first (or only) line of the commit is a summary of the changes, 50 characters at most, in the imperative tense (as in *add*, not *added*). If you want to expand further, you should leave a blank line and on the third line, begin an extended description wrapped to 72 characters.

Unfortunately, after prolonged periods of time, the quality of commit messages tends to degrade ([relevant XKCD](http://xkcd.com/1296/)). Don't worry about this, though, as you can avoid forcing others to look at your horribly crafted commit messages through a process known as *rebasing*, discussed later in this article.

## Branches and Pull Requests

One concept that is central to Git and GitHub flow is branching. Branches are pointers to commits. When working on feature additions or fixes in a project, it is advisable to *always* work in a separate branch, and either merge or rebase -- discussed later in much more detail -- into the master branch upon competition.

When you open a pull request on GitHub, the branch that you chose is noted. Pushing additional commits to that specific branch will result in them appearing in the pull request. This is one of the strongest cases for using a new branch for every feature or bug fix -- it makes it trivial to open a pull request for that specific change, without incorporating any unrelated changes.

## To Merge or Not to Merge

Merging is the process of merging the commits made in two branches into one branch. This is done when a branch that is being worked on is deemed complete, and the changes are to be merged into the master branch. In the simplest case (where the only commits that have been made are in the topic branch), this is known as a fast-forward merge, and the commits are "played on top of" the master branch. Fast-forward merges can be performed automatically by Git and require no additional effort on the part of the user performing the merge. In other cases, merging either results in a merge commit or the manual resolution of merge conflicts (if the changes made in the branches contradict one another).

Something that Git tutorials tend to gloss over is the rebase command. The reason for this is that rebasing involves *rewriting history*. When you rebase a set of commits, they will change, and if the older set of commits have already been pushed to a remote repository that others have pulled from, pushing new changes will cause a break in continuity for others who try to pull these newly pushed commits. Because of this, it is recommended to only rebase local commits in most cases.

```sh
$ git rebase -i HEAD~n  # rebase the last n commits
```

The `-i` flag stands for *interactive*. Upon executing the command, your `$EDITOR` of choice will open with a list of commits from least recent to most recent preceded by the word "pick":

```
#!text
pick a5b977a Ensure all expected resource files exist
pick f08e801 Add problems 311–320
pick 969f9e5 Update tests to ensure resource correspondence
```

Below the list of commits are some instructions about rebasing, including the available commands. To actually rebase, you make changes to the text in the editor and then close it. Here are the operations that you can perform:

- Delete the line, which will remove the commit entirely.
- Change "pick" to a different command, causing the rebase to execute that command instead.
- Rearrange the lines, which will rearrange the order of the commits.

Typically, a project maintainer might ask for you to squash your pull request. What this actually involves doing is rebasing and using the "squash" command to turn multiple commits into just one or a couple logical commits. For example, if you wanted to turn the three commits listed above into one larger commit, you would edit the file to look like the following:

```
#!text
pick a5b977a Ensure all expected resource files exist
squash f08e801 Add problems 311–320
squash 969f9e5 Update tests to ensure resource correspondence
```

Upon closing the editor, a new editor will open up that allows you to edit the commit message of the newly created single commit. The commit messages of each of the commits being squashed are included for the sake of convenience, and when the editor is closed, the non-commented lines become the new commit message.

I mentioned before that rebasing should only be done with local changes that have not been pushed to a remote repository, but in a pull request, by definition, the commits have already been pushed to your fork of the main repository. In this case, it is fine to rebase and push, since it can be assumed that people have not been actively making changes on the feature/fix branch that your pull request is based on. However, Git will not let you push the rebased commits using `git push` out of safety; you have to use `git push -f` to *force* the push to happen.

## Putting It All Together

After forking the project on GitHub, the typical GitHub workflow might look something like this:

```
#!sh
git clone https://github.com/YOUR_GITHUB_USERNAME/PROJECT_NAME.git
cd PROJECT_NAME
git branch my-feature
git checkout my-feature
nano README.md
rm silly-file.txt
git add -A
git commit
git push -u origin my-feature
```

1. Clone your fork to your local development machine.
2. Change the current directory to the project folder.
3. Create a branch called `my-feature`.
4. Switch to the newly created `my-feature` branch.
5. Make changes to `README.md`.
6. Remove `silly-file.txt`.
7. Stage all (`-A`) changes made, including file creations and deletions. You can specify certain files rather than using the `-A` flag to selectively stage changes.
8. Commit the changes that have been staged. Continue to commit new changes and rebase when needed.
9. Push the `my-feature` branch to remote repository aliased as `origin` (your fork), using the `-u` flag to add the branch as a remote tracking branch. (Subsequent pushes will only requre a `git push` with no additional parameters.) Then, open a pull request using GitHub's web interface!

For other Git-related problems that one may run into, Google can usually provide the answer. Be sure to look at [GitHub's help page](https://help.github.com) and the [Git documentation](http://git-scm.com/doc) itself. Here's to lots of open source contributions in 2015!
