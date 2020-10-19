# read data return as dictionary
# parameter
DATA_FILE = "./data/testdata.txt"
OUTPUT_FILE = "./data/output.txt"
SAVE_FILE = "./data/savedata.txt"


def graph_reader():
    nodeDict={}
    with open (DATA_FILE) as f:
        key = ""
        nodeDict.update (key)
        y=[]
        for line in f:
            x = line.split()
            if x[0]=="#":
                continue
            if (x[0] == key):
                #print (x[1], end =" ")
                #print (y)
                y.append(x[1])
            else:
                key = x[0]
                y = ["0"]
                y.append(x[1])
                #print ("")
                #print ("KEY:" + x[0]+ " "+ x[1], end =" ")
            nodeDict.update({key:y})
        print (" ")
    #print (nodeDict)
    return nodeDict



# write dictionary to a txt file
def file_saver():
    data = graph_reader()
    with open (SAVE_FILE, "w") as f:
        for item in data:
            print (item+"    ")
            


#save dictionary back to graph file
def graph_writer():
    with open (OUTPUT_FILE, "w") as f: 
        d=graph_reader()
        #{"b":[1,2,3,4,5],"c":[4,5],"d":[2,3]}
        for a in d:
            #print (a,end = " ")
            for l in d[a]:
                print (a + "    "+ str(l))
                f.write(a + "    "+ str(l)+"\n")
            print ("")
graph_writer()
file_saver()