# TJRJ - Informações sobre processos do TJRJ

**ATENÇÃO:**
parei de desenvolver esse software quando o TJRJ alterou o sistema (colocando captchas). O processo pelo qual me interessava ficou inativo e perdi o interesse em continuar. Não tenho absolutamente nenhum relacionamento com o TJRJ.

---

O módulo Python `tjrj` pega informações de processos jurídicos do site do TJRJ.

O programa `tjrj` é uma interface de linha de comando pra acessar essas informações.

Por enquanto, a única funcionalidade implementada é a de criar um feed
RSS dos movimentos de determinados processos.

## Instalação

    # python setup.py install

Isso instalará tanto o módulo Python quanto os programas de linha de comando.

## Configuração

O programa lê configurações no arquivo `~/.tjrj-processos`, ou no
arquivo especificado pela opção `--config`.

O arquivo de configuração deve ter o seguinte formato:
    
    [DEFAULT]
    diretorio_feeds = /home/lucastx/feeds

    [Telemar]

    numero = 0007765-23.2011.8.19.0037

    [Banco do Brasil]

    numero = 0007764-38.2011.8.19.0037

Na seção `[DEFAULT]`, é definido o diretório onde serão salvos os arquivos
feed (essa opção pode ser sobreposta em cada processo específico, mas pra quê?)

Cada outra seção representa um processo. O nome da seção vira o nome do
processo, e 'numero'... é o número do processo (quem diria!).

## Usando

Para usar o módulo:

    import tjrj

Para executar o programa:

    $ tjrj --help

### Feeds

Para gerar feeds dos processos:

    $ tjrj salvar-feeds [--config ARQUIVO]

O arquivo será nomeado com o número do processo, extensão `.xml`.

### Webserver

    $ tjrj webserver [--port PORTA]

O servidor web pode exibir os últimos movimentos de um processo
diretamente no navegador, em HTML, ou gerar um feed pra ser inscrito em
um leitor de RSS.
