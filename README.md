
Some simple usage cases.

### Usage Case: Adding Missing Geography Codes

This is where a code **does** exist (for instance: http://statistics.data.gov.uk/id/statistical-geography/E38000228)
but does not yet exists in our graph so is being rejected my PMD with an error like the following.

```
Testcase All pmd:codesUsed must have a label (for PMD dataset search)
Expected empty result set, got:
code
http://statistics.data.gov.uk/id/statistical-geography/E38000228
```

#### To add to the graph:

- Install rapper with `brew install raptor`
- Clone this repo then cd into it.
- Add the urls of the missing codes to a file (missing.txt) within that cloned repo, one code url per line.
- `chmod +x ./fetch_urls.sh`
- `./fetch_urls.sh < missing.txt >> vocabs/reference-geography.ttl`
- sanity check with `rapper -i turtle -c vocabs/reference-geography.ttl`.

If rapper reads without any errors you'll get output similar to the following (with a different path and count) which confirms the file can be parsed.

```
rapper: Parsing URI file:///Users/adamsm/go/src/github.com/GSS-Cogs/GDP-vocabs/vocabs/reference-geography.ttl with parser turtle
rapper: Parsing returned 16106 triples
```

To finish, commit the updated `vocabs/reference-geography.ttl` file and push the repo back to github.
