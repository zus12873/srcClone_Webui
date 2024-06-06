from flask import Flask, render_template, request, redirect, url_for,jsonify
import os
import subprocess
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': 'No files selected'})
        
        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1.filename == '' or file2.filename == '':
            return jsonify({'error': 'Empty file'})

        file1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)

        file1.save(file1_path)
        file2.save(file2_path)
        
        # 检查文件是否成功保存
        if os.path.exists(file1_path) and os.path.exists(file2_path):
            # 调用外部 Python 脚本
            cmd = ['python3', 'srcClone.py', file1_path, file2_path]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            # 处理脚本的输出，这里只是简单地返回输出文本
            print(result.stdout)
            return jsonify({'output':result.stdout})
        else:
            return jsonify({'error': 'Failed to save file'})

    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
