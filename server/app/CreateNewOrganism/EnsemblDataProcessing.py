import pandas as pd

import traceback

'''
FH   Key             Location/Qualifiers
FT   source          1..130694993
FT                   /organism="Mus musculus"
FT                   /db_xref="taxon:10090"
FT   gene            3119841..3129546
FT                   /gene=ENSMUSG00000071434
FT                   /locus_tag="9230019H11Rik"
FT                   /note="RIKEN cDNA 9230019H11 gene [Source:MGI
FT                   Symbol;Acc:MGI:3588256]"
FT   mRNA            join(3119841..3119898,3120176..3120296,3125002..3125271,
FT                   3125608..3125874,3126453..3126581,3127591..3129546)
FT                   /gene="ENSMUSG00000071434"
FT                   /note="transcript_id=ENSMUST00000095874"
FT   CDS             join(3120206..3120296,3125002..3125271,3125608..3125874,
FT                   3126453..3126559)
FT                   /gene="ENSMUSG00000071434"
FT                   /protein_id="ENSMUSP00000093559"
FT                   /note="transcript_id=ENSMUST00000095874"
FT                   /db_xref="Uniprot/SPTREMBL:Q3UW27"
FT                   /db_xref="Fantom:9230019H11"
FT                   /db_xref="EMBL:AC131283"
FT                   /db_xref="EMBL:AC168222"
FT                   /db_xref="EMBL:AK136660"
FT                   /db_xref="GO:GO:0001913"
FT                   /db_xref="GO:GO:0002474"
FT                   /db_xref="GO:GO:0005886"
FT                   /db_xref="GO:GO:0042267"
FT                   /db_xref="GO:GO:0042605"
FT                   /db_xref="GO:GO:0046703"
FT                   /db_xref="MGI_trans_name:9230019H11Rik-201"
FT                   /db_xref="goslim_goa:GO:0002376"
FT                   /db_xref="goslim_goa:GO:0003674"
FT                   /db_xref="goslim_goa:GO:0005575"
FT                   /db_xref="goslim_goa:GO:0005623"
FT                   /db_xref="goslim_goa:GO:0005886"
FT                   /db_xref="goslim_goa:GO:0006950"
FT                   /db_xref="goslim_goa:GO:0008150"
FT                   /db_xref="protein_id:BAE23092.1"
FT                   /db_xref="Reactome:REACT_300990"
FT                   /db_xref="Reactome:REACT_326389"
FT                   /db_xref="Reactome:REACT_345792"
FT                   /db_xref="UniParc:UPI00005ABCEA"
FT                   /translation="MTKAADTKHHHSMIQRLLILLSCGYTKLLAQSPTLCCSFDVNNTF
FT                   NDNVTSGLWNYEVQGEVKTVPFILNRNNKCHVTSDFENRLNATEICEKQLHSLQGQVYH
FT                   FQDVLLQMRGENNTIREPLTLQSIVCGWYADERFMGSWKVCLNGSKIFHGDIKRWLHIY
FT                   SGTNWTEEILEKIKNLNDFLNRTSQGEFKNKFKEYNLHCKENQEPTALSTTADVGRPSS
FT                   RACTSNPSVLLIMLSCFLLYVF


FT   gene            complement(130557348..130557464)
FT                   /gene=ENSMUSG00000096766
FT                   /locus_tag="Gm23793"
FT                   /note="predicted gene, 23793 [Source:MGI
FT                   Symbol;Acc:MGI:5453570]"
FT   misc_RNA        complement(130557348..130557464)
FT                   /gene="ENSMUSG00000096766"
FT                   /db_xref="MGI_trans_name:Gm23793-201"
FT                   /db_xref="RNACentral:URS0000660DEE"
FT                   /note="snRNA"
FT                   /note="transcript_id=ENSMUST00000179396"

'''


## return [ [geneGID, mRNATID, CDSPID, geneName, TransName, [uniprotRefList], [goRefList]] ]
def readAnnotation(infile):
    try:

        fp = open(infile)
        lines = fp.readlines()
        fp.close()

        prioKeyType = ''  # gene
        geneGID = ''  # /gene=ENSMUSG00000071434

        geneName = ''  # /locus_tag="9230019H11Rik"

        mRNATID = ''  # /note="transcript_id=ENSMUST00000095874"

        CDSPID = ''  # /protein_id="ENSMUSP00000093559"

        TransName = ''  # /db_xref="MGI_trans_name:9230019H11Rik-201"

        goRefList = []
        uniprotRefList = []
        contentLList = []
        for line in lines:
            if line[0:2] != 'FT':
                continue

            lineList = line.split()

            if len(lineList) == 3 and lineList[1] != 'CDS':
                if prioKeyType == 'CDS':
                    prioKeyType = ''
                    contentListTemp = []
                    contentListTemp.append(geneGID)
                    contentListTemp.append(mRNATID)
                    contentListTemp.append(CDSPID)
                    contentListTemp.append(geneName)
                    contentListTemp.append(TransName)
                    contentListTemp.append(uniprotRefList)
                    goRefList = list(set(goRefList))
                    contentListTemp.append(goRefList)

                    contentLList.append(contentListTemp)

                    TransName = ''
                    uniprotRefList = []
                    goRefList = []

            if len(lineList) == 3 and (lineList[1] == 'gene' or lineList[1] == 'CDS'):
                prioKeyType = lineList[1]
                continue

            if len(lineList) == 2 and prioKeyType == 'gene':
                # /locus_tag="9230019H11Rik"
                if lineList[1].find('/locus_tag=') != -1:
                    geneName = readSubline(lineList[1], '"', '"')


            # [geneGID, mRNATID, CDSPID, TransName, [uniprotRefList], [goRefList]]
            elif len(lineList) == 2 and prioKeyType == 'CDS':

                # /gene="ENSMUSG00000071434"
                if lineList[1].find('/gene=') != -1:
                    geneGID = readSubline(lineList[1], '"', '"')

                # /note="transcript_id=ENSMUST00000095874"
                elif lineList[1].find('/note="transcript_id=') != -1:
                    mRNATID = readSubline(lineList[1], '=')
                    mRNATID = readSubline(mRNATID, '=', '"')

                # /protein_id="ENSMUSP00000093559"
                elif lineList[1].find('/protein_id="') != -1:
                    CDSPID = readSubline(lineList[1], '"', '"')

                # geneName = FO538757.2  <---  /locus_tag="FO538757.2"
                # /db_xref="Clone_based_ensembl_transcript:FO538757.2-201"
                elif lineList[1].find(geneName + '-') != -1:
                    TransNameTail = readSubline(lineList[1], geneName, '"')
                    TransName = geneName + TransNameTail

                ##/db_xref="MGI_trans_name:9230019H11Rik-201"
                # elif lineList[1].find('/db_xref="MGI_trans_name:') != -1:
                #	TransName = readSubline(lineList[1], ':', '"')
                #	geneName = TransName.split('-')[0]


                # /db_xref="Uniprot/SWISSPROT:Q8R4S0"
                # /db_xref="Uniprot/SPTREMBL:Q3UX37"
                elif lineList[1].find('/db_xref="Uniprot/') != -1:
                    uniprotRef = readSubline(lineList[1], ':', '"')
                    uniprotRefList.append(uniprotRef)


                # /db_xref="GO:GO:0046703"
                # /db_xref="goslim_goa:GO:0002376"
                elif lineList[1].find('/db_xref="GO:') != -1:
                    goRef = readSubline(lineList[1], ':', '"')
                    goRefList.append(goRef)

        return contentLList



    except Exception, e:
        print "error in readAnnotation."
        traceback.print_exc()
        print e
