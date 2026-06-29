# KuuOS Repository Commit Candidate v0.93

v0.93 derives a deterministic Git tree candidate and commit candidate from one successful v0.92 atomic application receipt, its exact final `RepositorySnapshot`, and an exact parent-tree inventory read from the Git object database.

The layer consumes only values. It does not invoke Git, write an object database, update an index, modify a working tree, create a commit, sign an object, or mutate a reference.

The v0.92 receipt must be structurally valid, have status `REPOSITORY_ATOMIC_APPLICATION_APPLIED`, report a committed application effect, and bind the supplied final snapshot digest exactly.

The receipt source commit is the single parent candidate. It must be a canonical lower-case 40-hex object identifier.

The parent-tree inventory must bind the same parent commit and contain exactly one leaf entry for every path in the final snapshot inventory. Each entry supplies the parent Git mode and object identifier. The inventory must come from the object database and must not use the working tree.

The final snapshot may contain text only for a subset of its paths. This reflects the v0.92 snapshot contract, which preserves the complete path inventory while retaining explicit content only for selected text files.

v0.93 constructs a full tree candidate by overlaying the final text contents on the parent-tree inventory.

For each text path, v0.93 computes a new blob candidate from the exact UTF-8 bytes and preserves the parent Git mode. Text overlay on a gitlink is rejected.

For each non-text path, v0.93 retains the exact parent mode and parent object identifier. It does not infer, read, or regenerate unknown bytes.

Paths must be unique relative paths. Empty segments, dot segments, parent segments, backslashes, control characters, absolute paths, trailing slashes, and file-directory prefix conflicts are rejected.

Each new text blob candidate stores:

```text
path
preserved parent mode
UTF-8 byte count
content SHA-256 binding through canonical_digest
Git SHA-1 blob candidate object ID
```

Directory trees are constructed recursively from all overlaid and retained leaf entries. Git tree entry bodies use mode, UTF-8 name, NUL separator, and raw child object identifier bytes. Entries use Git tree ordering, and each directory receives a Git SHA-1 tree candidate object ID.

The root tree candidate is combined with:

```text
one exact parent commit
one author identity
one committer identity
one canonical commit message
```

Author and committer identities bind name, email, timestamp, and numeric timezone. Invalid delimiters, whitespace-bearing email addresses, negative timestamps, and timezones outside the range from `-1400` to `+1400` are rejected.

The commit message uses LF line endings and exactly one final newline. NUL and carriage-return characters are rejected.

The certificate stores both the traditional Git SHA-1 commit candidate object ID and a SHA-256 digest of the full commit payload. SHA-1 is used only because this certificate models the traditional Git object format. The SHA-256 payload binding remains available for independent integrity comparison.

Certification recomputes every new blob, retained parent entry, subtree, root tree, commit payload, and candidate object ID from the supplied receipt, snapshot, parent inventory, policy, identities, and message. Replacing an object ID and recomputing only the outer certificate digest does not validate.

The policy bounds the complete leaf count and the total UTF-8 byte count of newly represented text contents before candidate construction.

A successful certificate states:

```text
parent_tree_inventory_valid = true
parent_inventory_commit_bound = true
complete_parent_path_coverage = true
parent_modes_preserved = true
object_database_write_performed = false
index_write_performed = false
working_tree_write_performed = false
commit_created = false
reference_mutated = false
signing_performed = false
```

The candidate object ID is therefore a deterministic calculated value, not evidence that the object exists in any Git repository.

A later layer must separately authorize object materialization. Reference mutation remains a still later, separately authorized action.
