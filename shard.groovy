def marc4j = new File("/Users/jeremynelson/2017/kean-bf-loc-lean/marc4j-2.6.4.jar");
this.class.classLoader.rootLoader.addURL(marc4j.toURI().toURL());

import org.marc4j.*
raw_marc  = new File("/Users/jeremynelson/2017/kean-bf-loc-lean/marc.bib").newInputStream()
reader = new MarcStreamReader(raw_marc)
counter = 0
while(reader.hasNext()) {
    counter += 1
}

println "Starting Shard Class"
println "Total size of file " + counter