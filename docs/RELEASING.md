Notes on releasing tinygraph:

1. Make sure you have bumped the version number in `tinygraph/version.py`. Use reasonable
semantic versioning, with the major.minor.bugfix tradition. 

2. Push to github and verify that CI and readthedocs are working

3. validate that all the necessary issues have been closed and any associated milestones
on github are done. 

3. Use an [lightweight git tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging) for the release, 
   `git tag v1.2.3` or something similar. Be sure to push the tag to github and verify that 
   github sees the tag. 
   
4. [Create a new release on Github](https://github.com/thejonaslab/tinygraph/releases/new). Try and
have reasonable verbose descriptions of what has changed

   
   
