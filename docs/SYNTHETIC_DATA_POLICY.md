# Synthetic Data Policy

Every business, visitor, conversation, credential, source, and operational record in this repository is fictional. The project was implemented as a clean-room showcase and contains no copied client database, message, configuration, source path, identifier, or secret.

Synthetic identifiers use obvious labels such as `northstar-demo`, `harbor-demo`, and `Demo visitor`. Credentials in `.env.example`, tests, and Compose are local demonstration strings with no access to any external service. The fake provider adapter performs no network request.

The public safety scanner blocks contact patterns, user-home paths, common token formats, private keys, and private source-repository names in both the current tree and Git history.
