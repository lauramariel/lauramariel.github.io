---
layout: post
title:  "Setting up Github repo access with custom SSH configs"
date:  2025-08-28 15:40:56 -0700
categories: github, git, ssh
---
### Using Custom SSH with Github

1. Make sure the private key file defined exists and that the corresponding public key is defined in the repo's deploy keys. If not, add them.

    ~/.ssh/config format:
    ```
    Host <ssh-alias>
        HostName github.com
        IdentityFile ~/.ssh/<private-key-file>
        Port 22
        IdentitiesOnly yes
    ```
2. Clone the repo
    ```
    git clone git@github.com:<repo-name>
    ```
3. Update remote URL to match what's in SSH config
    ```
    git remote set-url origin git@<ssh-alias>:<repo-name>
    ```

4. Pull and test
    ```
    git branch --set-upstream-to=origin/main main
    git pull
    ```

### Other useful commands

* Setting user for the repo
    ```
    git config user.email "EMAIL"
    git config user.name "USER"
    ```
* Testing git auth
   ```
   ssh -T git@<ssh-alias>
   ```
* Another way to test
  ```
  git push --dry-run origin
  ```