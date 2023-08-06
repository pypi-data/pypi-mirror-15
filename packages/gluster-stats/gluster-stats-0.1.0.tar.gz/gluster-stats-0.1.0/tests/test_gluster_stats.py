#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_gluster_stats
----------------------------------

Tests for `gluster_stats` module.
"""
import hashlib
import json
import os
import shutil
from gluster_stats import gluster_stats
from builtins import object


class TestGlusterStats(object):
    """ Test gluster-stats """

    def test_378_default(self):
        """ Normal Run """
        stats = gluster_stats.GlusterStats(
                  test_file="tests/test_sources/gluster_stats_3.7.8.json")
        output = stats.get_stats()
        del output['generated_timestamp'] # Remove dynamic keys
        del output['gluster_stats_version'] # Remove dynamic keys
        print(json.dumps(output, indent=1, sort_keys=True))
        assert output == {
             "brick_stats": {
              "preprodcomms": [
               {
                "disk_free": 982151646412, 
                "disk_total": 1064615018496, 
                "disk_usage_percent": "0.08", 
                "disk_used": 82463372084, 
                "inode_free": 206325202, 
                "inode_total": 208035840, 
                "inode_usage_percent": "0.01", 
                "inode_used": 1710638, 
                "online": 1
               }, 
               {
                "disk_free": 984191755878, 
                "disk_total": 1064615018496, 
                "disk_usage_percent": "0.08", 
                "disk_used": 80423262618, 
                "inode_free": 206325528, 
                "inode_total": 208035840, 
                "inode_usage_percent": "0.01", 
                "inode_used": 1710312, 
                "online": 1
               }, 
               {
                "disk_free": 985802368614, 
                "disk_total": 1064615018496, 
                "disk_usage_percent": "0.07", 
                "disk_used": 78812649882, 
                "inode_free": 206325083, 
                "inode_total": 208035840, 
                "inode_usage_percent": "0.01", 
                "inode_used": 1710757, 
                "online": 1
               }
              ]
             }, 
             "gluster_version": "3.7.8", 
             "glusterd": 1, 
             "glusterfsd": 1, 
             "peers": 2, 
             "split_brain_entries": {
              "preprodcomms": 0
             }, 
             "unhealed_entries": {
              "preprodcomms": 855
             }, 
             "volume_count": 1, 
             "volumes": [
              "preprodcomms"
             ]
            }

    def test_375_default(self):
        """ Normal Run """
        stats = gluster_stats.GlusterStats(
                  test_file="tests/test_sources/gluster_stats_3.7.5.json")
        output = stats.get_stats()
        del output['generated_timestamp'] # Remove dynamic keys
        del output['gluster_stats_version'] # Remove dynamic keys
        print(json.dumps(output, indent=1, sort_keys=True))
        assert output == {
             "brick_stats": {
              "u01gluster": [
               {
                "disk_free": 824204224102, 
                "disk_total": 824204224102, 
                "disk_usage_percent": "0.00", 
                "disk_used": 0, 
                "inode_free": 161060390, 
                "inode_total": 161060416, 
                "inode_usage_percent": "0.00", 
                "inode_used": 26, 
                "online": 1
               }, 
               {
                "disk_free": 824204224102, 
                "disk_total": 824204224102, 
                "disk_usage_percent": "0.00", 
                "disk_used": 0, 
                "inode_free": 161060390, 
                "inode_total": 161060416, 
                "inode_usage_percent": "0.00", 
                "inode_used": 26, 
                "online": 1
               }, 
               {
                "disk_free": 824204224102, 
                "disk_total": 824204224102, 
                "disk_usage_percent": "0.00", 
                "disk_used": 0, 
                "inode_free": 161060390, 
                "inode_total": 161060416, 
                "inode_usage_percent": "0.00", 
                "inode_used": 26, 
                "online": 1
               }
              ]
             }, 
             "gluster_version": "3.7.5", 
             "glusterd": 1, 
             "glusterfsd": 1, 
             "peers": 2, 
             "split_brain_entries": {
              "u01gluster": 0
             }, 
             "unhealed_entries": {
              "u01gluster": 0
             }, 
             "volume_count": 1, 
             "volumes": [
              "u01gluster"
             ]
            }
