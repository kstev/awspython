#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Webotron: Deploy websites to AWS.

Webotron allows you to create static websites
- Configure AWS S3 buckets
 - Create
 - Enable static website hosting on a bucket
 - Sync a local directory to a bucket
- Configure DNS with AWS Route 53
- Configure a CDN and SSL with AWS CloudFront
"""

import boto3
import click

from bucket import BucketManager
from domain import DomainManager

session = None
bucket_manager = None

@click.group()
@click.option('--profile', default=None,
            help="Use a given AWS profile.")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager, domain_manager

    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile

    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)
    domain_manager = DomainManager(session)


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in an s3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create website enabled bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)
    url = 'http://%s.s3-website.%s.amazonaws.com' % (s3_bucket.name, session.region_name)
    return url


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contents of PATH to BUCKET."""
    bucket_manager.sync(pathname, bucket)
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))

@cli.command('setup-domain')
@click.argument('domain')
@click.argument('bucket')
def setup_domain(domain, bucket):
    """Configure DOMAIN to point to BUCKET."""
    bucket = bucket_manager.get_bucket(domain)

    zone = domain_manager.find_hosted_zone(domain) \
        or domain_manager.create_hosted_zone(domain)

    endpoint = util.get_endpoint(bucket_manager.get_region_name(bucket))
    domain_manager.create_s3_domain_record(zone, domain, endpoint)
    print("Domain configured: http://{}".format(domain))


if __name__ == '__main__':
    cli()
