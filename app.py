from flask import Flask, request,redirect,render_template, url_for, send_file
import hashlib
import os
import time
from datetime import datetime
import shutil
import zipfile
from datetime import datetime

from  werkzeug.utils import secure_filename
app = Flask(__name__)
STATIC_DIR='/var/www/warburton/warr/static'
TEMPLATES_DER='var/www/warburton/warr/template'
BASE_DIR='/var/www/warburton/warr/'
DEBUG= True

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('create.html')


@app.route('/create',methods=['GET','POST'],strict_slashes=False)
def create():
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == "POST":
        colors=[]
        name=request.form['name']
        file = request.files['file']
        if name =='':
            name='default'
        if file.filename=='':
            pic='/var/www/warburton/warr/background.png'
        else:
            pass 
            #TODO грузится стандартная картинка или фон

        now=datetime.now()
        name1=name+str(now)
        hash = hashlib.sha224(name1.encode())
        filename = secure_filename(file.filename)
        folder_name = hash.hexdigest()
        path = '/var/www/warburton/warr/downloads/%s/' % folder_name #main path for all shit
        path_c='/var/www/warburton/warr/color.txt' # template for colors
        os.makedirs('/var/www/warburton/warr/downloads/%s' % folder_name) #create folder like f87390182fd33j2k3h12fgf
        file.save(os.path.join(path,'background.jpg'))
        pic='/var/www/warburton/warr/downloads/%s/background.jpg' % folder_name

        with open(os.path.join(path+'colors.tdesktop-theme'), 'w') as myFile:
            print('COLOR_DARK:#{0}; \nCOLOR_GRAY:#{1}; \nCOLOR_GREEN_DARK : #{2}; \nCOLOR_GREEN_RIPPLE_ACTIVE :#{3};'
                  '\nCOLOR_GREEN_LIGHT:#{4}; \nCOLOR_WHITE: #{5}; \nOUT_MES :#{6}; \nINC_MES:#{7}; \nCOLOR_PINK:#{8}; \nHOVER_COLOR_MENU:#{9}; \n'
                  .format(request.form['main_color'],request.form['sec_color'],request.form['third_color'],request.form['pr_color'],request.form['icons_h'],
                          request.form['text_color'],request.form['out_color'],request.form['inc_color'],request.form['bubles'],
                          request.form['active_chat']),file=myFile)
            with open(path_c, 'r') as myFile1:
                for line in myFile1:
                    myFile.write(line)
        myZipFile = zipfile.ZipFile(path+name+'.tdesktop-theme', "w") #creating .tdesktop-theme
        color_file=path+'colors.tdesktop-theme'
        myZipFile.write(color_file,'colors.tdesktop-theme', zipfile.ZIP_DEFLATED)
        myZipFile.write(pic,'background.jpg',zipfile.ZIP_DEFLATED)
        myZipFile.close()
        return redirect(url_for('download',hash=hash.hexdigest(),name=name))
    return render_template('create.html')


@app.route('/downloads/<hash>/<name>')
def download(hash,name):
    try:
        return send_file('/var/www/warburton/warr/downloads/%s/%s.tdesktop-theme' % (hash,name),attachment_filename='%s.tdesktop-theme'% name ,
                         mimetype='application/zip',as_attachment=True)
    except:
        return render_template('download.html')



#TODO эту хуйню с удалением
# def delete():
#     current_time = time.time()
#     rootdir = '/var/www/warburton/warr/downloads/'
#     for subdir, dirs, files in os.walk(rootdir):
#         oldtime=(os.path.getmtime(subdir))
#         if (current_time - oldtime) >20:
#             import shutil
#             # print(subdir)
#             # shutil.rmtree(subdir)

if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080,debug=DEBUG)

#удаление файлов старее 60 минут
#find /var/www/warburton/warr/downloads/* -mmin +60 -exec rm -rf {} \;
