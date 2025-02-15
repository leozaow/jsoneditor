from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Altere para algo seguro em produção

# Exemplo simples de usuários
users = {
    'gmrio': 'gmrio',
    'leal': 'leal123',
    'barbosa': 'barbosa123',
    'userbeta': 'userbeta123'
}

def log_action(action):
    logs = session.get('logs', [])
    logs.append(action)
    session['logs'] = logs

@app.route('/', methods=['GET', 'POST'])
def login():
    # Se já está logado, vai direto para o editor
    if 'username' in session:
        return redirect(url_for('editor'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['username'] = username
            log_action(f"Usuário '{username}' fez login.")
            return redirect(url_for('editor'))
        else:
            flash('Credenciais inválidas', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        log_action(f"Usuário '{session['username']}' fez logout.")
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/editor', methods=['GET'])
def editor():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Apenas enviamos uma estrutura JSON vazia padrão
    # O restante é manipulado apenas no navegador (JavaScript)
    data = '{"s1202RemuTrabRPPSGroup":{"s1202RemuTrabRPPS":[]}}'
    return render_template('editor.html', data=data)

@app.route('/logs', methods=['GET'])
def show_logs():
    if 'username' not in session:
        return redirect(url_for('login'))
    logs = session.get('logs', [])
    return render_template('logs.html', logs=logs)

if __name__ == '__main__':
    # Rode em modo debug se desejar: app.run(debug=True)
    app.run(host='0.0.0.0', port=80)
