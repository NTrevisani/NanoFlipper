#!/bin/env python
import ROOT
from array import array
import sys

if len(sys.argv) < 3:
    print("Syntax: haddnano.py out.root input1.root input2.root ...")
    exit

ofname = sys.argv[1]
files = sys.argv[2:]

print("ofname: {}".format(ofname)) 
print("files:  {}".format(files)) 

# def zeroFill(tree, brName, brObj):
#     if brObj.GetLeaf(brName).GetTypeName() != "Bool_t":
#         print("Did not expect to back fill non-boolean branches",
#               tree, brName, brObj.GetLeaf(br).GetTypeName())
#     else:
#         buff = array('B', [0])
#         b = tree.Branch(brName, buff, brName+"/O")
#         # be sure we do not trigger flushing
#         b.SetBasketSize(tree.GetEntries()*2)
#         for x in range(0, tree.GetEntries()):
#             b.Fill()
#         b.ResetAddress()


fileHandles = []
goFast = True

print("Starting")

for fn in files:
    print("Adding file", fn)
    fileHandles.append(ROOT.TFile.Open(fn))
    if fileHandles[-1].GetCompressionSettings() != fileHandles[0].GetCompressionSettings():
        goFast = False
        print("Disabling fast merging as inputs have different compressions")
of = ROOT.TFile(ofname, "recreate")
if goFast:
    of.SetCompressionSettings(fileHandles[0].GetCompressionSettings())
of.cd()

for e in fileHandles[0].GetListOfKeys():
    name = e.GetName()
    print("Merging", name)
    obj = e.ReadObj()
    cl = ROOT.TClass.GetClass(e.GetClassName())
    inputs = ROOT.TList()
    isTree = obj.IsA().InheritsFrom(ROOT.TTree.Class())
    if isTree:
        obj = obj.CloneTree(-1, "fast" if goFast else "")
        branchNames = set([x.GetName() for x in obj.GetListOfBranches()])
    for fh in fileHandles[1:]:

        # Let's merge only TTree objects
        # Due to some errors in ntuple production, 
        # some files may contain also TH1F or TH2F objects.
        # Since no ALL files contain them, it may produce errors.
        if isTree:
            #print("fh: {}".format(fh))
            otherObj = fh.GetListOfKeys().FindObject(name).ReadObj()
            #print("Object name: {}".format(name))
            #print("Find object by name: {}".format(fh.GetListOfKeys().FindObject(name)))
            #print("otherObj: {}".format(otherObj))
            inputs.Add(otherObj)

        if isTree and obj.GetName() == 'Events':
            otherObj.SetAutoFlush(0)
            otherBranches = set([x.GetName()
                                 for x in otherObj.GetListOfBranches()])
            missingBranches = list(branchNames-otherBranches)
            additionalBranches = list(otherBranches-branchNames)
            print("missing:", missingBranches,
                  "\n Additional:", additionalBranches)
            for br in missingBranches:
                # fill "Other"
                zeroFill(otherObj, br, obj.GetListOfBranches().FindObject(br))
            for br in additionalBranches:
                # fill main
                branchNames.add(br)
                zeroFill(obj, br, otherObj.GetListOfBranches().FindObject(br))
            # merge immediately for trees
        if isTree:
            obj.Merge(inputs, "fast" if goFast else "")
            inputs.Clear()

    if isTree:
        obj.Write()
    elif obj.IsA().InheritsFrom(ROOT.TH1.Class()):
        obj.Merge(inputs)
        obj.Write()
    elif obj.IsA().InheritsFrom(ROOT.TObjString.Class()):
        for st in inputs:
            if st.GetString() != obj.GetString():
                print("Strings are not matching")
        obj.Write()
    else:
        print("Cannot handle ", obj.IsA().GetName())
