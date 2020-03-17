# Automating AWS with Python

Repo for AWS Python Code

## 01-webotron

Script that will sync a local directory to an S3 bucket, and optionally configure R53 and Cloudfront.

### Features

Webotron currently has these features:

- List buckets
- List contents of a bucket
- Create and set up bucket for static website hosting
- Sync directory contents with bucket
- Set AWS profile with --profile <profileName>
- Configure route 53 domain