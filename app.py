from flask import Flask, render_template, \
  request, redirect, url_for
import pymysql.cursors, os, xmlrpc.client

application = Flask(__name__)

conn = cursor = None
#fungsi koneksi database
def openDb():
   global conn, cursor
   conn = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='db_penjualan',
                             charset='utf8mb4')
   cursor = conn.cursor()	
#fungsi untuk menutup koneksi
def closeDb():
   global conn, cursor
   cursor.close()
   conn.close()
#fungsi view index() untuk menampilkan data dari database
@application.route('/')
def index():   
   openDb()
   container = []
   sql = "SELECT * FROM barang"
   cursor.execute(sql)
   results = cursor.fetchall()
   for data in results:
      container.append(data)
   closeDb()
   return render_template('index.html', container=container,)

#fungsi view tambah() untuk membuat form tambah
@application.route('/tambah', methods=['GET','POST'])
def tambah():
   if request.method == 'POST':
      nama = request.form['nama']
      harga = request.form['harga']
      stok = request.form['stok']
      openDb()
      sql = "INSERT INTO barang (nama_barang, harga,stok) VALUES (%s, %s, %s)"
      val = (nama, harga, stok)
      cursor.execute(sql, val)
      conn.commit()
      closeDb()
      return redirect(url_for('index'))
   else:
      return render_template('tambah.html')
#fungsi view edit() untuk form edit
@application.route('/edit/<id_barang>', methods=['GET','POST'])
def edit(id_barang):
   openDb()
   cursor.execute('SELECT * FROM barang WHERE id_barang=%s', (id_barang))
   data = cursor.fetchone()
   if request.method == 'POST':
      id_barang = request.form['id_barang']
      nama = request.form['nama']
      harga = request.form['harga']
      stok = request.form['stok']
      sql = "UPDATE barang SET nama_barang=%s, harga=%s, stok=%s WHERE id_barang=%s"
      val = (nama, harga, stok, id_barang)
      cursor.execute(sql, val)
      conn.commit()
      closeDb()
      return redirect(url_for('index'))
   else:
      closeDb()
      return render_template('edit.html', data=data)
#fungsi untuk menghapus data
@application.route('/hapus/<id_barang>', methods=['GET','POST'])
def hapus(id_barang):
   openDb()
   cursor.execute('DELETE FROM barang WHERE id_barang=%s', (id_barang,))
   conn.commit()
   closeDb()
   return redirect(url_for('index'))

#fungsi odoo xml-rpc
def call_odoo_method(url, db, username, password, model, method, *args):
   # Authenticate
   common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
   uid = common.authenticate(db, username, password, {})

   # Call the method
   models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
   result = models.execute_kw(db, uid, password, model, method, args)
   return result

@application.route('/odooapi',methods=['GET','POST'])
def odooapi():
   # client =  Client(host='https://fastprintid.odoo.com',
   #          dbname='fastprintid-sandyhartono-master-1221888',
   #          user='prog4.fastprintsby@gmail.com',
   #          pwd='odoo13')
   # from xmlrpc.server import xmlrpclib
   url = 'https://fastprintid.odoo.com',
   db = 'fastprintid-sandyhartono-master-1221888',
   username = 'prog4.fastprintsby@gmail.com',
   password = 'odoo13'
   partners = call_odoo_method(url, db, username, password, 'res.partner', 'search', [[]])
   print(partners)
      
if __name__ == '__main__':
   application.run(debug=True)