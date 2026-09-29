# Gabarito — Atividade de Revisão

**Uso exclusivo do professor.** Não distribuir aos alunos. Esta atividade não vale nota — é preparatória para a AP1.

## Parte 1 — Associação comando → função

1. `docker run hello-world` → **E** (Roda uma imagem mínima só para confirmar que a instalação do Docker funciona)
2. `-d` → **B** (Executa o container em segundo plano, liberando o terminal)
3. `-p 8080:80` → **C** (Mapeia uma porta do host para uma porta do container)
4. `-v pasta:destino` → **F** (Conecta uma pasta externa aos dados de dentro do container, para os dados persistirem)
5. `ssh usuario@endereco -p porta` → **A** (Conecta a um servidor remoto, informando usuário, endereço e porta)
6. `ls` → **G** (Lista os arquivos e pastas do diretório atual)
7. `cd` → **J** (Entra em outra pasta (navega no sistema de arquivos))
8. `cat` → **I** (Mostra na tela o conteúdo de um arquivo de texto)
9. `nano` → **H** (Abre um editor de texto simples no terminal, para criar ou editar arquivos)
10. `sudo apt install -y docker.io` → **D** (Instala o Docker através do gerenciador de pacotes do sistema)

## Parte 2 — Complete o comando

```
docker run -d --name meusite -p 8080:80 -v ~/site:/usr/share/nginx/html nginx
```

(A ordem das flags `-d`, `-p` e `-v` entre si não importa, desde que `--name meusite` continue logo após `docker run` e cada flag preceda seu respectivo valor.)

## Parte 3 — Verdadeiro ou Falso

1. **F** — O comando docker --version já garante que o daemon do Docker está pronto para receber comandos como docker run.
   *Justificativa:* O cliente (docker --version) responde mesmo sem falar com o daemon; docker ps/docker run só funcionam quando o daemon está pronto — por isso o roteiro usa um comando/script de espera.

2. **V** — Dados gravados dentro de um volume (-v) sobrevivem à recriação do container.
   *Justificativa:* Essa é justamente a diferença entre o que é efêmero (dentro do container) e o que persiste (no volume, fora dele).

3. **F** — O comando cat permite editar o conteúdo de um arquivo de texto.
   *Justificativa:* cat apenas exibe o conteúdo na tela; quem edita é o nano.

4. **V** — Cada servidor remoto pode expor o SSH em uma porta diferente dos demais.
   *Justificativa:* Por isso é preciso sempre conferir a porta (e o usuário) de cada servidor antes de conectar.

5. **V** — Uma pista de investigação pode estar escondida apenas no NOME de um arquivo, sem nada revelador no conteúdo.
   *Justificativa:* Exatamente o princípio de investigação sistemática: olhar também para nomes de arquivos e pastas, não só para o texto dentro deles.

6. **F** — Em uma prática com apenas 4 comandos permitidos, remover ou mover arquivos livremente (rm, mv) é uma opção esperada.
   *Justificativa:* O conjunto de comandos permitidos é deliberadamente restrito (ex.: ls, cd, cat, nano); comandos destrutivos ou de movimentação não fazem parte dele.

## Parte 4 — Questões abertas (respostas esperadas)

1. O daemon do Docker provavelmente ainda não terminou de iniciar quando o `hello-world` foi executado. `docker --version` é um comando de cliente e responde mesmo sem o daemon pronto; comandos como `docker run` e `docker ps` precisam do daemon ativo. O colega deveria aguardar (ou usar um comando/script que confirme com `docker info` que o daemon já está pronto) antes de tentar novamente.

2. O nome `backup_2024-11-03_bloqueado.txt` já sugere, sem abrir o arquivo: que é um backup, de uma data específica (03/11/2024), e que está marcado como "bloqueado" — um forte indício de que algo relevante está ali. Prestar atenção a nomes de arquivo é importante porque nem toda informação relevante é escrita por extenso dentro do conteúdo; datas, palavras-chave e marcações no próprio nome podem ser a pista principal, e ignorá-las faz a investigação perder informação.
