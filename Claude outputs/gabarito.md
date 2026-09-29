# Gabarito — AP1 (Docker e Administração de Sistemas Linux)

**Uso exclusivo do professor — não distribuir aos alunos.**

Cada prova tem 10 questões de múltipla escolha, todas valendo 1,0 pt (total: 10,0 pts por
prova). A distribuição de dificuldade (4 questões muito fáceis, 4 fáceis e 2 médias) foi
mantida apenas para equilibrar a prova internamente — não afeta a pontuação.

---

## Gabarito — Prova A

| Nº | Dificuldade | Valor | Resposta |
|---|---|---|---|
| 1 | muito fácil | 1.0 | **A** |
| 2 | muito fácil | 1.0 | **C** |
| 3 | muito fácil | 1.0 | **B** |
| 4 | muito fácil | 1.0 | **C** |
| 5 | fácil | 1.0 | **A** |
| 6 | fácil | 1.0 | **B** |
| 7 | fácil | 1.0 | **B** |
| 8 | fácil | 1.0 | **B** |
| 9 | média | 1.0 | **B** |
| 10 | média | 1.0 | **B** |

**1. (muito fácil, 1.0 pt) — resposta: A**
> Qual comando é usado para conectar a um servidor remoto via SSH, informando usuário, endereço e porta?

- A) ssh usuario@endereco -p porta ✅
- B) ftp usuario@endereco -p porta
- C) ping usuario@endereco -p porta
- D) telnet -u usuario endereco

*Justificativa:* É a sintaxe padrão de conexão SSH usada ao longo do curso.

**2. (muito fácil, 1.0 pt) — resposta: C**
> Em um terminal Linux, qual comando mostra o conteúdo de um arquivo de texto na tela?

- A) nano
- B) ls
- C) cat ✅
- D) cd

*Justificativa:* cat exibe o conteúdo do arquivo; nano edita, ls lista, cd navega.

**3. (muito fácil, 1.0 pt) — resposta: B**
> Qual comando é usado para verificar rapidamente se a instalação do Docker está funcionando, rodando uma imagem de teste simples?

- A) docker install
- B) sudo docker run hello-world ✅
- C) docker test
- D) docker check

*Justificativa:* hello-world é a imagem de teste padrão do Docker.

**4. (muito fácil, 1.0 pt) — resposta: C**
> Qual editor de texto em modo terminal foi usado ao longo do curso para criar e editar arquivos?

- A) vim
- B) gedit
- C) nano ✅
- D) word

*Justificativa:* nano é o editor de terminal usado nas atividades práticas.

**5. (fácil, 1.0 pt) — resposta: A**
> Em um sistema Linux (Ubuntu), qual comando instala o Docker através do gerenciador de pacotes apt?

- A) sudo apt install -y docker.io ✅
- B) sudo docker install
- C) sudo yum install docker
- D) sudo docker.io start

*Justificativa:* apt install -y docker.io é o comando padrão de instalação em distribuições baseadas em Debian/Ubuntu.

**6. (fácil, 1.0 pt) — resposta: B**
> Em uma VM sem systemd, o daemon do Docker pode levar alguns segundos para ficar pronto depois de iniciado. Qual é a forma correta de lidar com isso antes de continuar?

- A) Rodar o comando de início e seguir em frente imediatamente, sem checar nada
- B) Usar um comando/script que aguarda e confirma (por exemplo, com "docker info") que o daemon está pronto antes de liberar o terminal ✅
- C) Reiniciar a máquina inteira
- D) Ignorar o problema, pois ele nunca acontece

*Justificativa:* Sem essa espera ativa, comandos como "docker ps" podem falhar por o daemon ainda não estar pronto, mesmo o cliente respondendo normalmente.

**7. (fácil, 1.0 pt) — resposta: B**
> No nano, qual atalho de teclado é usado para salvar o arquivo que está sendo editado?

- A) Ctrl+S
- B) Ctrl+O ✅
- C) Ctrl+W
- D) Ctrl+Z

*Justificativa:* Ctrl+O (de "output") salva; depois é preciso confirmar com Enter.

**8. (fácil, 1.0 pt) — resposta: B**
> No comando "sudo docker run -d --name meusite -p 8080:80 -v ~/site:/usr/share/nginx/html nginx", o que a opção -d faz?

- A) Apaga o container depois de usar
- B) Roda o container em segundo plano (modo "detached") ✅
- C) Define o nome do container
- D) Ativa o modo de depuração

*Justificativa:* -d = detached, o container roda em segundo plano e libera o terminal.

**9. (média, 1.0 pt) — resposta: B**
> Um aluno editou um arquivo HTML com o nano, publicou um container Nginx usando esse arquivo como volume, e depois precisou recriar o container. O conteúdo editado continuava lá depois da recriação. Por que isso acontece?

- A) Porque o Nginx salva uma cópia automática na internet
- B) Porque o arquivo estava dentro de um volume, que existe fora do container e não é apagado quando ele é recriado ✅
- C) Porque o Docker nunca apaga nada, mesmo sem volume
- D) Porque toda imagem Docker guarda uma cópia de segurança

*Justificativa:* O volume monta um caminho externo ao container; o conteúdo vive fora dele e sobrevive à recriação.

**10. (média, 1.0 pt) — resposta: B**
> Ao explorar o sistema de arquivos de um servidor remoto via SSH, usando apenas comandos de leitura (sem poder apagar ou mover nada), por que pode ser útil prestar atenção também aos nomes dos arquivos e pastas, e não só ao conteúdo deles?

- A) Porque nomes de arquivo nunca têm relevância nenhuma
- B) Porque, às vezes, uma informação importante está codificada no próprio nome do arquivo, e não escrita no texto dentro dele ✅
- C) Porque arquivos com nomes longos sempre têm erro
- D) Porque o comando cat só funciona em arquivos com nomes curtos

*Justificativa:* Nem toda informação relevante está escrita por extenso; o nome do arquivo também pode carregar dados.

---

## Gabarito — Prova B

| Nº | Dificuldade | Valor | Resposta |
|---|---|---|---|
| 1 | muito fácil | 1.0 | **B** |
| 2 | muito fácil | 1.0 | **A** |
| 3 | muito fácil | 1.0 | **A** |
| 4 | muito fácil | 1.0 | **A** |
| 5 | fácil | 1.0 | **B** |
| 6 | fácil | 1.0 | **A** |
| 7 | fácil | 1.0 | **B** |
| 8 | fácil | 1.0 | **B** |
| 9 | média | 1.0 | **B** |
| 10 | média | 1.0 | **A** |

**1. (muito fácil, 1.0 pt) — resposta: B**
> Qual comando lista os arquivos e pastas do diretório atual em um terminal Linux?

- A) cat
- B) ls ✅
- C) nano
- D) cd

*Justificativa:* ls lista o conteúdo do diretório atual.

**2. (muito fácil, 1.0 pt) — resposta: A**
> Qual comando é usado para entrar em uma pasta em um terminal Linux (e "cd .." para voltar)?

- A) cd ✅
- B) ls
- C) open
- D) go

*Justificativa:* cd (change directory) navega entre pastas.

**3. (muito fácil, 1.0 pt) — resposta: A**
> No nano, qual atalho de teclado fecha o editor (sair)?

- A) Ctrl+X ✅
- B) Ctrl+Q
- C) Ctrl+E
- D) Esc

*Justificativa:* Ctrl+X sai do nano (perguntando antes se quer salvar).

**4. (muito fácil, 1.0 pt) — resposta: A**
> Qual comando testa se a instalação do Docker deu certo, baixando e rodando uma imagem simples que só imprime uma mensagem?

- A) sudo docker run hello-world ✅
- B) sudo docker test
- C) sudo docker check-install
- D) sudo docker ping

*Justificativa:* hello-world é a imagem padrão de verificação de instalação do Docker.

**5. (fácil, 1.0 pt) — resposta: B**
> No comando "ssh aluno01@ENDERECO -p 2201", o que representa o número 2201?

- A) A senha do usuário
- B) A porta usada para conectar via SSH naquele servidor específico ✅
- C) O número de tentativas permitidas
- D) O ID do container

*Justificativa:* Cada servidor/VM pode expor o SSH numa porta diferente, informada depois do -p.

**6. (fácil, 1.0 pt) — resposta: A**
> Ao longo das atividades práticas, os alunos usaram apenas quatro comandos de terminal para explorar pastas e ler e editar arquivos remotamente via SSH. Quais são eles?

- A) ls, cd, cat, nano ✅
- B) ls, rm, mv, cp
- C) ssh, ping, curl, wget
- D) cd, mkdir, touch, chmod

*Justificativa:* ls (listar), cd (navegar), cat (ler) e nano (editar) cobrem exploração e edição básicas.

**7. (fácil, 1.0 pt) — resposta: B**
> No comando "sudo docker run -d --name meusite -p 8080:80 -v ~/site:/usr/share/nginx/html nginx", o que a opção -p 8080:80 faz?

- A) Define a senha do container
- B) Mapeia a porta 8080 do host para a porta 80 dentro do container ✅
- C) Limita o uso de processador a 80%
- D) Apaga a porta 80 do container

*Justificativa:* -p host:container mapeia a porta externa (8080) para a porta interna do Nginx (80).

**8. (fácil, 1.0 pt) — resposta: B**
> Por que é comum, logo após instalar o Docker, rodar "sudo docker run hello-world" antes de fazer qualquer outra coisa?

- A) Para configurar a senha do usuário
- B) Para confirmar que a instalação do Docker está funcionando corretamente ✅
- C) Para publicar um site
- D) Para desinstalar o Docker de teste

*Justificativa:* É um teste rápido de que o Docker foi instalado e o daemon está respondendo.

**9. (média, 1.0 pt) — resposta: B**
> Em uma atividade prática, um aluno precisava editar, com o nano, um arquivo contendo um valor específico (por exemplo, uma coordenada ou um código), que depois seria conferido automaticamente por um script de correção. Por que é importante digitar exatamente o valor esperado, e não um valor qualquer?

- A) Porque qualquer valor funciona, contanto que o arquivo seja salvo
- B) Porque um script de correção automatizado compara o valor salvo com o valor esperado, e só considera correto quando eles coincidem (dentro de uma tolerância definida) ✅
- C) Porque o nano só aceita determinados caracteres
- D) Porque valores errados travam a conexão SSH

*Justificativa:* A correção automática compara o valor editado com o valor esperado; digitar algo diferente é considerado incorreto.

**10. (média, 1.0 pt) — resposta: A**
> Um aluno publicou um Nginx com "sudo docker run -d --name meusite -p 8080:80 -v ~/site:/usr/share/nginx/html nginx", mas ao acessar o site pelo navegador numa porta pública mapeada, a página não abre — embora "curl localhost:8080" funcione normalmente de dentro da própria VM. Qual é a causa mais provável?

- A) O Nginx foi publicado numa porta diferente de 8080 dentro da VM (por exemplo, -p 80:80), então o mapeamento externo não encontra nada na 8080 ✅
- B) O navegador não suporta HTML
- C) O arquivo index.html está vazio
- D) A internet do aluno caiu

*Justificativa:* Se o mapeamento externo aponta para a porta 8080 interna e o Nginx não está publicado nela, o mapeamento não encontra o serviço.
