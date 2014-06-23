#!/usr/bin/python
#
# Copyright (C) 2009 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provides functions to persist serialized auth tokens in the datastore.

The get_token and set_token functions should be used in conjunction with
gdata.gauth's token_from_blob and token_to_blob to allow auth token objects
to be reused across requests. It is up to your own code to ensure that the
token key's are unique.
"""
from __future__ import unicode_literals

__author__ = 'j.s@google.com (Jeff Scudder)'


from google.appengine.ext import db
from google.appengine.api import memcache


class Token(db.Model):
  """Datastore Model which stores a serialized auth token."""
  t = db.BlobProperty()


def get_token(unique_key):
  """Searches for a stored token with the desired key.

  Checks memcache and then the datastore if required.

  Args:
    unique_key: str which uniquely identifies the desired auth token.

  Returns:
    A string encoding the auth token data. Use gdata.gauth.token_from_blob to
    convert back into a usable token object. None if the token was not found
    in memcache or the datastore.
  """
  token_string = memcache.get(unique_key)
  if token_string is None:
    # The token wasn't in memcache, so look in the datastore.
    token = Token.get_by_key_name(unique_key)
    if token is None:
      return None
    return token.t
  return token_string


def set_token(unique_key, token_str):
  """Saves the serialized auth token in the datastore.

  The token is also stored in memcache to speed up retrieval on a cache hit.

  Args:
    unique_key: The unique name for this token as a string. It is up to your
        code to ensure that this token value is unique in your application.
        Previous values will be silently overwitten.
    token_str: A serialized auth token as a string. I expect that this string
        will be generated by gdata.gauth.token_to_blob.

  Returns:
    True if the token was stored sucessfully, False if the token could not be
    safely cached (if an old value could not be cleared). If the token was
    set in memcache, but not in the datastore, this function will return None.
    However, in that situation an exception will likely be raised.

  Raises:
    Datastore exceptions may be raised from the App Engine SDK in the event of
    failure.
  """
  # First try to save in memcache.
  result = memcache.set(unique_key, token_str)
  # If memcache fails to save the value, clear the cached value.
  if not result:
    result = memcache.delete(unique_key)
    # If we could not clear the cached value for this token, refuse to save.
    if result == 0:
      return False
  # Save to the datastore.
  if Token(key_name=unique_key, t=token_str).put():
    return True
  return None


def delete_token(unique_key):
  # Clear from memcache.
  memcache.delete(unique_key)
  # Clear from the datastore.
  Token(key_name=unique_key).delete()
