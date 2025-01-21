Calculadora de Meta Financeira
Este projeto é uma aplicação gráfica desenvolvida com PyQt5 que permite ao usuário definir uma meta financeira, registrar depósitos e acompanhar seu progresso. O aplicativo calcula automaticamente o total depositado, exibe o progresso em uma barra visual e fornece a opção de exportar o histórico de depósitos para um arquivo CSV.

Funcionalidades
Configuração de Meta: O usuário pode definir uma meta financeira e o número máximo de depósitos a serem feitos.
Rastreamento de Progresso: O progresso em relação à meta é exibido através de uma barra de progresso visual.
Histórico de Depósitos: O programa mantém um histórico de todos os depósitos realizados, incluindo valores e datas.
Notificação de Sucesso: Ao atingir a meta ou o número máximo de depósitos, o usuário pode definir uma nova meta ou salvar os dados em um arquivo CSV.
Exportação para CSV: O histórico de depósitos pode ser exportado para um arquivo CSV, que inclui a meta financeira, o número máximo de depósitos e os detalhes de cada depósito.

Tecnologias Utilizadas
Python: Linguagem de programação principal.
PyQt5: Biblioteca para a criação da interface gráfica.
JSON: Para persistência dos dados entre as sessões do programa.
CSV: Para exportação do histórico de depósitos.

Como Usar
Clonar o Repositório: Clone este repositório para sua máquina local:

bash
Copiar
Editar
git clone https://github.com/Caique94/ControleDeInvestimentos.git
Instalar as Dependências: Instale as dependências necessárias com pip:

bash
Copiar
Editar
pip install pyqt5
Rodar o Programa: Execute o arquivo principal para iniciar o aplicativo:

bash
Copiar
Editar
python main.py
Fluxo do Aplicativo
1. Configuração Inicial:
Ao iniciar o aplicativo, você será solicitado a definir sua meta financeira (valor que deseja alcançar) e o número máximo de depósitos. Esses valores serão usados para calcular seu progresso.

2. Adicionar Depósitos:
Para adicionar um depósito, insira o valor desejado e clique em "Adicionar Depósito". O valor será somado ao total depositado, e o progresso será atualizado.

3. Visualizar Histórico:
Você pode visualizar o histórico de depósitos clicando no botão "Ver Histórico de Depósitos". Ele exibirá todos os depósitos realizados, com seus valores e datas.

4. Sucesso na Meta:
Quando você atingir sua meta ou o número máximo de depósitos, o programa perguntará se você deseja definir uma nova meta ou exportar os dados para um arquivo CSV.

5. Exportar para CSV:
O histórico de depósitos pode ser exportado para um arquivo CSV, que incluirá os dados da meta, o número máximo de depósitos e o histórico completo de depósitos.

Exemplo de Arquivo CSV Gerado
O arquivo CSV gerado incluirá informações como:

Meta: O valor total a ser alcançado.
Depósitos Máximos: O número máximo de depósitos permitidos.
Total Depositado: O total de depósitos realizados.
Contagem de Depósitos: O número de depósitos feitos.
E para cada depósito:
Valor: O valor do depósito.
Data: A data e hora do depósito.
Contribuindo
Contribuições são bem-vindas! Siga os passos abaixo para contribuir para o projeto:

Faça um fork deste repositório.
Crie uma nova branch para sua feature:
git checkout -b minha-feature

Faça suas alterações e commite:
git commit -m "Adiciona nova funcionalidade"

Push sua branch:
git push origin minha-feature
Abra um Pull Request para revisão.

Licença
Este projeto está licenciado sob a MIT License.

