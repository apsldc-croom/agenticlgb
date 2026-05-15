# Release Flow

Release process and versioning.

## Release Branches

```
main → develop → release/{version}
                    → hotfix/{version}
```

## Versioning

```
{major}.{minor}.{patch}
```

- Major: Breaking changes
- Minor: New features
- Patch: Bug fixes

## Release Process

```python
def create_release(version):
    # Create branch
    git.checkout_new_branch(f"release/{version}")
    
    # Update version
    update_version_file(version)
    
    # Run release tests
    run_integration_tests()
    
    # Merge to main
    git.merge(f"release/{version}", "main")
    
    # Tag release
    git.tag(f"v{version}", "main")
    
    # Merge back to develop
    git.merge("main", "develop")
```

## Release Checklist

```yaml
release:
  pre_checks:
    - all_tests_pass
    - documentation_updated
    - changelog_generated
  
  steps:
    - create_release_branch
    - run_integration_tests
    - update_version
    - merge_to_main
    - create_tag
    - deploy
  
  post_checks:
    - verify_deployment
    - notify_team
    - update_tracking
```