import sys

filename=str(sys.argv[1])[0:len(str(sys.argv[1]))-4]

f = open(filename+".xml", "r")
parser_string = f.read()

i=0

#search for every tag initiator (<)
while parser_string.find("<",i)!=-1:
    first_index = parser_string.find("<",i)
    #check if it is an opening  (the next char can't be '/')
    if parser_string[first_index+1]!='/':
        #find the tag terminator
        second_index = parser_string.find(">", first_index+1)
        #find the closing tag (must have "</"+tag_name+">")
        third_index = parser_string.find("</" + parser_string[first_index+1:second_index] + ">",second_index+1)
        #check if the string between the opening and closing tags are empty or only have spaces/tabs/endlines
        if parser_string[second_index+1:third_index].isspace() or parser_string[second_index+1:third_index] == "":
            #find end of the closing tag
            forth_index = parser_string.find(">", third_index+1)
            #create a new final parser without the opening tag, closing tag and spaces/tags/endlines between those
            final_string = parser_string[0:first_index]+parser_string[forth_index+1:len(parser_string)]
            parser_string = final_string
            #since the content has been removed, the next position to search should be the one of
            #the opening tag initiator that no longer exists
            i = first_index
        else:
            # go to the next tag
            i = first_index+1
    else:
        #go to the next tag
        i=first_index+1

f2 = open(filename + "OutputWithoutEmptyTags.xml", "w")
f2.write(parser_string)

f.close()
f2.close()

f = open(filename + "OutputWithoutEmptyTags.xml", "r")

parser_string = f.read()

i=0

#search for every heading opening tag (<h1>)
while parser_string.find("<h1>",i)!=-1:
    j = parser_string.find("<h1>",i)
    #search for every tag initiator that does not belong to a heading opening tag
    while parser_string[parser_string.find("<",j+1)+1]!='h' and parser_string.find("<",j+1)!=-1:
        first_index = parser_string.find("<",j+1)
        #check if it is an opening  (the next char can't be '/')
        if parser_string[first_index+1]!='/':
            #find the tag terminator
            second_index = parser_string.find(">", first_index+1)
            #store this tag terminator index to be able to merge strings at the end of each merge process
            second_index1 = second_index
            #find the closing tag (must have "</"+tag_name+">")
            third_index = parser_string.find("</" + parser_string[first_index+1:second_index] + ">",second_index+1)
            #initiate the string that merges consecutive strings that do not end with sentence-ending ponctuation
            merged_string = ""
            #search for consecutive strings that do not end with sentence-ending ponctuation
            while parser_string[third_index-1]!="." and parser_string[third_index-1]!="?" and parser_string[third_index-1]!="!" and parser_string[third_index-1]!=":":
                #merge the current merged string with the newly found string that does not end with sentence-ending ponctuation
                merged_string = merged_string + parser_string[second_index+1:third_index] + " "
                #find the next tag initiator that belongs to a tag that may contain a string that does not end with sentence-ending ponctuation
                first_index = parser_string.find("<",third_index+2)
                #find the next tag terminator
                second_index = parser_string.find(">", first_index+1)
                #find the closing tag (must have "</"+tag_name+">")
                third_index = parser_string.find("</" + parser_string[first_index+1:second_index] + ">",second_index+1)
            if merged_string!="":
                #create a new final parser by merging: the current parser until the opening tag of the
                #first string that does not end with sentence-ending ponctuation + the merged string containing strings that do not
                #end with sentence-ending ponctuation + the current parser from the begining of the first string that ends with
                #sentence-ending ponctuation until the end of the parser
                final_string = parser_string[0:second_index1+1] + merged_string + parser_string[second_index+1:len(parser_string)]
                parser_string = final_string
                #the next positiong to be searched in the new parser is the one after the tag terminator of the string that ends with sentence-ending ponctuation
                j = second_index1+1 + len(merged_string) + len(parser_string[second_index+1:third_index])
            else:
                #go to the next tag
                j = first_index+1
        else:
            #go to the next tag
            j = first_index+1
    #go to the next heading
    i = j

f2 = open(filename + "OutputWithMergedStrings.xml", "w")
f2.write(parser_string)

f.close()
f2.close()

f = open(filename + "OutputWithMergedStrings.xml", "r")

parser_string = f.read()

i=0

#search for every heading opening tag (<h1>)
while parser_string.find("<h1>",i)!=-1:
    j = parser_string.find("<h1>",i)
    #find the closing tag initiator
    first_index = parser_string.find("<",j+1)
    #create a new final parser with the new format
    final_string = parser_string[0:j] + "<section title=\"" + parser_string[j+4:first_index] + "\"" + parser_string[first_index+4:len(parser_string)]
    parser_string = final_string
    #search for consecutive tags that are not headers
    while parser_string[parser_string.find("<",j+1)+1]!='h' and parser_string.find("<",j+1)!=-1:
        first_index = parser_string.find("<",j+1)
        #check if it is an opening  (the next char can't be '/')
        if parser_string[first_index+1]!='/':
            #find the tag terminator
            second_index = parser_string.find(">", first_index+1)
            #find the closing tag (must have "</"+tag_name+">")
            third_index = parser_string.find("</" + parser_string[first_index+1:second_index] + ">",second_index+1)
            #store the tag name for further elimination
            tag_holder = parser_string[first_index+1:second_index]
            #find the closing tag terminator
            fourth_index = parser_string.find(">", third_index+1)
            #create a final parser by replacing the previous tag name by "clause"
            final_string = parser_string[0:first_index+1] + "clause" + parser_string[second_index:third_index+2] + "clause" + parser_string[fourth_index:len(parser_string)]
            parser_string = final_string
        #go to the next tag
        j = first_index + 1
    #create a final string by introducing the section closing tag. Since the length of the final parser has been changed,
    #proper shifts had to me made
    final_string = parser_string[0:fourth_index+2*len("clause")-2*len(tag_holder) + 1] + "\n</section>" + parser_string[fourth_index+2*len("clause")-2*len(tag_holder) + 1:len(parser_string)]
    parser_string = final_string
    #go to the next heading
    i = j

f2 = open(filename + "OutputWithSectionsAndClauses.xml", "w")
f2.write(parser_string)

f.close()
f2.close()


f = open(filename + "OutputWithSectionsAndClauses.xml", "r")
parser_string = f.read()

#create a new final parser
final_string = "<document>\n"

i=0

#search for every section opening tag (<section)
while parser_string.find("<section",i)!=-1:
    first_index = parser_string.find("<section",i)
    #find the opening tag terminator (>)
    second_index = parser_string.find(">", first_index+1)
    #update the final parser by adding the found header
    final_string = final_string + "\t" + parser_string[first_index:second_index+1] + "\n"
    j = first_index
    #search for consecutive clauses
    while parser_string[parser_string.find("<",j+1)+2:parser_string.find("<",j+1)+9]!="section" and parser_string.find("<",j+1)!=-1:
        second_index = parser_string.find("<",j+1)
        #check if it is an opening  (the next char can't be '/')
        if parser_string[second_index+1]!='/':
            #find the tag terminator
            third_index = parser_string.find(">", second_index+1)
            #find the closing tag (must have "</"+tag_name+">")
            forth_index = parser_string.find("</" + parser_string[second_index+1:third_index] + ">",third_index+1)
            #update the final string by adding the found clause
            final_string = final_string + "\t\t" + parser_string[second_index:forth_index] + "</clause>\n"
        #go to the next clause
        j = second_index+1
    #add section closing tag
    final_string = final_string + "\t</section>\n"
    #go to the next section
    i = first_index+1

#add the document terminator
final_string = final_string + "</document>"

f2 = open(filename + "OutputFinal.xml", "w")
f2.write(final_string)

f.close()
f2.close()
