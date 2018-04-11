import pandas as pd

import traceback



def transcript_fa_Phyto(file_path):
    # transcript/cDNA


    filename = file_path
    # handling of cDNASequence table
    try:
        fileHandle = open(filename)

    except Exception, e:
        fileHandle = None
        filename = filename + "sta"
        pass

    try:

        fileHandle = open(filename)
        lines = fileHandle.readlines()
        fileHandle.close()

        print "Analyzing file %s..." % filename

        cDNASequence = []
        cDNASequenceTemp = []
        tempStr = ""

        for line in lines:
            if line[0] == '>':
                if tempStr != "":
                    cDNASequenceTemp.append(tempStr)

                    GeneID = cDNASequenceTemp[0]
                    sequence_lenght = len(cDNASequenceTemp[1])
                    sequence = cDNASequenceTemp[1]

                    cDNASequence.append({'GeneID': GeneID, 'length': sequence_lenght, 'Sequence': sequence})
                    tempStr = ""
                    cDNASequenceTemp = []

                geneID = line[1:].split(' ')[0]
                cDNASequenceTemp.append(geneID)
            else:
                tempStr += line[0:len(line) - 1]

        cDNASequence_df = pd.DataFrame(cDNASequence)
        return {'error': None, 'cDNASequence': cDNASequence_df}

    except Exception, e:
        print e
        return {'error': e};


def peptide_fa_Phyto(file_path):

    filename = file_path
    try:

        fileHandle = open(filename)
        lines = fileHandle.readlines()
        fileHandle.close()

        print "Analyzing file %s..." % filename

        PeptideSequence = []
        PeptideSequenceTemp = []
        tempStr = ""

        for line in lines:
            if line[0] == '>':
                if tempStr != "":
                    PeptideSequenceTemp.append(tempStr)

                    GeneID = PeptideSequenceTemp[0]
                    sequence_lenght = len(PeptideSequenceTemp[1])
                    sequence = PeptideSequenceTemp[1]

                    PeptideSequence.append({'GeneID': GeneID, 'length': sequence_lenght, 'Sequence': sequence})

                    tempStr = ""
                    PeptideSequenceTemp = []


                geneID = line[1:].split(' ')[0]
                PeptideSequenceTemp.append(geneID)
            else:
                tempStr += line[0:len(line) - 1]

        PeptideSequence_df = pd.DataFrame(PeptideSequence)

        return {'error': None, 'PeptideSequence': PeptideSequence_df}

    except Exception, e:
        traceback.print_exc()
        print e
        return {'error': e};


def cds_fa_Phyto(file_path):

    filename = file_path

    try:

        fileHandle = open(filename)
        lines = fileHandle.readlines()
        fileHandle.close()

        print "Analyzing file %s..." % filename

        CDSSequence = []
        CDSSequenceTemp = []
        tempStr = ""

        for line in lines:
            if line[0] == '>':
                if tempStr != "":
                    CDSSequenceTemp.append(tempStr)

                    GeneID = CDSSequenceTemp[0]
                    sequence_lenght = len(CDSSequenceTemp[1])
                    sequence = CDSSequenceTemp[1]

                    CDSSequence.append({'GeneID': GeneID, 'length': sequence_lenght, 'Sequence': sequence})

                    tempStr = ""
                    CDSSequenceTemp = []

                geneID = line[1:].split(' ')[0]
                CDSSequenceTemp.append(geneID)

            else:
                tempStr += line[0:len(line) - 1]

        CDSSequence_df = pd.DataFrame(CDSSequence)
        return {'error': None, 'CDSSequence': CDSSequence_df}

    except Exception, e:
        traceback.print_exc()
        print e
        return {'error': e};



def gene_gff3_Phyto(file_path):


    filename = file_path
    # handling of ChromosomalPosition table
    try:
        fileHandle = open(filename)
        lines = fileHandle.readlines()
        fileHandle.close()

        print "Analyzing file %s..." % filename

        ChromosomalPosition = []
        geneIDtemp, pacIDtemp = "", ""
        for line in lines:
            if line[0:2] != "##":
                lineList = line.split('	')
                if lineList[2] != "gene":
                    ChromosomalPositionTemp = []
                    ChromosomalPositionTemp.append(lineList[0])
                    if lineList[2] == "five_prime_UTR":
                        ChromosomalPositionTemp.append(r"5`-UTR")
                    elif lineList[2] == "three_prime_UTR":
                        ChromosomalPositionTemp.append(r"3`-UTR")
                    else:
                        ChromosomalPositionTemp.append(lineList[2])
                    ChromosomalPositionTemp.extend(lineList[3:5])
                    ChromosomalPositionTemp.append(lineList[6])
                    if lineList[2] == "mRNA":
                        attributeList = lineList[8].split(';')
                        geneIDtemp = attributeList[1].split('=')[1]
                        pacIDtemp = attributeList[2].split('=')[1]
                    ChromosomalPositionTemp.append(geneIDtemp)
                    ChromosomalPositionTemp.append(pacIDtemp)
                    ChromosomalPositionTemp.extend(['N/A', 'protein_coding_gene'])

                    ChromosomalPosition.append(ChromosomalPositionTemp)

        print "Importing to ChromosomalPosition and SearchTableID table..."
        tempGeneFlag = "temp"

        ChromosomalPosition_list = []
        SearchTableID_list = []

        for singleCPArray in ChromosomalPosition:
            ChromosomalPosition_list.append({'Chromosome': singleCPArray[0], 'Category': singleCPArray[1], \
                                             'geneType': singleCPArray[1], 'Start': int(singleCPArray[2]), \
                                             'End': int(singleCPArray[3]), 'Strand':singleCPArray[4], \
                                             'GeneID':singleCPArray[5], 'PACID':singleCPArray[6], \
                                             'LetterCode':singleCPArray[7], 'Note':singleCPArray[8]})

            if singleCPArray[5] != tempGeneFlag:
                SearchTableID_list.append({'GeneID': singleCPArray[5], 'Chromosome': singleCPArray[0]})
                tempGeneFlag = singleCPArray[5]

        ChromosomalPosition_df = pd.DataFrame(ChromosomalPosition_list)
        SearchTableID_df = pd.DataFrame(SearchTableID_list)
        return {'error': None, 'ChromosomalPosition': ChromosomalPosition_df, 'SearchTableID':SearchTableID_df}

    except Exception, e:
        traceback.print_exc()
        print e
        return {'error': e};

def annotation_info_Phyto(file_path):
    filename = file_path

    # handling of KOG,Panther,Pfam tables
    try:
        fileHandle = open(filename)
        lines = fileHandle.readlines()
        fileHandle.close()

        print "Analyzing file %s..." % filename

        geneDic = {}
        tmpGene = ''

        protein_annotation_list = []
        for line in lines:

            if line[0] == '#':
                continue

            line = line.strip('\n')
            lineList = line.split('\t')
            if len(lineList) < 3:
                pass
            if lineList[0] == "" and lineList[1] == "" and lineList[2] == "":
                pass
            else:

                tempDic = {}
                for word in lineList:
                    if word.startswith('KOG'):
                        tempDic['KOG'] = {'KOGID': word.replace(',', '|'), 'KOGName': "N/A"}
                    if word.startswith('PTHR'):
                        tempDic['Panther'] = {'PantherID': word.replace(',', '|'), 'PantherName': "N/A"}
                    if word.startswith('PF'):
                        tempDic['Pfam'] = {'PfamDomainID': word.replace(',', '|'), 'PfamDomainName': "N/A"}
                if lineList[0][:1].isdigit():
                    geneDic[lineList[2]] = tempDic
                    tmpGene = lineList[2]
                else:
                    geneDic[lineList[0]] = tempDic
                    tmpGene = lineList[0]

                if lineList[len(lineList) - 1] != '':
                    # GeneID, Annotation
                    protein_annotation_list.append({ 'GeneID':tmpGene, 'Annotation':lineList[len(lineList) - 1] })
                else:
                    protein_annotation_list.append({'GeneID': tmpGene, 'Annotation': 'N/A' })

        KOG_list = []
        Panther_list = []
        Pfam_list = []
        for gene in geneDic:
            tempDic = geneDic[gene]
            if 'KOG' in tempDic:
                KOG = tempDic['KOG']
                if KOG['KOGID'] != "":
                    # GeneID, GeneID_FG, KOGID, KOGName
                    KOG_list.append({ 'GeneID':gene, 'GeneID_FG':'N/A', 'KOGID':KOG['KOGID'], 'KOGName':KOG['KOGName'] })
            else:
                KOG_list.append({'GeneID': gene, 'GeneID_FG': 'N/A', 'KOGID': 'N/A', 'KOGName': 'N/A'})

            if 'Panther' in tempDic:
                Panther = tempDic['Panther']
                if Panther['PantherID'] != "":
                    # GeneID, GeneID_FG, PantherID, PantherName
                    Panther_list.append({'GeneID': gene, 'GeneID_FG': 'N/A', 'PantherID': Panther['PantherID'], 'PantherName': Panther['PantherName']} )

            else:
                Panther_list.append( {'GeneID': gene, 'GeneID_FG': 'N/A', 'PantherID': 'N/A', 'PantherName': 'N/A'} )

            if 'Pfam' in tempDic:
                Pfam = tempDic['Pfam']
                if Pfam['PfamDomainID'] != "":
                    # GeneID, GeneID_FG, PfamDomainID, PfamDomainName
                    Pfam_list.append({'GeneID': gene, 'GeneID_FG': 'N/A', 'PfamDomainID': Pfam['PfamDomainID'], 'PfamDomainName': Pfam['PfamDomainName']})
            else:
                Pfam_list.append({'GeneID': gene, 'GeneID_FG': 'N/A', 'PfamDomainID': 'N/A', 'PfamDomainName': 'N/A'})

        protein_annotation_df = pd.DataFrame(protein_annotation_list)
        KOG_df = pd.DataFrame(KOG_list)
        Panther_df = pd.DataFrame(Panther_list)
        Pfam_df = pd.DataFrame(Pfam_list)
        return {'error':None, 'protein':protein_annotation_df, 'KOG':KOG_df, 'Panther':Panther_df, 'Pfam':Pfam_df}

    except Exception, e:
        print e
        return {'error':e};