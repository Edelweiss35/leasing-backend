#! /usr/bin/python3
# -*- coding: utf-8 -*-

from leasingai.preprocessor.LegalPositionPreprocessor import LegalPositionPreprocessor
from leasingai.preprocessor.XMLtoJSONpreprocessor import BboxXMLParser
from leasingai.preprocessor.PDFtoXMLpreprocessor import PDFtoXML
from leasingai.reducer.clause_content_reducer import ClauseContentReducer
import json


def execute_NLP_backend(document_id, legal_position_id):
    ptx = PDFtoXML(document_id)
    bxp = BboxXMLParser(ptx)
    lpp = LegalPositionPreprocessor(legal_position_id)
    ccr = ClauseContentReducer(lpp, bxp)

    # write output to log files for testing purpose
    
    with open("/home/naresh/temp.json", 'w') as file:
        file.write(json.dumps(bxp.get_JSON()))
    with open("/home/naresh/temp2.json", 'w') as file:
        file.write(json.dumps(ccr.get_JSON()[0]))
    with open("/home/naresh/temp3.json", 'w') as file:
        file.write(json.dumps(ccr.get_JSON()[1]))
    with open("/home/naresh/temp4.json", 'w') as file:
        file.write(json.dumps(ccr.get_JSON()[2]))
    return json.dumps(ccr.get_JSON()[2])
