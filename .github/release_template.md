# Checklist for creating a new release

- [ ] Update `CHANGELOG.md` for the new version
- [ ] Change version number in `docs/source/conf.py`, `greedybear/settings.py`
- [ ] Verify CI Tests
- [ ] Create release for the branch `develop`
- [ ] Wait for dockerHub to finish the builds (not available yet)
- [ ] Merge the PR to the `main` branch

**Note:** Only use "Merge and commit" as the merge strategy and not "Squash and merge". Using "Squash and merge" makes history between branches misaligned.

