from flask import Flask, render_template, request
import subprocess

IN_FILE = 'in.txt'
OUT_FILE = 'out.txt'
# JAR = '../../IdeaProjects/Graphene_sent_simpl__discourse/SentenceSimplification/target/' \
#       'sentence-simplification-5.0.0-jar-with-dependencies.jar'
JAR = 'sentence-simplification-5.0.0-jar-with-dependencies.jar'


app = Flask(__name__)
def sentence_simplification(sent):
    with open(OUT_FILE) as F:
        pass
    with open(IN_FILE, 'w') as f:
        f.write(sent)
    return subprocess.call(['java', '-jar', JAR, IN_FILE, OUT_FILE])
    # return subprocess.call('java -jar ' + JAR + ' ' + IN_FILE + ' ' + OUT_FILE, shell=True)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/simplify-sentence')
def get_template():
    return render_template('index.html')


@app.route('/simplify-sentence',  methods=["POST"])
def simplify_sentence():
    sent = request.form['sentence']
    if sentence_simplification(sent):
        return render_template('index.html', Core='Error')
    else:
        with open(OUT_FILE, 'r') as f:
            content = f.readlines()
            return render_template('index.html', Original=str(content[0]), Core=str(content[1]), Context=str(' \t\n'.join(content[2:])))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
