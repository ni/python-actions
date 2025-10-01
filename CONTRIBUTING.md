# Contributing to `ni/python-actions`

Contributions to `ni/python-actions` are welcome from all!

`ni/python-actions` is managed via [git](https://git-scm.com), with the canonical upstream
repository hosted on [GitHub](https://github.com/ni/<reponame>/).

`ni/python-actions` follows a pull-request model for development.  If you wish to
contribute, you will need to create a GitHub account, fork this project, push a
branch with your changes to your project, and then submit a pull request.

Please remember to sign off your commits (e.g., by using `git commit -s` if you
are using the command line client). This amends your git commit message with a line
of the form `Signed-off-by: Name Lastname <name.lastmail@emailaddress.com>`. Please
include all authors of any given commit into the commit message with a
`Signed-off-by` line. This indicates that you have read and signed the Developer
Certificate of Origin (see below) and are able to legally submit your code to
this repository.

See [GitHub's official documentation](https://help.github.com/articles/using-pull-requests/) for more details.

## Getting Started

To contribute to this project, it is recommended that you follow these steps:

- Fork the repository on GitHub.
- Run the PR workflow on your fork of the repository. At this point, if any tests fail, do not begin
  development. Try to investigate these failures. If you're unable to do so, report an issue through
  our GitHub issues page.
- Write new tests that demonstrate your bug or feature. Ensure that these new tests fail.
- Make your change.
- Run all the regression tests again (including the tests you just added), and confirm that they all
  pass.
- Send a GitHub Pull Request to the main repository's `main` branch. GitHub Pull Requests are the
  expected method of code collaboration on this project.

## Testing

To run the `ni/python-actions` regression tests, run the following command:

```bash
gh workflow run PR.yml --ref users/me/my-dev-branch
```

View the workflow status and logs using the GitHub web UI.

## Publishing a Release

You can publish `ni/python-actions` by creating a GitHub release in the `ni/python-actions` repo.
Here are the steps to follow to publish the package:

- From the main GitHub repo page, select "Create a new release".
- On the "New Release" page, create a new tag using the "Select Tag" drop down. The tag must be the
  letter 'v' followed the version number. Example: v0.1.2.
- Enter a title in the "Release title" field. The title should contain the repo name and version
  tag. For example: ni/python-actions v0.1.2.
- Click "Generate release notes" and edit the release notes.
- Delete entries for PRs that do not affect users, such as "chore(deps):" and "fix(deps):" PRs.
  However, consider including significant dependency updates, such as major version updates.
- Consider grouping related entries.
- Reformat entries to be more readable. For example, change "Blah blah by so-and-so in \#123" to
  "Blah blah (\#123)".
- If this is a pre-release release, check the "Set as a pre-release" checkbox.
- Click "Publish release".
- This repository does not have a publish workflow yet, so you must manually update the `v{major}`
  and `v{major}.{minor}` tags:

  ```bash
  git checkout v0.1.2
  git tag -f v0.1
  git tag -f v0
  git push -f origin v0.1
  git push -f origin v0
  ```

> [!NOTE]
> This GitHub project has immutable releases enabled. Once you publish a release, you can only edit
> the title and description. You cannot modify the full release tag (e.g. `v0.1.2`).

## Developer Certificate of Origin (DCO)

   Developer's Certificate of Origin 1.1

   By making a contribution to this project, I certify that:

   (a) The contribution was created in whole or in part by me and I
       have the right to submit it under the open source license
       indicated in the file; or

   (b) The contribution is based upon previous work that, to the best
       of my knowledge, is covered under an appropriate open source
       license and I have the right under that license to submit that
       work with modifications, whether created in whole or in part
       by me, under the same open source license (unless I am
       permitted to submit under a different license), as indicated
       in the file; or

   (c) The contribution was provided directly to me by some other
       person who certified (a), (b) or (c) and I have not modified
       it.

   (d) I understand and agree that this project and the contribution
       are public and that a record of the contribution (including all
       personal information I submit with it, including my sign-off) is
       maintained indefinitely and may be redistributed consistent with
       this project or the open source license(s) involved.

(taken from [developercertificate.org](https://developercertificate.org/))

See [LICENSE](https://github.com/ni/<reponame>/blob/main/LICENSE)
for details about how `ni/python-actions` is licensed.
