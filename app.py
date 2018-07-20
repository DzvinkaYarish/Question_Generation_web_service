from flask import Flask, render_template, request
import subprocess
from pycorenlp import StanfordCoreNLP
import requests
import json

IN_FILE = 'in.txt'
OUT_FILE = 'out.txt'
TREE_FILE = 'tree.txt'
# JAR = '../../IdeaProjects/Graphene_sent_simpl__discourse/SentenceSimplification/target/' \
#       'sentence-simplification-5.0.0-jar-with-dependencies.jar'
JAR_SS = 'sentence-simplification-5.0.0-jar-with-dependencies.jar'
JAR_QG = ''


app = Flask(__name__)
nlp = StanfordCoreNLP('172.17.0.1:9003')


def get_tree(sent):
    url = "http://localhost:9001/tregex"
    request_params = {
        "pattern": "S|SBAR !> ROOT !< S|SBAR"}  # split by all kinds of conjunctions(including non restrictive relative clauses)
    text = "The woman who visited me in the hospital was very kind."""  # participial also if coma
    d_s = requests.post(url, data=text, params=request_params).text
    print(d_s)
    # output = nlp.annotate(sent, properties={
    #   'annotators': 'tokenize,ssplit,pos,depparse,parseparse',
    #   'outputFormat': 'json'
    #   })
    # with open(TREE_FILE, 'w') as f:
    #     f.write(output['sentences'][0]['parse'])


def parse_qg_output(q):
    q_p = [p.strip('[]') for p in q.split()]
    q_p = [v.split('=')[1] for v in q_p if v.startswith('Value')]
    return q_p


def simplify_sentence(sent):
    with open(OUT_FILE) as F:
        pass
    with open(IN_FILE, 'w') as f:
        f.write(sent)
    return subprocess.call(['java', '-jar', JAR_SS, IN_FILE, OUT_FILE])
    # return subprocess.call('java -jar ' + JAR + ' ' + IN_FILE + ' ' + OUT_FILE, shell=True)


def generate_question(sent):
    get_tree(sent)
    return 1
    # return subprocess.call(['java', '-jar', JAR_QG, TREE_FILE, OUT_FILE])


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/generate-questions')
def get_template_qg():
    return render_template('question_gen_template.html')


@app.route('/generate-questions', methods=['POST'])
def question_generation():
    sent = request.form['sentence']
    if generate_question(sent):
        return render_template('question_gen_template.html', Sentence='Error')
    else:
        with open(OUT_FILE) as f:
            questions = [' '.join(parse_qg_output(l.strip())) for l in f.readlines()]
        return render_template('question_gen_template.html', Sentence=sent, Questions=';'.join(questions))


@app.route('/simplify-sentence')
def get_template_ss():
    return render_template('sent_simlp_template.html')


@app.route('/simplify-sentence',  methods=["POST"])
def sentence_simplification():
    sent = request.form['sentence']
    if sentence_simplification(sent):
        return render_template('sent_simlp_template.html', Core='Error')
    else:
        with open(OUT_FILE, 'r') as f:
            content = f.readlines()
            return render_template('sent_simlp_template.html', Original=str(content[0]), Core=str(content[1]), Context=str(' \t\n'.join(content[2:])))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
