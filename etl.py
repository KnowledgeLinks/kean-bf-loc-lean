__author__ = "Jeremy Nelson"

import gzip
import pymarc
import rdflib

import lxml.etree as etree
import bibcat.rml.processor as processor

LOC_TRANSFORM = lxml.etree.XSLT(lxml.etree.parse("~/2017/marc2bibframe2/xsl/marc2bibframe2.xsl"))

def process_marc(marc_filename):
    marc_reader = pymarc.MARCReader(open(marc_filename, 'rb'), 
        to_unicode=True,
        utf_handling='ignore')
    count = 0
    loc2lean = processor.SPARQLProcessor(
        rml_rules=['bibcat-loc-bf-to-lean-bf.ttl'])
    lean_graph, loc_graph = None, None
    while 1:
        try:
            rec = next(marc_reader)
            loc_bf_xml = LOC_TRANSFORM(etree.XML(pymarc.record_to_xml(rec, namespace=True)),
                base_uri="'http://library.kean/edu/'")
            loc_bf = rdflib.Graph()
            loc_bf.parse(data=loc_bf_xml, format='xml')
            loc2lean.triplestore = loc_bf
            loc2lean.run()
            if loc_graph is None:
                loc_graph = loc_bf
                lean_graph = loc2lean.output
            else:
                loc_graph += loc_bf
                lean_graph += loc2lean.output
            if not count%100 and count > 0:
                print(".", end="")
            if not count%1000:
                print("{:,}".format(count), end="")
            if not count%5000 and count > 0:
                start = count-5000
                with open("data/bf-lean-{}-{}.ttl".format(start, count), "wb") as lean_fo:
                    lean_fo.write(lean_graph.serialize(format='turtle'))
                lean_graph = None
                with gzip.open("data/bf-loc-{}-{}-xml.gz".format(start, count) "wb") as loc_fo:
                    loc_fo.write(loc_graph.serialize())
                loc_graph = None
            count += 1    
        except StopIteration:
            break
        except:
            print("E{:,}".format(count), end="")
            
            
        

if __name__ == '__main__':
    pass
