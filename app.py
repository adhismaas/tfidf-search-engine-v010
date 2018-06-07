from flask import Flask, render_template, request
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import pandas as pd
import json
import webbrowser
import numpy as np
import math
import copy

# algorithm :
# 1. take input from user
# 2. tf-idf the input, further information on ppt
# 3. compare result with ones from database / json

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def process():
	if request.method == 'GET':
		return render_template('result.html')

	elif request.method =='POST':
		kalimat = request.form['keyword']
		kataDepan = pd.read_csv("datas/konjungsi.csv")
		kataDepan = kataDepan.values.tolist()
		datasets = pd.read_csv("datas/datasets.csv")
		dokumen = datasets.values.tolist()
		stemmedDoc = []
		factory = StemmerFactory()
		stemmer = factory.create_stemmer()
		temp = 0
		tfidf = []
		banyakDok = len(dokumen)

		kata = kalimat.split()
		tabelTf = [[0]* banyakDok for x in range(len(kata))]
		tabelDf = []
		# # tabelTf[2] = [3,4,5]
		# print(tabelDf)
		hasil = [[] for x in range(banyakDok)]

		# 2 - Filtering - cek bila kata memiliki kata depan yang harus dihapus
		kata = [x for x in kata if x not in kataDepan]

		# 3 - Stemming - menghapus awalan
		kata = [stemmer.stem(x) for x in kata]

		# print(dokumen)

		for baris in dokumen:
			arrayTempBaris = baris[3].split()

			# 2 - Filtering - cek bila kata memiliki kata depan yang harus dihapus
			arrayTempBaris = [x for x in arrayTempBaris if x not in kataDepan]
			tempBaris = " ".join(arrayTempBaris)


			# 3 - Stemming - menghapus awalan
			tempBaris = stemmer.stem(tempBaris)
			stemmedDoc.append(tempBaris.split())
			# pprint(stemmedDoc)

		#masukkan proses pencarian - penampilan hasil disini
		# s = [w.replace([x for x in s if x in tandaBaca], ' ') for w in s]

		#hitung tf
		for i in range(len(stemmedDoc)):
			for n in range(len(kata)):
				tabelTf[n][i] = stemmedDoc[i].count(kata[n])

		#hitung df
		for data in tabelTf:
			tabelDf.append(sum(data))

		for i in range(len(tabelDf)):
			if tabelDf[i] == 0:
				tabelDf[i] = 0
			else:
				tabelDf[i] = (1 + math.log(banyakDok/tabelDf[i]))

		# pprint(tabelTf)
		# pprint(tabelTf[1][29])
		# pprint(tabelTf[1,29:29])

		# print("tabelTf = ", tabelTf, "\n TabelDf = ", tabelDf, "\n Kata = ", kata)
		for i in range(len(stemmedDoc)):
			# pprint(i)
			for n in range(len(kata)):
				# tfidf[i].append(tabelTf[i][n] * tabelDf[n])
				temp += tabelTf[n][i] * tabelDf[n]
			# 	pprint(n)
			# 	pprint(tabelTf[n][i])
			# 	pprint(temp)
			tfidf.append(temp)
			temp=0

		datasets['tfidf'] = pd.Series(tfidf)
		datasets = datasets.sort_values(by=['tfidf'], ascending=False)
		print(datasets)

		# # pprint(tabelTf)
		# # pprint(tfidf)

		# for i in range(len(tfidf)):
		# 	for n in range (len(tfidf)):
		# 		# pprint(temp)
		# 		# pprint(tfidf[n])
		# 		pprint(temp)
		# 		if temp < tfidf[n]:
		# 			x = hasil[i]
		# 			hasil[i] = n
		# 			hasil[n] = x
		# 			temp = tfidf[n]
		# 	temp=0

		# return datasets.values.tolist()
		return render_template('result.html', keyword=kalimat, data=datasets.values.tolist())

	# else:
 #        ('<center>404 Not Found</center>')

# run app
if __name__ == "__main__":
    app.run(debug=True)