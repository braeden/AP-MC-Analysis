import re
import os
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader

d = {}

def getPDFPage(filename, pageNum):
    filename = '/home/braeden/Documents/Python/APanalysis/'+filename+'.pdf'
    fp = open(filename)
    pdfFile = PdfFileReader(fp)

    if pdfFile.isEncrypted:
        try:
            pdfFile.decrypt('')
            print 'File Decrypted (PyPDF2)'
        except:
            command="cp "+filename+" temp.pdf; qpdf --password='' --decrypt temp.pdf "+filename
            os.system(command)
            print 'File Decrypted (qpdf)'
            #re-open the decrypted file
            fp = open(filename)
            pdfFile = PdfFileReader(fp)
    else:
        print 'File Not Encrypted'
    print(filename)
    print(pdfFile.numPages)
    page = pdfFile.getPage(int(pageNum))
    return(page)
with open('input.txt', 'r') as fp:
    lines = fp.readlines()
    for lines in lines:
        a = lines.split(',')
        page = getPDFPage(a[0],int(a[1]))

        answersRaw = page.extractText().encode('utf-8').split('Questions', 1)[-1]
        #answersRaw = answersRaw.split('Q',1)[-1]
        regex = re.compile('[^A-Z]')
        beforeStrip = ["Questions"]
        afterStrip = ["Return", "College"]
        print(answersRaw)
        for b in beforeStrip:
            if b in answersRaw:
                answersRaw = answersRaw.split(b,1)[-1]
        for b in afterStrip:
            if b in answersRaw:
                answersRaw = answersRaw.split(b,1)[0]
        print(answersRaw)
        answersStripped = regex.sub('', answersRaw)
        print(answersStripped)
        letters = ["A","B","C","D","E"]
        for l in letters:
            print(str(l) + ": " + str(list(answersStripped).count(l)))
            c = d.get(l, 0)
            d[l] = c+list(answersStripped).count(l)


for i in d:
    print i, d[i]

#a-1 for bio
