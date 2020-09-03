# Introduction

## Vision

## Code of conduct

# Getting Started

## Feature Requests

## First contribution
Working on your first pull request? You can learn how from these resources:

* [First timers only](https://www.firsttimersonly.com/)
* [How to contribute to an open source project on GitHub](https://egghead.io/courses/how-to-contribute-to-an-open-source-project-on-github)

## Developer Workflow
When starting a new branch - this will ensure that all the work being done starts from x.x.x+1-dev0

```bash
make patch
```

Every commit should increment the build

```bash
make build
```

When a change is ready to be pushed, then release the build

```bash
make release
```

So an example looks like:

```bash
# starting version is 0.3.4
git pull origin master
git branch <issue>
make patch
# version becomes 0.3.5-dev0
# make some changes
# commit
make build
# version is now 0.3.5-dev1
# make some changes
# commit
# version is now 0.3.5-dev2
# ready to push
make release
# version is now 0.3.5
git commit -m 'updating version'
git push
```

Then a pull request is created, when the pull is approved, the tag should be updated to match the version.