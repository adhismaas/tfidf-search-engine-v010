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

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def process():
	if request.method == 'GET':
		return('<form action="/test" method="post"><input type="submit" value="Send" /></form>')

	elif request.method =='POST':
		kalimat = request.form['text']
		# tandaBaca = ['.',',',':','\"','/','(',')','-',';','\\','{','}']
		kataDepan = pd.read_csv("/datas/konjungsi.csv")
		kataDepan = kataDepan['kataKonjungsi'].tolist()
		dokumen = pd.read_csv("/datas/konjungsi.csv")
		dokumen = dokumen.values.tolist()
		stemmedDoc = []
		factory = StemmerFactory()
		stemmer = factory.create_stemmer()
		i = 0
		tabelDf = []
		tfidf = []
		banyakDok = len(dokumen)
		

		
		# 1 - Tokenizing - menghapus tanda baca (ex : titik koma)
		# tempKalimat = list(kalimat)
		# terdeteksi = [karakter for karakter in tempKalimat if karakter in tandaBaca]

		# for x in terdeteksi:
		# 	for y in tempKalimat:
		# 		tempKalimat = [huruf.replace(x, ' ') for huruf in tempKalimat]

		# kalimat = " ".join(tempKalimat)
		kata = kalimat.split()
		tabelTf = [[]*len(kata) for x in range(banyakDok)]

		# 2 - Filtering - cek bila kata memiliki kata depan yang harus dihapus
		kata = [x for x in kata if x not in kataDepan]

		# 3 - Stemming - menghapus awalan
		kata = [stemmer.stem(x) for x in kata]

		# 4 - hitung tf.idf
		# while counter < len(dokumen):
		# 	tf[counter] = [x.count() for x in dokumen if x is kata[counter]]
		# 	counter += 1

		for baris in dokumen:
			arrayTempBaris = list(baris[3])

			# 2 - Filtering - cek bila kata memiliki kata depan yang harus dihapus
			arrayTempBaris = [x for x in arrayTempBaris if x not in kataDepan]
			tempBaris = "".join(arrayTempBaris)

			# 3 - Stemming - menghapus awalan
			tempBaris = stemmer.stem(tempBaris)
			stemmedDoc.append(tempBaris.split())

		#masukkan proses pencarian - penampilan hasil disini
		# s = [w.replace([x for x in s if x in tandaBaca], ' ') for w in s]

		#hitung tf
		for i in range(len(stemmedDoc)):
			for n in range(len(kata)):
				tabelTf[n][i] = stemmedDoc[i].count()

		#hitung df
		for data in tabelTf:
			tabelDf = sum(data)

		for data in tabelDf:
			data = (1 + math.log(len(banyakDok/data)))

		for i in range(len(stemmedDoc)):
			for n in range(len(kata)):
				tfidf.append(tabelTf[i][n] * tabelDf[n])
# run app
if __name__ == "__main__":
    app.run()