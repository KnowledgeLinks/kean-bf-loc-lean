import org.marc4j.*
import java.io.FileInputStream

val kean_marc = FileInputStream(args[0])
val reader = MarcStreamReader(kean_marc)
var count = 0 
println("Sharding Kean Records")
while (true) {
    reader.next()
    count += 1
    if(count%100 == 0 && count > 1) {
        print(".")
    }
    if(count%1000 == 0) {
        print(count)
    }
}
println("Total Kean $count")
