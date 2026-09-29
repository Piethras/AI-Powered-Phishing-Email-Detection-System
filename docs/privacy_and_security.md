# Data Handling, Privacy & Security

## What is stored
When an email is scanned (via upload or manual paste), the sender
address, subject, and the first 500 characters of the body are stored
in MySQL, along with the prediction result. Full raw email content
beyond that snippet is not persisted.

## Data deletion
Stored records can be permanently removed via `DELETE
/api/emails/<id>`, which deletes the email and its associated
predictions and feedback. This was verified working (email id 9,
stale test data, successfully deleted).

## What is NOT currently implemented (documented limitation, not oversight)
- No encryption at rest for stored email content.
- No authentication/access control in front of the API or dashboard -
  an intentional scope decision for an academic prototype, not an
  unnoticed gap.
- No automatic/scheduled data retention policy; records persist until
  manually deleted via the endpoint above.
- No consent mechanism for third-party email content (relevant if
  scanning email not authored by the system's operator).

## What IS in place
- SQLAlchemy's ORM uses parameterized queries throughout, preventing
  SQL injection.
- The email parser (Day 4) only reads content via Python's `email`
  library; it never executes attachments or embedded scripts.
- Whitelist and feedback actions carry an audit trail (who, when).
- A working deletion endpoint allows removing stored email records on
  request.

## Scope statement
This system is a local, single-user academic prototype, evaluated on
public research datasets and the developer's own test emails - not a
multi-tenant production service handling third-party PII at scale.
Production deployment would require: encryption at rest, proper
authentication/authorization, a formal data retention/deletion policy,
and (if deployed in a jurisdiction with a relevant data protection
regime, e.g. GDPR) a compliance review before processing real user email.
This gap is stated explicitly here rather than left implicit.