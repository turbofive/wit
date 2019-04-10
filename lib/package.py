#!/usr/bin/env python3

import lib.gitrepo


# Make this a factory for different VCS types
class Package:
    """
    Generic package type
    """

    @staticmethod
    def from_arg(s):
        """
        >>> Package.from_arg(".::HEAD")
        lib.gitrepo.GitRepo(source='.', revision='HEAD')
        >>> Package.from_arg("not-a-repo")
        Traceback (most recent call last):
            ...
        argparse.ArgumentTypeError: Remote git repo 'not-a-repo' does not exist!
        """
        # TODO Could speed up validation
        #   - use git ls-remote to validate remote exists
        #   - use git ls-remote to validate revision for tags and branches
        #   - if github repo, check if page exists (or if you get 404)
        # FIXME: This is ugly. Split on '::' into a path and revision, but
        # there may not be a revision. So add an additional array
        source, rev = (s.split("::") + [None])[:2]
        if rev is None:
            rev = "HEAD"

        return lib.gitrepo.GitRepo(source, rev)

    @staticmethod
    def from_manifest(wsroot, m):
        commit = m['commit']
        name = m['name']
        # Source is not required, because the repo may be found on
        # $WIT_REPO_PATH
        source = m.get('source', None)
        path = wsroot / name

        # if not lib.gitrepo.GitRepo.is_git_repo(path):
        #    # TODO implement redownloading from remote
        #    msg = "path '{}' is not a git repo even though it's in the manifest!".format(path)
        #    raise Exception(msg)

        return lib.gitrepo.GitRepo(source, commit, name=name, path=path)


if __name__ == '__main__':
    import doctest
    doctest.testmod()