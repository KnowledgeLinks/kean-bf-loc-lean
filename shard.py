import pymarc

reader = pymarc.MARCReader(open("marc.bib", "rb"), to_unicode=True)
count = 0
while 1:
    try:
        rec = next(reader)
   
    except StopIteration:
        break
    except:
        pass
    if not count%100 and count > 0:
        print(".", end="")
    if not count%1000:
        print("{:,}".format(count), end="")
    count += 1
print("Total count " + count)
