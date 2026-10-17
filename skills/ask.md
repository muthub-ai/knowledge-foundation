# Ask

1. `llmwiki2 --bundle wiki ask "<question>"` (the local classifier selects notes, Claude answers with citations).
2. Check every citation against the note it cites. Say plainly what the wiki does not know.
3. If the answer is worth keeping, draft a Question note (`kind: Question`, `status: draft`) on a branch and open a
   pull request. Never file it directly.
