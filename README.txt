#README

1. Open a Linux-based OS terminal;

2. Install python if necessary;

3. Run the following command: python parse.py <filename> (filename without .xml);

4. This solution outputs 4 parsed files:
    - xmlOutputWithoutEmptyTags: empty tags removed from xml;
    - xmlOutputWithMergedStrings: consecutive strings that do not end in sentence-ending punctuation are merged;
    - xmlOutputWithSectionsAndClauses: the xml is divided in sections and clauses;
    - xmlOutputFinal: the structure of the xml is corrected to fit the final one (body and html replaced by document,
      tabs and new lines adjusted)
