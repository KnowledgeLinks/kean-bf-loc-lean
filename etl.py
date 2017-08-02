__author__ = "Jeremy Nelson"

import datetime
import gzip
import logging
import sys

import pymarc
import rdflib

import lxml.etree
import bibcat.rml.processor as processor
import bibcat

logging.getLogger('rdflib').setLevel(logging.CRITICAL)

LOC_TRANSFORM = lxml.etree.XSLT(
    lxml.etree.parse("E:/2017/marc2bibframe2/xsl/marc2bibframe2.xsl"))

def process_marc(marc_filename):
    marc_reader = pymarc.MARCReader(open(marc_filename, 'rb'), 
        to_unicode=True,
        utf8_handling='ignore')
    count = 0
    start = datetime.datetime.utcnow()
    print("Start {}".format(start))
    loc2lean = processor.SPARQLProcessor(
        rml_rules=['bibcat-loc-bf-to-lean-bf.ttl'])
    lean_graph, loc_graph = None, None
    while 1:
        try:
            if count == 100:
                with open("E:/2017/Kean-LOC/data/first-100-lean.ttl" , "wb+") as fo:
                    fo.write(lean_graph.serialize(format='turtle'))
                with open("E:/2017/Kean-LOC/data/first-100-loc.xml", "wb+") as fo:
                    fo.write(loc_graph.serialize(format='xml'))
            if not count%100 and count > 0:
                print(".", end="")
            if not count%1000:
                print("{:,}".format(count), end="")
            if not count%5000 and count > 0:
                start = count-5000
                bibcat.clean_uris(lean_graph)
                with open("E:/2017/Kean-LOC/data/bf-lean-{}-{}.ttl".format(start, count), "wb+") as lean_fo:
                    lean_fo.write(lean_graph.serialize(format='turtle'))
                lean_graph = None
                with gzip.open("E:/2017/Kean-LOC/data/bf-loc-{}-{}-xml.gz".format(start, count), "wb+") as loc_fo:
                    loc_fo.write(loc_graph.serialize())
                loc_graph = None
            count += 1    
            rec = next(marc_reader)
            loc_bf_xml = LOC_TRANSFORM(lxml.etree.XML(pymarc.record_to_xml(rec, namespace=True)),
                baseuri="'http://library.kean.edu/'")
            loc_bf = rdflib.Graph()
            loc_bf.parse(data=loc_bf_xml, format='xml')
            loc2lean.triplestore = loc_bf
            loc2lean.run()
            bibcat.clean_uris(loc2lean.output)
            if loc_graph is None:
                loc_graph = loc_bf
                lean_graph = loc2lean.output
            else:
                loc_graph += loc_bf
                lean_graph += loc2lean.output
        except StopIteration:
            with open("E:/2017/Kean-LOC/data/bf-lean-final-{}.ttl".format(count), "wb+") as lean_fo:
                lean_fo.write(lean_graph.serialize(format='turtle'))
            with gzip.open("E:/2017/Kean-LOC/data/bf-loc-final-{}-xml.gz".format(count), "wb+") as loc_fo:
                loc_fo.write(loc_graph.serialize())
            break
        except:
            print(sys.exc_info()[-1], end="\t")
            print("E{:,}".format(count), end="")
            count += 1
            with open("E:/2017/Kean-LOC/data/errors.mrc", "wb+") as fo:
                fo.write(rec.as_marc21())
    end = datetime.datetime.utcnow()
    print("{} for total time {} mins, count is {:,}".format(end,
        (end-start).seconds / 60.0,
        count))   
            
        

if __name__ == '__main__':
   process_marc("E:/2017/tmp/marc_export")
