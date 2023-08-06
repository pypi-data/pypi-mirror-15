========================
``load(oid)`` must die!
========================

Currently, we use ``load(oid)`` to load current data for an object
unless we've recieved an invalidation for it (the object).  This leads to
complex code that:

- checkes to see if an object has been invalidated and if not:

- loads the object using ``load``, and

- if while loading, the object was invalidated, it then reloads using
  ``loadBefore``.

The ``IStorage.load`` method is problematic because it's required to
load current data.  This leads to delicate ordering of ``load``
results and invalidations, which also provide information about the
current version of an object.  In FileStorage, we also have to get a
read lock on the file before we load current data, to prevent writes.

In reviewing NEO, I realized that there's no reason for ``load`` to
exist, and in fact, NEO doesn't really implement it.

First of all, it makes no sense to use ``load`` if the transaction
time (``Connection._txn_time``) is known.  We should just use
``loadBefore`` with the transaction time.

Second, one can choose a suitable transaction time at the beginning of
a transaction.  A suitable transaction time is just past (because we
use ``loadBefore``) the database transaction time.  We don't want to
read any data that was written later, regardless of what we've gotten
invalidations for.  We can use ``IStorage.lastTransaction()`` to
determine the last transaction id(/time). For storages with remote
data, like ZEO or NEO, we might choose to request the last transaction
id from the remote server to make sure we've processed any in-flight
transactions.  This is what NEO does.  (More about this in a separate
issue.)

By determining the transaction time at the start of a transaction, we
can:

- Always call ``loadBefore`` which can be much more efficiently
  implemented than ``load()``.

- Greatly simplify ``Connection._setstate``.

- Greatly simplify logic of ZEO, and perhaps NEO or RelStorage.

So, in conclusion:

- Reimplement transaction handling in Connection to set ``_txn_time``
  at the beginning of a transaction using
  ``p64(u64(storage.lastTransaction()) + 1)``.

- Simplify `_setstate` by always calling ``loadBefore`` using ``_txn_time``.

  Update ``get(oid)`` in a similar fashion.  (This is probably not as big
  an issue in this case, as ``get(oid)`` doesn't load object state,
  but I still want to deprecate ``load``.)
