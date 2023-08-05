hatena-haiker: Hatena Haiku for Python 3
========================================

hatena-haiker is an unofficial library
for the `Hatena Haiku <http://h.hatena.ne.jp/>`_ API.


Example
-------

.. code-block:: python

    >>> import haiker
    >>> auth = haiker.OAuth(
    ...     'MyConsumerKey', 'MyConsumerSecret',
    ...     'MyAccessToken', 'MyAccessTokenSecret'
    ... )
    >>> api = haiker.Haiku(auth)
    >>> api.public_timeline(count=3)
    [{'created_at': '...',
      'favorited': '...',
      'id': '...',
      'in_reply_to_status_id': '',
      'in_reply_to_user_id': '',
      'keyword': '...',
      'link': '...',
      'replies': [...],
      'source': '...',
      'target': {...},
      'text': '....',
      'user': {'followers_count': '...',
               'id': '...',
               'name': '...',
               'profile_image_url': '...',
               'screen_name': '...',
               'url': 'http://h.hatena.ne.jp/...'}},
     {...},
     {...}]


Installation
------------

.. code-block:: bash

    $ pip3 install --upgrade hatena-haiker


Documentation
-------------

After completing the installation, enter the following:

.. code-block:: bash

    $ python3 -m pydoc haiker

